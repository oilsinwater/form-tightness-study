#!/usr/bin/env python3
"""select_stimuli.py — deterministic selection of 1 candidate per topic x level (288)
from pool_measured.jsonl, minimising |r(level, log_ppl)| and |r(level, tokens)| over the
full set and within each domain, subject to per-domain mean tokens differing across
levels by < 10 % (max/min - 1).

Search: greedy coordinate descent with random restarts (seed 20261030). Candidates with
len_ok=false are penalised (not forbidden) so a cell is never left empty.

Writes stimuli.jsonl, manifest.json, and the decorrelation section of selection_report.md.
"""
import argparse, hashlib, json, random, time
from collections import defaultdict
from pathlib import Path
import numpy as np

SEED = 20261030
LEVELS = ["T1", "T2", "T3"]
LVL_NUM = {"T1": 1, "T2": 2, "T3": 3}
R_TARGET = 0.10
TOK_TOL = 0.10
HERE = Path(__file__).resolve().parent


def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if x.std() == 0 or y.std() == 0:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


class Problem:
    def __init__(self, rows):
        cells = defaultdict(list)
        for r in rows:
            cells[(r["topic_id"], r["level"])].append(r)
        self.keys = sorted(cells)
        self.cands = [cells[k] for k in self.keys]
        self.n = len(self.keys)
        self.level = np.array([LVL_NUM[k[1]] for k in self.keys], float)
        self.domain = np.array([cells[k][0]["domain"] for k in self.keys])
        self.domains = sorted(set(self.domain))
        self.dom_idx = {d: np.where(self.domain == d)[0] for d in self.domains}
        self.lvl_idx = {d: {lv: np.where((self.domain == d) & (self.level == LVL_NUM[lv]))[0]
                            for lv in LEVELS} for d in self.domains}
        # per-cell candidate feature arrays
        self.tok = [np.array([c["tokens"] for c in cs], float) for cs in self.cands]
        self.lpp = [np.array([c["log_ppl"] for c in cs], float) for cs in self.cands]
        self.bad = [np.array([0.0 if c["gen_meta"].get("len_ok", True) else 1.0 for c in cs]) for cs in self.cands]

    def features(self, choice):
        tok = np.array([self.tok[i][c] for i, c in enumerate(choice)])
        lpp = np.array([self.lpp[i][c] for i, c in enumerate(choice)])
        bad = sum(self.bad[i][c] for i, c in enumerate(choice))
        return tok, lpp, bad

    def stats(self, choice):
        tok, lpp, bad = self.features(choice)
        s = {"r_all_tokens": pearson(self.level, tok), "r_all_logppl": pearson(self.level, lpp),
             "per_domain": {}, "len_ok_violations": int(bad)}
        for d in self.domains:
            ix = self.dom_idx[d]
            means = {lv: float(tok[self.lvl_idx[d][lv]].mean()) for lv in LEVELS}
            lmeans = {lv: float(lpp[self.lvl_idx[d][lv]].mean()) for lv in LEVELS}
            spread = max(means.values()) / min(means.values()) - 1
            s["per_domain"][d] = {"r_tokens": pearson(self.level[ix], tok[ix]),
                                  "r_logppl": pearson(self.level[ix], lpp[ix]),
                                  "mean_tokens": means, "mean_logppl": lmeans,
                                  "token_spread": spread}
        return s

    def objective(self, choice):
        s = self.stats(choice)
        obj = abs(s["r_all_tokens"]) + abs(s["r_all_logppl"])
        for d in self.domains:
            pd = s["per_domain"][d]
            obj += 0.5 * (abs(pd["r_tokens"]) + abs(pd["r_logppl"]))
            obj += 10.0 * max(0.0, pd["token_spread"] - TOK_TOL)
        obj += 0.05 * s["len_ok_violations"]
        return obj, s


