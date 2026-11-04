#!/usr/bin/env python3
"""select_stimuli.py (v3) — deterministic selection of 1 candidate per topic x cell (384) from
pool_measured.jsonl for the 2x2 register x tightness design.

Objective: minimise the maximum of |r(tightness, log_ppl)| and |r(tightness, tokens)| computed
overall, within the verse rows and within the prose rows (six correlations), subject to per-domain
mean tokens across the four cells differing by < 10 % (max/min - 1). A secondary term (weight 0.1)
keeps the per-domain correlations small as well; they are reported but are not a gate. Candidates
with len_ok=false are penalised, not forbidden. Search: greedy coordinate descent with random restarts (seed 20261030).

Gate (PLAN.md s3 v2): every one of the six |r| < 0.10 and every per-domain spread < 10 %.
v3 adds a HARD constraint: only candidates coded address = none by BOTH the regex and the blind LLM
coder (address_codes.jsonl from address_screen.py) are admissible; the script aborts if any topic x
cell slot has no admissible candidate. stimuli.jsonl rows carry address_regex, address_llm, attrib_count.
Writes stimuli.jsonl, manifest.json and the decorrelation section of selection_report.md.
"""
import argparse, hashlib, json, random, time
from collections import defaultdict
from pathlib import Path
import numpy as np

SEED = 20261030
CELLS = ["loose_verse", "tight_verse", "tight_prose", "loose_prose"]
REGISTERS = ["verse", "prose"]
R_TARGET = 0.10
TOK_TOL = 0.10
HERE = Path(__file__).resolve().parent


def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if len(x) < 3 or x.std() == 0 or y.std() == 0:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


class Problem:
    def __init__(self, rows):
        cells = defaultdict(list)
        for r in rows:
            cells[(r["topic_id"], r["cell"])].append(r)
        self.keys = sorted(cells)
        self.cands = [cells[k] for k in self.keys]
        self.n = len(self.keys)
        self.tight = np.array([1.0 if cells[k][0]["tightness"] == "tight" else 0.0 for k in self.keys])
        self.reg = np.array([cells[k][0]["register"] for k in self.keys])
        self.cell = np.array([k[1] for k in self.keys])
        self.domain = np.array([cells[k][0]["domain"] for k in self.keys])
        self.domains = sorted(set(self.domain))
        self.scopes = {"all": np.arange(self.n)}
        for g in REGISTERS:
            self.scopes[g] = np.where(self.reg == g)[0]
        self.dom_scopes = {}
        for d in self.domains:
            self.dom_scopes[(d, "all")] = np.where(self.domain == d)[0]
            for g in REGISTERS:
                self.dom_scopes[(d, g)] = np.where((self.domain == d) & (self.reg == g))[0]
        self.cell_idx = {(d, c): np.where((self.domain == d) & (self.cell == c))[0] for d in self.domains for c in CELLS}
        self.tok = [np.array([c["tokens"] for c in cs], float) for cs in self.cands]
        self.lpp = [np.array([c["log_ppl"] for c in cs], float) for cs in self.cands]
        self.bad = [np.array([0.0 if c["gen_meta"].get("len_ok", True) else 1.0 for c in cs]) for cs in self.cands]

    def features(self, choice):
        tok = np.array([self.tok[i][c] for i, c in enumerate(choice)])
        lpp = np.array([self.lpp[i][c] for i, c in enumerate(choice)])
        bad = sum(self.bad[i][c] for i, c in enumerate(choice))
        return tok, lpp, bad

    def core(self, choice):
        tok, lpp, bad = self.features(choice)
        r = {s: (pearson(self.tight[ix], tok[ix]), pearson(self.tight[ix], lpp[ix])) for s, ix in self.scopes.items()}
        spread = {}
        for d in self.domains:
            means = [tok[self.cell_idx[(d, c)]].mean() for c in CELLS]
            spread[d] = max(means) / min(means) - 1
        return tok, lpp, bad, r, spread

    def objective(self, choice):
        tok, lpp, bad, r, spread = self.core(choice)
        rs = [abs(v) for pair in r.values() for v in pair]
        obj = max(rs) + 0.2 * sum(rs)
        # secondary (not a gate): keep the per-domain correlations small too
        obj += 0.1 * np.mean([abs(pearson(self.tight[ix], tok[ix])) + abs(pearson(self.tight[ix], lpp[ix]))
                              for (d, g), ix in self.dom_scopes.items() if g == "all"])
        obj += 10.0 * sum(max(0.0, s - TOK_TOL) for s in spread.values())
        obj += 0.05 * bad
        return obj

    def stats(self, choice):
        tok, lpp, bad, r, spread = self.core(choice)
        s = {"r": {k: {"tokens": v[0], "log_ppl": v[1]} for k, v in r.items()},
             "token_spread": spread, "len_ok_violations": int(bad), "per_domain": {}, "cell_means": {}}
        for d in self.domains:
            s["per_domain"][d] = {"r": {g: {"tokens": pearson(self.tight[ix], tok[ix]), "log_ppl": pearson(self.tight[ix], lpp[ix])}
                                        for (dd, g), ix in self.dom_scopes.items() if dd == d},
                                  "mean_tokens": {c: float(tok[self.cell_idx[(d, c)]].mean()) for c in CELLS},
                                  "mean_logppl": {c: float(lpp[self.cell_idx[(d, c)]].mean()) for c in CELLS},
                                  "token_spread": spread[d]}
        for c in CELLS:
            ix = np.where(self.cell == c)[0]
            s["cell_means"][c] = {"n": int(len(ix)), "mean_tokens": float(tok[ix].mean()), "sd_tokens": float(tok[ix].std(ddof=1)),
                                  "mean_logppl": float(lpp[ix].mean()), "sd_logppl": float(lpp[ix].std(ddof=1))}
        return s


