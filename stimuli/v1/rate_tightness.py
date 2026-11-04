#!/usr/bin/env python3
"""rate_tightness.py — blind LLM rating of each stimulus with tightness-rubric.md.

System prompt = the exact text of tightness-rubric.md. User message = the item text. Nothing
else. Items are rated in a seeded random order with no labels. Scores are requested as JSON
through the API's response_format (json_schema) so no instruction is added to the prompt;
if the endpoint rejects response_format, the plain reply is parsed for the five 0-2 scores
(parse_mode logged per item).

Model: deepseek/deepseek-v4.1-flash via CommandCode, temperature 0. The model emits reasoning
tokens before content; only message.content is read.

Writes tightness_ratings.csv and appends a manipulation-check section to selection_report.md.
"""
import argparse, csv, json, os, random, re, sys, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import numpy as np

RATER_MODEL = "deepseek/deepseek-v4.1-flash"
BASE_URL = "https://api.commandcode.ai/provider/v1"
TEMPERATURE = 0.0
MAX_TOKENS = 4096  # reasoning tokens precede content; 1024 was exhausted on half the smoke items
SEED = 20261030
LEVELS = ["T1", "T2", "T3"]
HERE = Path(__file__).resolve().parent

SCHEMA = {
    "name": "tightness_scores",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {f"item{i}": {"type": "integer", "minimum": 0, "maximum": 2} for i in range(1, 6)},
        "required": [f"item{i}" for i in range(1, 6)],
        "additionalProperties": False,
    },
}


def load_api_key(name="COMMANDCODE_API_KEY"):
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


def parse_scores(text):
    """Return (dict item1..item5, mode) or (None, mode)."""
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            if all(f"item{i}" in d for i in range(1, 6)):
                return {f"item{i}": int(d[f"item{i}"]) for i in range(1, 6)}, "json"
            # tolerate {"1":..,"2":..} or lists
            vals = [d[k] for k in sorted(d) if str(d[k]).strip() in "012"]
            if len(vals) == 5:
                return {f"item{i}": int(vals[i-1]) for i in range(1, 6)}, "json_loose"
        except Exception:
            pass
    # table / lines like "| 1 | ... | 2 |" or "Item 1: 2"
    found = {}
    for i in range(1, 6):
        mm = re.search(rf"(?:item\s*{i}|^\|?\s*{i}\s*\|)[^0-9\n]*?([012])\b", text, re.I | re.M)
        if not mm:
            mm = re.search(rf"\b{i}\b[^\n]*?\b([012])\s*(?:/\s*2)?\s*$", text, re.M)
        if mm:
            found[f"item{i}"] = int(mm.group(1))
    if len(found) == 5:
        return found, "regex"
    return None, "failed"


