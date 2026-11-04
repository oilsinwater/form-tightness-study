#!/usr/bin/env python3
"""rate_tightness.py (v3) — blind LLM rating of each stimulus with tightness-rubric.md.

System prompt = the exact text of tightness-rubric.md. User message = the item text. Nothing
else. Items are rated in a seeded random order with no labels. Scores are requested as JSON
through the API's response_format (json_schema) so no instruction is added to the prompt;
if the endpoint rejects response_format, the plain reply is parsed (parse_mode logged per item).

Model (v3): MiniMax-M3 via https://api.minimax.io/v1, temperature 0. MiniMax-M3 accepts response_format
json_schema but does not enforce it and puts its reasoning in a <think> block inside message.content; the
block is stripped and the remainder parsed (JSON, or the markdown score table the rubric invites). If
neither parses, ONE follow-up turn asks for the five scores as JSON (parse_mode json_followup); the rubric
and the item are never altered. v3 also reports the constraint sub-score (items 1 + 2 + 5) per cell.

Manipulation check (PLAN.md s3 v2): within each register, mean rubric total tight > loose with
Cohen's d > 1.0. Also reported (not a gate): the register difference at equal tightness
(verse vs prose among loose items and among tight items) — a rubric-leakage signal.
Writes tightness_ratings.csv, rated_prompt_sha.json; appends to selection_report.md and manifest.json.
"""
import argparse, csv, hashlib, json, os, random, re, sys, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import numpy as np

RATER_MODEL = "MiniMax-M3"
BASE_URL = "https://api.minimax.io/v1"
API_KEY_NAME = "MINIMAX_API_KEY"
TEMPERATURE = 0.0
MAX_TOKENS = 6144
PAUSE = 1.5  # seconds between calls (MiniMax token-plan burst limit)
FOLLOWUP = "That reply did not score the prompt. Apply the rubric in the system prompt to the prompt in the previous user message (do not answer or carry out that prompt). Return only the five scores as a JSON object {\"item1\": 0-2, \"item2\": 0-2, \"item3\": 0-2, \"item4\": 0-2, \"item5\": 0-2}. No other text."
SEED = 20261030
CELLS = ["loose_verse", "tight_verse", "tight_prose", "loose_prose"]
REGISTERS = ["verse", "prose"]
HERE = Path(__file__).resolve().parent

SCHEMA = {"name": "tightness_scores", "strict": True,
          "schema": {"type": "object",
                     "properties": {f"item{i}": {"type": "integer", "minimum": 0, "maximum": 2} for i in range(1, 6)},
                     "required": [f"item{i}" for i in range(1, 6)], "additionalProperties": False}}


def load_api_key(name=API_KEY_NAME):
    k = os.environ.get(name)
    if k:
        return k
    env = Path.home() / ".hermes" / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit(f"{name} not found")