def search(P, restarts, rng, log):
    best_choice, best_obj, best_stats = None, float("inf"), None
    for rs in range(restarts):
        choice = [rng.randrange(len(cs)) for cs in P.cands]
        obj, _ = P.objective(choice)
        improved = True
        sweeps = 0
        while improved and sweeps < 30:
            improved = False
            sweeps += 1
            order = list(range(P.n)); rng.shuffle(order)
            for i in order:
                cur = choice[i]
                for c in range(len(P.cands[i])):
                    if c == cur:
                        continue
                    choice[i] = c
                    o, _ = P.objective(choice)
                    if o < obj - 1e-12:
                        obj, cur, improved = o, c, True
                choice[i] = cur
        if obj < best_obj:
            best_obj, best_choice = obj, list(choice)
            best_stats = P.stats(choice)
            log(f"restart {rs}: obj={obj:.4f} r_tok={best_stats['r_all_tokens']:+.3f} "
                f"r_lpp={best_stats['r_all_logppl']:+.3f} sweeps={sweeps}")
    return best_choice, best_obj, best_stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", default=str(HERE / "pool_measured.jsonl"))
    ap.add_argument("--raw-pool", default=str(HERE / "pool.jsonl"))
    ap.add_argument("--out", default=str(HERE / "stimuli.jsonl"))
    ap.add_argument("--manifest", default=str(HERE / "manifest.json"))
    ap.add_argument("--report", default=str(HERE / "selection_report.md"))
    ap.add_argument("--restarts", type=int, default=40)
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.pool) if l.strip()]
    P = Problem(rows)
    print(f"{len(rows)} candidates, {P.n} cells, domains={P.domains}")
    assert P.n == 288, f"expected 288 cells, got {P.n}"
    rng = random.Random(SEED)
    logs = []
    def log(m):
        logs.append(m); print(m, flush=True)
    t0 = time.time()
    choice, obj, st = search(P, args.restarts, rng, log)
    log(f"search done in {time.time()-t0:.0f}s, objective={obj:.4f}")

    # write stimuli.jsonl
    stim = []
    for i, (k, c) in enumerate(zip(P.keys, choice)):
        r = P.cands[i][c]
        stim.append({"id": f"{r['topic_id']}_{r['level']}", "domain": r["domain"], "topic_id": r["topic_id"],
                     "tightness_level": r["level"], "prompt": r["prompt_text"], "tokens": r["tokens"],
                     "log_ppl": r["log_ppl"], "cand_id": r["cand_id"]})
    with open(args.out, "w") as f:
        for s in stim:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    # overall per-level means
    lvl_means = {}
    for lv in LEVELS:
        sub = [s for s in stim if s["tightness_level"] == lv]
        lvl_means[lv] = {"n": len(sub), "mean_tokens": float(np.mean([s["tokens"] for s in sub])),
                         "sd_tokens": float(np.std([s["tokens"] for s in sub], ddof=1)),
                         "mean_logppl": float(np.mean([s["log_ppl"] for s in sub])),
                         "sd_logppl": float(np.std([s["log_ppl"] for s in stim if s["tightness_level"] == lv], ddof=1))}

    passed = (abs(st["r_all_tokens"]) < R_TARGET and abs(st["r_all_logppl"]) < R_TARGET and
              all(abs(pd["r_tokens"]) < R_TARGET and abs(pd["r_logppl"]) < R_TARGET and pd["token_spread"] < TOK_TOL
                  for pd in st["per_domain"].values()))

    gen_models = sorted({r["gen_model"] for r in rows})
    endpoints = sorted({r["gen_meta"].get("endpoint", "?") for r in rows})
    manifest = {
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "n_stimuli": len(stim), "n_pool": len(rows),
        "generator_model": gen_models, "generator_endpoint": endpoints,
        "generator_temperature": sorted({r["gen_meta"]["temperature"] for r in rows}),
        "meta_prompt_sha256": {lv: sha256((HERE / "meta_prompts" / f"{lv}.txt").read_text()) for lv in LEVELS},
        "selection_seed": SEED, "selection_restarts": args.restarts, "selection_objective": obj,
        "selection_r": {"all": {"tokens": st["r_all_tokens"], "log_ppl": st["r_all_logppl"]},
                        "per_domain": {d: {"tokens": pd["r_tokens"], "log_ppl": pd["r_logppl"],
                                           "token_spread": pd["token_spread"]} for d, pd in st["per_domain"].items()}},
        "decorrelation_pass": passed,
        "measure_meta": rows[0].get("measure_meta"),
        "sha256_stimuli_jsonl": sha256(Path(args.out).read_text()),
        "sha256_pool_jsonl": sha256(Path(args.raw_pool).read_text()) if Path(args.raw_pool).exists() else None,
        "sha256_pool_measured_jsonl": sha256(Path(args.pool).read_text()),
        "sha256_topics_jsonl": sha256((HERE / "topics.jsonl").read_text()),
        "sha256_rubric": sha256((HERE / "tightness-rubric.md").read_text()),
        "prompts": {s["id"]: {"sha256": sha256(s["prompt"]), "cand_id": s["cand_id"]} for s in stim},
    }
    Path(args.manifest).write_text(json.dumps(manifest, indent=1, ensure_ascii=False))

    # report (decorrelation section; rate_tightness.py appends the manipulation check)
    L = []
    L.append("# Selection report\n")
    L.append(f"Generated {manifest['created']}. Pool: {len(rows)} candidates ({len(gen_models)} generator model(s): {', '.join(gen_models)}; endpoint {', '.join(endpoints)}). "
             f"Selected {len(stim)} stimuli, seed {SEED}, {args.restarts} random restarts of greedy coordinate descent.\n")
    L.append("## Decorrelation\n")
    L.append(f"Targets: |r| < {R_TARGET} overall and per domain; per-domain mean token spread across levels < {TOK_TOL:.0%}. "
             f"**Pass: {passed}**\n")
    L.append("| scope | r(level, tokens) | r(level, log-ppl) | token spread |")
    L.append("|---|---|---|---|")
    L.append(f"| all (n={len(stim)}) | {st['r_all_tokens']:+.3f} | {st['r_all_logppl']:+.3f} | — |")
    for d, pd in st["per_domain"].items():
        L.append(f"| {d} | {pd['r_tokens']:+.3f} | {pd['r_logppl']:+.3f} | {pd['token_spread']:.1%} |")
    L.append("\n### Per-level means (all domains)\n")
    L.append("| level | n | mean tokens (SD) | mean log-ppl (SD) |")
    L.append("|---|---|---|---|")
    for lv in LEVELS:
        m = lvl_means[lv]
        L.append(f"| {lv} | {m['n']} | {m['mean_tokens']:.1f} ({m['sd_tokens']:.1f}) | {m['mean_logppl']:.3f} ({m['sd_logppl']:.3f}) |")
    L.append("\n### Per-domain, per-level mean tokens / log-ppl\n")
    L.append("| domain | T1 tok | T2 tok | T3 tok | T1 lpp | T2 lpp | T3 lpp |")
    L.append("|---|---|---|---|---|---|---|")
    for d, pd in st["per_domain"].items():
        mt, ml = pd["mean_tokens"], pd["mean_logppl"]
        L.append(f"| {d} | {mt['T1']:.1f} | {mt['T2']:.1f} | {mt['T3']:.1f} | {ml['T1']:.3f} | {ml['T2']:.3f} | {ml['T3']:.3f} |")
    # pool-level (pre-selection) correlations for comparison
    all_tok = [r["tokens"] for r in rows]; all_lpp = [r["log_ppl"] for r in rows]; all_lv = [LVL_NUM[r["level"]] for r in rows]
    L.append(f"\nFor comparison, over the full pool before selection: r(level, tokens) = {pearson(all_lv, all_tok):+.3f}, "
             f"r(level, log-ppl) = {pearson(all_lv, all_lpp):+.3f}. Candidates outside the 90–160 word band in pool: "
             f"{sum(0 if r['gen_meta'].get('len_ok', True) else 1 for r in rows)}; selected: {st['len_ok_violations']}.\n")
    L.append("### Search log\n")
    L.append("```\n" + "\n".join(logs) + "\n```\n")
    Path(args.report).write_text("\n".join(L))
    print(json.dumps(manifest["selection_r"], indent=1))
    print("pass:", passed)


if __name__ == "__main__":
    main()