def cohens_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    sp = np.sqrt(((len(a)-1)*a.var(ddof=1) + (len(b)-1)*b.var(ddof=1)) / (len(a)+len(b)-2))
    return float((b.mean() - a.mean()) / sp) if sp > 0 else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stimuli", default=str(HERE / "stimuli.jsonl"))
    ap.add_argument("--rubric", default=str(HERE / "tightness-rubric.md"))
    ap.add_argument("--out", default=str(HERE / "tightness_ratings.csv"))
    ap.add_argument("--report", default=str(HERE / "selection_report.md"))
    ap.add_argument("--manifest", default=str(HERE / "manifest.json"))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default=RATER_MODEL)
    args = ap.parse_args()

    from openai import OpenAI
    client = OpenAI(base_url=BASE_URL, api_key=load_api_key())
    rubric = Path(args.rubric).read_text()
    stim = [json.loads(l) for l in open(args.stimuli) if l.strip()]
    rng = random.Random(SEED)
    order = list(range(len(stim))); rng.shuffle(order)
    if args.limit:
        order = order[:args.limit]

    done = {}
    outp = Path(args.out)
    if outp.exists():
        with open(outp) as f:
            for r in csv.DictReader(f):
                done[r["id"]] = r
    jobs = [(pos, stim[i]) for pos, i in enumerate(order) if stim[i]["id"] not in done]
    print(f"{len(done)} rated, {len(jobs)} to rate with {args.model} T={TEMPERATURE}", flush=True)

    fields = ["id", "domain", "topic_id", "tightness_level", "item1", "item2", "item3", "item4", "item5",
              "total", "parse_mode", "rater_model", "temperature", "rating_order", "timestamp", "raw"]
    lock = threading.Lock()
    newfile = not outp.exists()
    fh = open(outp, "a", newline="")
    w = csv.DictWriter(fh, fieldnames=fields)
    if newfile:
        w.writeheader(); fh.flush()
    state = {"use_schema": True}

    def rate(job):
        pos, s = job
        msgs = [{"role": "system", "content": rubric}, {"role": "user", "content": s["prompt"]}]
        content, scores, mode = "", None, "failed"
        for attempt in range(4):
            kw = dict(model=args.model, messages=msgs, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, seed=SEED)
            if state["use_schema"]:
                kw["response_format"] = {"type": "json_schema", "json_schema": SCHEMA}
            try:
                r = client.chat.completions.create(**kw)
                content = r.choices[0].message.content or ""
                if not content.strip():
                    print(f"[{s['id']}] empty content (finish={r.choices[0].finish_reason}); retry", flush=True)
                    continue
                scores, mode = parse_scores(content)
                if scores:
                    if state["use_schema"]:
                        mode = "json_schema"
                    break
            except Exception as e:
                msg = str(e)
                if state["use_schema"] and ("response_format" in msg or "json_schema" in msg or "400" in msg):
                    print(f"response_format rejected ({msg[:120]}); falling back to plain parsing", flush=True)
                    state["use_schema"] = False
                    continue
                print(f"[{s['id']}] API error: {msg[:160]}; retry", flush=True)
                time.sleep(5 * (attempt + 1))
        row = {"id": s["id"], "domain": s["domain"], "topic_id": s["topic_id"], "tightness_level": s["tightness_level"],
               **({k: scores[k] for k in scores} if scores else {f"item{i}": "" for i in range(1, 6)}),
               "total": sum(scores.values()) if scores else "", "parse_mode": mode, "rater_model": args.model,
               "temperature": TEMPERATURE, "rating_order": pos, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
               "raw": content[:500].replace("\n", " ")}
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

    # ---- manipulation check ----
    rows = list(csv.DictReader(open(outp)))
    ok = [r for r in rows if r["total"] != ""]
    by = {lv: [float(r["total"]) for r in ok if r["tightness_level"] == lv] for lv in LEVELS}
    item_means = {lv: {f"item{i}": float(np.mean([float(r[f"item{i}"]) for r in ok if r["tightness_level"] == lv]))
                       for i in range(1, 6)} for lv in LEVELS}
    d12 = cohens_d(by["T1"], by["T2"]); d23 = cohens_d(by["T2"], by["T3"]); d13 = cohens_d(by["T1"], by["T3"])
    means = {lv: float(np.mean(by[lv])) for lv in LEVELS}
    sds = {lv: float(np.std(by[lv], ddof=1)) for lv in LEVELS}
    monotone = means["T1"] < means["T2"] < means["T3"]
    passed = monotone and d12 > 1.0 and d23 > 1.0
    per_dom = {}
    for d in sorted({r["domain"] for r in ok}):
        bd = {lv: [float(r["total"]) for r in ok if r["domain"] == d and r["tightness_level"] == lv] for lv in LEVELS}
        per_dom[d] = {"means": {lv: float(np.mean(bd[lv])) for lv in LEVELS},
                      "d12": cohens_d(bd["T1"], bd["T2"]), "d23": cohens_d(bd["T2"], bd["T3"])}
    summary = {"rater_model": args.model, "endpoint": BASE_URL, "temperature": TEMPERATURE, "n_rated": len(ok),
               "n_failed_parse": len(rows) - len(ok), "parse_modes": dict(zip(*np.unique([r["parse_mode"] for r in rows], return_counts=True))) if rows else {},
               "mean_total": means, "sd_total": sds, "item_means": item_means,
               "cohens_d": {"T1_vs_T2": d12, "T2_vs_T3": d23, "T1_vs_T3": d13},
               "monotone": monotone, "pass_d_gt_1": passed, "per_domain": per_dom}
    summary["parse_modes"] = {str(k): int(v) for k, v in summary["parse_modes"].items()}

    L = ["\n## Manipulation check (blind rubric rating)\n",
         f"Rater: `{args.model}` via `{BASE_URL}`, temperature {TEMPERATURE}, seed {SEED}, items in seeded random order, "
         f"system prompt = `tightness-rubric.md` verbatim, user message = item text only, scores returned via "
         f"response_format json_schema where accepted (parse modes: {summary['parse_modes']}). "
         f"Rated {len(ok)} / {len(rows)} items.\n",
         f"Pre-stated pass rule: mean total monotone T1 < T2 < T3 and Cohen's d > 1.0 between adjacent levels. "
         f"**Monotone: {monotone}. d(T1,T2) = {d12:.2f}, d(T2,T3) = {d23:.2f}, d(T1,T3) = {d13:.2f}. Pass: {passed}**\n",
         "| level | n | mean total (SD) | item1 | item2 | item3 | item4 | item5 |", "|---|---|---|---|---|---|---|---|"]
    for lv in LEVELS:
        im = item_means[lv]
        L.append(f"| {lv} | {len(by[lv])} | {means[lv]:.2f} ({sds[lv]:.2f}) | " + " | ".join(f"{im[f'item{i}']:.2f}" for i in range(1, 6)) + " |")
    L += ["\n| domain | T1 | T2 | T3 | d(T1,T2) | d(T2,T3) |", "|---|---|---|---|---|---|"]
    for d, pd in per_dom.items():
        L.append(f"| {d} | {pd['means']['T1']:.2f} | {pd['means']['T2']:.2f} | {pd['means']['T3']:.2f} | {pd['d12']:.2f} | {pd['d23']:.2f} |")
    rep = Path(args.report)
    txt = rep.read_text() if rep.exists() else "# Selection report\n"
    txt = re.split(r"\n## Manipulation check", txt)[0]
    rep.write_text(txt + "\n".join(L) + "\n")
    mp = Path(args.manifest)
    if mp.exists():
        man = json.loads(mp.read_text()); man["manipulation_check"] = summary
        man["sha256_tightness_ratings_csv"] = __import__("hashlib").sha256(outp.read_bytes()).hexdigest()
        mp.write_text(json.dumps(man, indent=1, ensure_ascii=False))
    print(json.dumps({k: summary[k] for k in ["mean_total", "cohens_d", "monotone", "pass_d_gt_1", "n_rated", "n_failed_parse", "parse_modes"]}, indent=1))


if __name__ == "__main__":
    main()