def strip_think(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()


def parse_scores(text):
    text = strip_think(text)
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            if all(f"item{i}" in d for i in range(1, 6)):
                return {f"item{i}": int(d[f"item{i}"]) for i in range(1, 6)}, "json"
            vals = [d[k] for k in sorted(d) if str(d[k]).strip() in "012"]
            if len(vals) == 5:
                return {f"item{i}": int(vals[i-1]) for i in range(1, 6)}, "json_loose"
        except Exception:
            pass
    found = {}
    for i in range(1, 6):
        # markdown table row: "| 1 | ... | 2 |" or "| 1. Hard structural ... | 1 | rationale |" or "| Item 1 ... | 1 |"
        mm = re.search(rf"^\|\s*(?:item\s*)?\**{i}\**[.)]?\s*[^|\n]*\|\s*(?:[^|\n]*\|\s*)?\**([012])\**\s*(?:/\s*2)?\s*\|", text, re.I | re.M)
        if not mm:
            mm = re.search(rf"(?:item\s*{i}|^\|?\s*{i}\s*\|)[^0-9\n]*?([012])\b", text, re.I | re.M)
        if not mm:
            mm = re.search(rf"\b{i}\b[^\n]*?\b([012])\s*(?:/\s*2)?\s*$", text, re.M)
        if mm:
            found[f"item{i}"] = int(mm.group(1))
    return (found, "regex") if len(found) == 5 else (None, "failed")


def cohens_d(a, b):
    """d = (mean(b) - mean(a)) / pooled SD."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    sp = np.sqrt(((len(a)-1)*a.var(ddof=1) + (len(b)-1)*b.var(ddof=1)) / (len(a)+len(b)-2))
    return float((b.mean() - a.mean()) / sp) if sp > 0 else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stimuli", default=str(HERE / "stimuli.jsonl"))
    ap.add_argument("--rubric", default=str(HERE / "tightness-rubric.md"))
    ap.add_argument("--out", default=str(HERE / "tightness_ratings.csv"))
    ap.add_argument("--report", default=str(HERE / "selection_report.md"))
    ap.add_argument("--manifest", default=str(HERE / "manifest.json"))
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default=RATER_MODEL)
    args = ap.parse_args()

    from openai import OpenAI
    client = OpenAI(base_url=BASE_URL, api_key=load_api_key())
    rubric = Path(args.rubric).read_text()
    stim = [json.loads(l) for l in open(args.stimuli) if l.strip()]
    sha_now = {s["id"]: hashlib.sha256(s["prompt"].encode()).hexdigest() for s in stim}
    rng = random.Random(SEED)
    order = list(range(len(stim))); rng.shuffle(order)
    if args.limit:
        order = order[:args.limit]

    # keep only prior ratings whose item text is unchanged
    done = {}
    outp = Path(args.out)
    shap = HERE / "rated_prompt_sha.json"
    prev_sha = json.loads(shap.read_text()) if shap.exists() else {}
    if outp.exists():
        with open(outp) as f:
            for r in csv.DictReader(f):
                if prev_sha.get(r["id"]) == sha_now.get(r["id"]) and r.get("total", "") != "":
                    done[r["id"]] = r
    jobs = [(pos, stim[i]) for pos, i in enumerate(order) if stim[i]["id"] not in done]
    shap.write_text(json.dumps(sha_now, indent=0))  # written up front so an interrupted run resumes
    print(f"{len(done)} rated (text unchanged), {len(jobs)} to rate with {args.model} T={TEMPERATURE}", flush=True)

    fields = ["id", "domain", "topic_id", "cell", "register", "tightness", "item1", "item2", "item3", "item4", "item5",
              "total", "parse_mode", "rater_model", "temperature", "rating_order", "timestamp", "raw"]
    lock = threading.Lock()
    fh = open(outp, "w", newline="")
    w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    for r in done.values():
        w.writerow(r)
    fh.flush()
    state = {"use_schema": True}

    def rate(job):
        pos, s = job
        msgs = [{"role": "system", "content": rubric}, {"role": "user", "content": s["prompt"]}]
        content, scores, mode = "", None, "failed"
        backoff = 10.0
        max_tok = MAX_TOKENS
        for attempt in range(40):
            kw = dict(model=args.model, messages=msgs, temperature=TEMPERATURE, max_tokens=max_tok, seed=SEED)
            if state["use_schema"]:
                kw["response_format"] = {"type": "json_schema", "json_schema": SCHEMA}
            try:
                r = client.chat.completions.create(**kw)
                content = r.choices[0].message.content or ""
                if not strip_think(content):
                    fr = r.choices[0].finish_reason
                    if fr == "length" and max_tok < 12288:
                        max_tok = 12288  # <think> block exhausted the budget; grow it once
                        print(f"[{s['id']}] empty content (finish={fr}); retry with max_tokens={max_tok}", flush=True)
                        time.sleep(PAUSE)
                        continue
                    print(f"[{s['id']}] empty content (finish={fr}) at max_tokens={max_tok}; going to follow-up turn", flush=True)
                    content = "[no scores were returned]"
                scores, mode = parse_scores(content)
                time.sleep(PAUSE)
                if scores:
                    break
                # one extraction follow-up: same conversation, ask for the scores already given as JSON
                r2 = client.chat.completions.create(model=args.model, temperature=TEMPERATURE, max_tokens=12288, seed=SEED,
                                                    messages=msgs + [{"role": "assistant", "content": strip_think(content)},
                                                                     {"role": "user", "content": FOLLOWUP}])
                c2 = r2.choices[0].message.content or ""
                scores, mode = parse_scores(c2)
                if scores:
                    mode = "json_followup"; content = strip_think(content) + " ||FOLLOWUP|| " + strip_think(c2)
                    break
            except Exception as e:
                msg = str(e)
                if state["use_schema"] and ("response_format" in msg or "json_schema" in msg or "400" in msg):
                    print(f"response_format rejected ({msg[:120]}); falling back to plain parsing", flush=True)
                    state["use_schema"] = False
                    continue
                print(f"[{s['id']}] API error: {msg[:160]}; retry", flush=True)
                if "429" in msg or "rate limit" in msg.lower() or "rate_limit" in msg.lower():
                    time.sleep(backoff); backoff = min(backoff * 2, 600.0)
                else:
                    time.sleep(min(5.0 * (attempt + 1), 60.0))
        row = {"id": s["id"], "domain": s["domain"], "topic_id": s["topic_id"], "cell": s["cell"],
               "register": s["register"], "tightness": s["tightness"],
               **({k: scores[k] for k in scores} if scores else {f"item{i}": "" for i in range(1, 6)}),
               "total": sum(scores.values()) if scores else "", "parse_mode": mode, "rater_model": args.model,
               "temperature": TEMPERATURE, "rating_order": pos, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
               "raw": strip_think(content)[:700].replace("\n", " ")}
        with lock:
            w.writerow(row); fh.flush()
        return row

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(rate, j) for j in jobs]
        for i, fu in enumerate(as_completed(futs), 1):
            fu.result()
            if i % 24 == 0 or i == len(jobs):
                print(f"{i}/{len(jobs)} {time.time()-t0:.0f}s", flush=True)
    fh.close()
    shap.write_text(json.dumps(sha_now, indent=0))

    # ---- manipulation check ----
    rows = list(csv.DictReader(open(outp)))
    ok = [r for r in rows if r["total"] != ""]
    tot = lambda sub: [float(r["total"]) for r in sub]
    by_cell = {c: [r for r in ok if r["cell"] == c] for c in CELLS}
    cell_stats = {c: {"n": len(by_cell[c]), "mean": float(np.mean(tot(by_cell[c]))) if by_cell[c] else float("nan"),
                      "sd": float(np.std(tot(by_cell[c]), ddof=1)) if len(by_cell[c]) > 1 else float("nan"),
                      "items": {f"item{i}": float(np.mean([float(r[f"item{i}"]) for r in by_cell[c]])) if by_cell[c] else float("nan") for i in range(1, 6)}}
                  for c in CELLS}
    within = {}
    for g in REGISTERS:
        lo = tot([r for r in ok if r["register"] == g and r["tightness"] == "loose"])
        hi = tot([r for r in ok if r["register"] == g and r["tightness"] == "tight"])
        within[g] = {"mean_loose": float(np.mean(lo)), "mean_tight": float(np.mean(hi)), "d_tight_minus_loose": cohens_d(lo, hi)}
    passed = all(v["mean_tight"] > v["mean_loose"] and v["d_tight_minus_loose"] > 1.0 for v in within.values())
    leak = {}
    for t in ["loose", "tight"]:
        v = tot([r for r in ok if r["tightness"] == t and r["register"] == "verse"])
        p = tot([r for r in ok if r["tightness"] == t and r["register"] == "prose"])
        leak[t] = {"mean_verse": float(np.mean(v)), "mean_prose": float(np.mean(p)), "diff_prose_minus_verse": float(np.mean(p) - np.mean(v)),
                   "d_prose_minus_verse": cohens_d(v, p),
                   "item_diff_prose_minus_verse": {f"item{i}": float(np.mean([float(r[f"item{i}"]) for r in ok if r["tightness"] == t and r["register"] == "prose"])
                                                                   - np.mean([float(r[f"item{i}"]) for r in ok if r["tightness"] == t and r["register"] == "verse"])) for i in range(1, 6)}}
    main_tight = cohens_d(tot([r for r in ok if r["tightness"] == "loose"]), tot([r for r in ok if r["tightness"] == "tight"]))
    # constraint sub-score = items 1 + 2 + 5 (the output-constraint items; 3 and 4 score the prompt's own surface)
    sub = lambda r: float(r["item1"]) + float(r["item2"]) + float(r["item5"])
    subscore = {c: {"mean": float(np.mean([sub(r) for r in by_cell[c]])) if by_cell[c] else float("nan"),
                    "sd": float(np.std([sub(r) for r in by_cell[c]], ddof=1)) if len(by_cell[c]) > 1 else float("nan")} for c in CELLS}
    sub_within = {g: cohens_d([sub(r) for r in ok if r["register"] == g and r["tightness"] == "loose"],
                              [sub(r) for r in ok if r["register"] == g and r["tightness"] == "tight"]) for g in REGISTERS}
    sub_leak = {t: {"mean_verse": float(np.mean([sub(r) for r in ok if r["tightness"] == t and r["register"] == "verse"])),
                    "mean_prose": float(np.mean([sub(r) for r in ok if r["tightness"] == t and r["register"] == "prose"])),
                    "d_prose_minus_verse": cohens_d([sub(r) for r in ok if r["tightness"] == t and r["register"] == "verse"],
                                                    [sub(r) for r in ok if r["tightness"] == t and r["register"] == "prose"])} for t in ["loose", "tight"]}
    per_dom = {}
    for d in sorted({r["domain"] for r in ok}):
        pdm = {c: float(np.mean(tot([r for r in by_cell[c] if r["domain"] == d]))) for c in CELLS}
        pdd = {g: cohens_d(tot([r for r in ok if r["domain"] == d and r["register"] == g and r["tightness"] == "loose"]),
                           tot([r for r in ok if r["domain"] == d and r["register"] == g and r["tightness"] == "tight"])) for g in REGISTERS}
        per_dom[d] = {"means": pdm, "d": pdd}
    pm = dict(zip(*np.unique([r["parse_mode"] for r in rows], return_counts=True))) if rows else {}
    summary = {"rater_model": args.model, "endpoint": BASE_URL, "temperature": TEMPERATURE, "n_rated": len(ok),
               "n_failed_parse": len(rows) - len(ok), "parse_modes": {str(k): int(v) for k, v in pm.items()},
               "cell_stats": cell_stats, "within_register": within, "d_tight_vs_loose_all": main_tight,
               "register_leakage_at_equal_tightness": leak, "pass_within_register_d_gt_1": passed, "per_domain": per_dom,
               "constraint_subscore_items_1_2_5": {"cells": subscore, "d_tight_minus_loose_within_register": sub_within,
                                                   "register_leakage_at_equal_tightness": sub_leak},
               "rubric_system_prompt_sha256": hashlib.sha256(rubric.encode()).hexdigest(), "followup_text": FOLLOWUP}

    L = ["\n## Manipulation check (blind rubric rating)\n",
         f"Rater: `{args.model}` via `{BASE_URL}`, temperature {TEMPERATURE}, seed {SEED}, items in seeded random order, "
         f"system prompt = `tightness-rubric.md` verbatim, user message = item text only; response_format json_schema is sent (MiniMax-M3 accepts "
         f"but does not enforce it), the <think> block is stripped and the reply parsed; if unparseable, one follow-up turn asks for the five scores as JSON "
         f"(parse modes: {summary['parse_modes']}). Rated {len(ok)} / {len(rows)} items.\n",
         "Pre-stated pass rule: within each register, mean rubric total tight > loose with Cohen's d > 1.0. "
         + " ".join(f"{g}: loose {v['mean_loose']:.2f} vs tight {v['mean_tight']:.2f}, d = {v['d_tight_minus_loose']:.2f}." for g, v in within.items())
         + f" Overall d(tight − loose) = {main_tight:.2f}. **{'PASS' if passed else 'FAIL'}**\n",
         "| cell | n | mean total (SD) | item1 | item2 | item3 | item4 | item5 |", "|---|---|---|---|---|---|---|---|"]
    for c in CELLS:
        cs = cell_stats[c]
        L.append(f"| {c} | {cs['n']} | {cs['mean']:.2f} ({cs['sd']:.2f}) | " + " | ".join(f"{cs['items'][f'item{i}']:.2f}" for i in range(1, 6)) + " |")
    L += ["\n### Register difference at equal tightness (rubric leakage signal; reported, not a gate)\n",
          "| tightness | mean verse | mean prose | prose − verse | d | item1 Δ | item2 Δ | item3 Δ | item4 Δ | item5 Δ |", "|---|---|---|---|---|---|---|---|---|---|"]
    for t, v in leak.items():
        L.append(f"| {t} | {v['mean_verse']:.2f} | {v['mean_prose']:.2f} | {v['diff_prose_minus_verse']:+.2f} | {v['d_prose_minus_verse']:+.2f} | "
                 + " | ".join(f"{v['item_diff_prose_minus_verse'][f'item{i}']:+.2f}" for i in range(1, 6)) + " |")
    L += ["\nItems 3 and 4 of the rubric score the prompt's own syntax and figurative density, so a prose > verse difference at equal tightness is expected by construction; it means the rubric total is not a pure tightness score.\n",
          "### Constraint sub-score (items 1 + 2 + 5, range 0–6; the register-clean tightness score)\n",
          "| cell | mean (SD) |", "|---|---|"]
    L += [f"| {c} | {subscore[c]['mean']:.2f} ({subscore[c]['sd']:.2f}) |" for c in CELLS]
    L += ["", "Within-register d(tight − loose) on the sub-score: " + ", ".join(f"{g} {v:.2f}" for g, v in sub_within.items()) + ". "
          "Prose − verse at equal tightness on the sub-score: " + ", ".join(f"{t} {v['mean_prose']-v['mean_verse']:+.2f} (d = {v['d_prose_minus_verse']:+.2f})" for t, v in sub_leak.items()) + ".\n",
          "### Per domain\n", "| domain | " + " | ".join(CELLS) + " | d verse | d prose |", "|---|---|---|---|---|---|---|"]
    for d, pd in per_dom.items():
        L.append(f"| {d} | " + " | ".join(f"{pd['means'][c]:.2f}" for c in CELLS) + f" | {pd['d']['verse']:.2f} | {pd['d']['prose']:.2f} |")
    rep = Path(args.report)
    txt = rep.read_text() if rep.exists() else "# Selection report\n"
    txt = re.split(r"\n## Manipulation check", txt)[0]
    rep.write_text(txt + "\n".join(L) + "\n")
    mp = Path(args.manifest)
    if mp.exists():
        man = json.loads(mp.read_text()); man["manipulation_check"] = summary
        man["sha256_tightness_ratings_csv"] = hashlib.sha256(outp.read_bytes()).hexdigest()
        mp.write_text(json.dumps(man, indent=1, ensure_ascii=False))
    print(json.dumps({k: summary[k] for k in ["within_register", "d_tight_vs_loose_all", "register_leakage_at_equal_tightness",
                                               "pass_within_register_d_gt_1", "n_rated", "n_failed_parse", "parse_modes",
                                               "constraint_subscore_items_1_2_5"]}, indent=1))


if __name__ == "__main__":
    main()