def search(P, restarts, rng, log):
    best_choice, best_obj = None, float("inf")
    for rs in range(restarts):
        choice = [rng.randrange(len(cs)) for cs in P.cands]
        obj = P.objective(choice)
        improved, sweeps = True, 0
        while improved and sweeps < 30:
            improved = False; sweeps += 1
            order = list(range(P.n)); rng.shuffle(order)
            for i in order:
                cur = choice[i]
                for c in range(len(P.cands[i])):
                    if c == cur:
                        continue
                    choice[i] = c
                    o = P.objective(choice)
                    if o < obj - 1e-12:
                        obj, cur, improved = o, c, True
                choice[i] = cur
        if obj < best_obj:
            best_obj, best_choice = obj, list(choice)
            st = P.stats(choice)
            log(f"restart {rs}: obj={obj:.4f} " + " ".join(f"{s}:tok{v['tokens']:+.3f}/lpp{v['log_ppl']:+.3f}" for s, v in st["r"].items())
                + f" maxspread={max(st['token_spread'].values()):.3f} sweeps={sweeps}")
    return best_choice, best_obj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", default=str(HERE / "pool_measured.jsonl"))
    ap.add_argument("--raw-pool", default=str(HERE / "pool.jsonl"))
    ap.add_argument("--out", default=str(HERE / "stimuli.jsonl"))
    ap.add_argument("--manifest", default=str(HERE / "manifest.json"))
    ap.add_argument("--report", default=str(HERE / "selection_report.md"))
    ap.add_argument("--restarts", type=int, default=40)
    ap.add_argument("--codes", default=str(HERE / "address_codes.jsonl"))
    args = ap.parse_args()

    all_rows = [json.loads(l) for l in open(args.pool) if l.strip()]
    codes = {}
    for l in open(args.codes):
        if l.strip():
            c = json.loads(l); codes[c["cand_id"]] = c
    missing = [r["cand_id"] for r in all_rows if r["cand_id"] not in codes
               or codes[r["cand_id"]].get("text_sha256") != sha256(r["prompt_text"])]
    assert not missing, f"{len(missing)} pool rows lack an address code for their current text, e.g. {missing[:5]}"
    rows = []
    drop = defaultdict(lambda: {"n": 0, "dropped": 0, "regex_flagged": 0, "llm_not_none": 0})
    for r in all_rows:
        c = codes[r["cand_id"]]
        ok = c["address_regex"] == "none" and c["address_llm"] == "none"
        d = drop[r["cell"]]; d["n"] += 1
        d["regex_flagged"] += 0 if c["address_regex"] == "none" else 1
        d["llm_not_none"] += 0 if c["address_llm"] == "none" else 1
        if ok:
            r["address_regex"] = c["address_regex"]; r["address_llm"] = c["address_llm"]
            r["attrib_count"] = c.get("attrib_count"); r["self_ref_count"] = c.get("self_ref_count")
            r["second_person_count"] = c.get("second_person_count")
            rows.append(r)
        else:
            d["dropped"] += 1
    drop = dict(drop)
    slots = defaultdict(int)
    for r in rows:
        slots[(r["topic_id"], r["cell"])] += 1
    print("address filter:", json.dumps(drop))
    P = Problem(rows)
    print(f"{len(rows)} candidates, {P.n} cells, domains={P.domains}")
    assert P.n == 384, f"expected 384 topic x cell slots with >= 1 admissible candidate, got {P.n}; enlarge the pool"
    rng = random.Random(SEED)
    logs = []
    def log(m):
        logs.append(m); print(m, flush=True)
    t0 = time.time()
    choice, obj = search(P, args.restarts, rng, log)
    st = P.stats(choice)
    log(f"search done in {time.time()-t0:.0f}s, objective={obj:.4f}")

    stim = []
    for i, (k, c) in enumerate(zip(P.keys, choice)):
        r = P.cands[i][c]
        stim.append({"id": f"{r['topic_id']}_{r['cell']}", "domain": r["domain"], "topic_id": r["topic_id"],
                     "register": r["register"], "tightness": r["tightness"], "cell": r["cell"], "prompt": r["prompt_text"],
                     "tokens": r["tokens"], "log_ppl": r["log_ppl"], "cand_id": r["cand_id"], "source": r.get("source", "v2_gen"),
                     "address_regex": r["address_regex"], "address_llm": r["address_llm"], "attrib_count": r["attrib_count"],
                     "self_ref_count": r["self_ref_count"], "second_person_count": r["second_person_count"]})
    with open(args.out, "w") as f:
        for s in stim:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    r_ok = all(abs(v) < R_TARGET for pair in st["r"].values() for v in pair.values())
    spread_ok = all(s < TOK_TOL for s in st["token_spread"].values())
    addr_ok = all(x["address_regex"] == "none" and x["address_llm"] == "none" for x in stim)
    passed = r_ok and spread_ok and addr_ok
    gen_models = sorted({r["gen_model"] for r in rows})
    endpoints = sorted({r["gen_meta"].get("endpoint", "?") for r in rows})
    tok_in_band = sum(1 for s in stim if 130 <= s["tokens"] <= 200)
    manifest = {
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "design": "v3 2x2 register x tightness, address = none in all cells",
        "n_stimuli": len(stim), "n_pool": len(all_rows), "n_pool_admissible": len(rows), "cells": CELLS,
        "address_filter": drop, "address_rule": "address_regex == none AND address_llm == none (coding-scheme.md ADDRESS)",
        "address_coder": {"llm_model": next(iter(codes.values())).get("llm_model"), "llm_temperature": next(iter(codes.values())).get("llm_temperature"),
                          "scheme_sha256": next(iter(codes.values())).get("scheme_sha256"), "regex": "address_regex.py"},
        "sha256_address_codes_jsonl": sha256(Path(args.codes).read_text()),
        "sha256_address_regex_py": sha256((HERE / "address_regex.py").read_text()),
        "selected_all_address_none": addr_ok,
        "admissible_per_slot_min": int(min(slots.values())), "admissible_per_slot_mean": float(np.mean(list(slots.values()))),
        "generator_model": gen_models, "generator_endpoint": endpoints,
        "generator_temperature": sorted({r["gen_meta"]["temperature"] for r in rows}),
        "generator_max_tokens": sorted({r["gen_meta"].get("max_tokens") for r in rows}),
        "pool_sources": {s: sum(1 for r in all_rows if r.get("source") == s) for s in ["v1_reuse", "v2_gen", "v3_gen"]},
        "admissible_sources": {s: sum(1 for r in rows if r.get("source") == s) for s in ["v1_reuse", "v2_gen", "v3_gen"]},
        "selected_sources": {s: sum(1 for x in stim if x["source"] == s) for s in ["v1_reuse", "v2_gen", "v3_gen"]},
        "meta_prompt_sha256": {c: sha256((HERE / "meta_prompts" / f"{c}.txt").read_text()) for c in CELLS},
        "token_band": [130, 200], "selected_in_token_band": tok_in_band,
        "selection_seed": SEED, "selection_restarts": args.restarts, "selection_objective": obj,
        "selection_r": st["r"], "per_domain": st["per_domain"], "cell_means": st["cell_means"],
        "token_spread": st["token_spread"], "r_target": R_TARGET, "spread_target": TOK_TOL,
        "decorrelation_pass": r_ok and spread_ok, "decorrelation_pass_r": r_ok, "decorrelation_pass_spread": spread_ok,
        "selection_pass_all_gates": passed,
        "measure_meta": rows[0].get("measure_meta"),
        "sha256_stimuli_jsonl": sha256(Path(args.out).read_text()),
        "sha256_pool_jsonl": sha256(Path(args.raw_pool).read_text()) if Path(args.raw_pool).exists() else None,
        "sha256_pool_measured_jsonl": sha256(Path(args.pool).read_text()),
        "sha256_topics_jsonl": sha256((HERE / "topics.jsonl").read_text()),
        "sha256_rubric": sha256((HERE / "tightness-rubric.md").read_text()),
        "prompts": {s["id"]: {"sha256": sha256(s["prompt"]), "cand_id": s["cand_id"], "source": s["source"]} for s in stim},
    }
    Path(args.manifest).write_text(json.dumps(manifest, indent=1, ensure_ascii=False))

    L = ["# Selection report (v3, 2x2 register x tightness, address = none)\n",
         f"Generated {manifest['created']}. Pool: {len(all_rows)} candidates ({manifest['pool_sources']}; generators {', '.join(gen_models)}; endpoints {', '.join(endpoints)}). "
         f"Address filter (both coders `none`): {len(rows)} admissible; dropped per cell: " + "; ".join(f"{c} {drop[c]['dropped']}/{drop[c]['n']}" for c in CELLS) +
         f". Admissible candidates per topic × cell slot: min {manifest['admissible_per_slot_min']}, mean {manifest['admissible_per_slot_mean']:.2f}. "
         f"**Address gate (all 384 selected coded none by both): {'PASS' if addr_ok else 'FAIL'}.** "
         f"Selected {len(stim)} stimuli ({manifest['selected_sources']}), seed {SEED}, {args.restarts} random restarts of greedy coordinate descent. "
         f"Selected items inside the 130–200 token band: {tok_in_band}/{len(stim)}; len_ok violations: {st['len_ok_violations']}.\n",
         "## Decorrelation\n",
         f"Targets: |r(tightness, tokens)| < {R_TARGET} and |r(tightness, log-ppl)| < {R_TARGET} overall and within each register; "
         f"per-domain mean token spread across the four cells < {TOK_TOL:.0%}. **r gate: {'PASS' if r_ok else 'FAIL'}. Spread gate: {'PASS' if spread_ok else 'FAIL'}. Overall: {'PASS' if passed else 'FAIL'}**\n",
         "| scope | n | r(tightness, tokens) | r(tightness, log-ppl) |", "|---|---|---|---|"]
    for s, ix in P.scopes.items():
        L.append(f"| {s} | {len(ix)} | {st['r'][s]['tokens']:+.3f} | {st['r'][s]['log_ppl']:+.3f} |")
    L += ["\n### Per domain\n", "| domain | r tok (all) | r lpp (all) | r tok (verse) | r lpp (verse) | r tok (prose) | r lpp (prose) | token spread |", "|---|---|---|---|---|---|---|---|"]
    for d, pd in st["per_domain"].items():
        r = pd["r"]
        L.append(f"| {d} | {r['all']['tokens']:+.3f} | {r['all']['log_ppl']:+.3f} | {r['verse']['tokens']:+.3f} | {r['verse']['log_ppl']:+.3f} | "
                 f"{r['prose']['tokens']:+.3f} | {r['prose']['log_ppl']:+.3f} | {pd['token_spread']:.1%} |")
    L += ["\n### Cell means (all domains)\n", "| cell | n | mean tokens (SD) | mean log-ppl (SD) |", "|---|---|---|---|"]
    for c in CELLS:
        m = st["cell_means"][c]
        L.append(f"| {c} | {m['n']} | {m['mean_tokens']:.1f} ({m['sd_tokens']:.1f}) | {m['mean_logppl']:.3f} ({m['sd_logppl']:.3f}) |")
    L += ["\n### Per-domain cell means: tokens / log-ppl\n", "| domain | " + " | ".join(f"{c} tok" for c in CELLS) + " | " + " | ".join(f"{c} lpp" for c in CELLS) + " |",
          "|---|" + "---|" * 8]
    for d, pd in st["per_domain"].items():
        L.append(f"| {d} | " + " | ".join(f"{pd['mean_tokens'][c]:.1f}" for c in CELLS) + " | " + " | ".join(f"{pd['mean_logppl'][c]:.3f}" for c in CELLS) + " |")
    all_t = np.array([1.0 if r["tightness"] == "tight" else 0.0 for r in rows])
    all_tok = [r["tokens"] for r in rows]; all_lpp = [r["log_ppl"] for r in rows]
    pool_r = {"all": (pearson(all_t, all_tok), pearson(all_t, all_lpp))}
    for g in REGISTERS:
        ix = [i for i, r in enumerate(rows) if r["register"] == g]
        pool_r[g] = (pearson(all_t[ix], np.array(all_tok)[ix]), pearson(all_t[ix], np.array(all_lpp)[ix]))
    L.append("\nFor comparison, over the full pool before selection: " + "; ".join(f"{s}: r_tok = {a:+.3f}, r_lpp = {b:+.3f}" for s, (a, b) in pool_r.items())
             + f". Pool rows outside the 130–200 token band: {sum(1 for r in rows if not (130 <= r['tokens'] <= 200))}.\n")
    L += ["### Search log\n", "```\n" + "\n".join(logs) + "\n```\n"]
    Path(args.report).write_text("\n".join(L))
    print(json.dumps({"r": st["r"], "token_spread": st["token_spread"], "cell_means": st["cell_means"]}, indent=1))
    print("pass:", passed, "r_ok:", r_ok, "spread_ok:", spread_ok, "addr_ok:", addr_ok)


if __name__ == "__main__":
    main()
