#!/usr/bin/env python3
"""check_c_rate_user_turns.py — blind tightness rating of every distinct user turn in
results/check_c_projections.csv (pre-stimulus check (c)).

Reuses the v1 rater protocol from stimuli/rate_tightness.py: system prompt = tightness-rubric.md
verbatim, user message = the user turn text, nothing else. The rater never sees projections,
assistant text, transcript name, or turn index. Items deduplicated by user_text_sha256 and rated
in a seeded random order (seed 20261030). deepseek/deepseek-v4.1-flash via CommandCode, T 0,
json_schema response_format (plain-text parse fallback, parse_mode logged).

Writes results/check_c_user_tightness.csv:
  user_text_sha256, item1..item5, total, raw_json, model, ts  (+ parse_mode, rating_order)
Resumable: already-rated hashes are skipped.
"""
import argparse, csv, json, os, random, re, sys, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

RATER_MODEL = "deepseek/deepseek-v4.1-flash"
BASE_URL = "https://api.commandcode.ai/provider/v1"
TEMPERATURE = 0.0
MAX_TOKENS = 4096
SEED = 20261030

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
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            if all(f"item{i}" in d for i in range(1, 6)):
                return {f"item{i}": int(d[f"item{i}"]) for i in range(1, 6)}, "json"
            vals = [d[k] for k in sorted(d) if str(d[k]).strip() in "012"]
            if len(vals) == 5:
                return {f"item{i}": int(vals[i - 1]) for i in range(1, 6)}, "json_loose"
        except Exception:
            pass
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--projections", required=True)
    ap.add_argument("--rubric", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default=RATER_MODEL)
    args = ap.parse_args()

    from openai import OpenAI
    client = OpenAI(base_url=BASE_URL, api_key=load_api_key())
    rubric = Path(args.rubric).read_text()

    # distinct user turns, keyed by sha256; blind: only the text leaves this dict
    items = {}
    with open(args.projections, newline="") as f:
        for r in csv.DictReader(f):
            items.setdefault(r["user_text_sha256"], r["user_text"])
    hashes = sorted(items)  # deterministic base order before seeded shuffle
    rng = random.Random(SEED)
    rng.shuffle(hashes)
    if args.limit:
        hashes = hashes[: args.limit]

    outp = Path(args.out)
    done = set()
    if outp.exists():
        with open(outp, newline="") as f:
            done = {r["user_text_sha256"] for r in csv.DictReader(f) if r["total"] != ""}
    jobs = [(pos, h) for pos, h in enumerate(hashes) if h not in done]
    print(f"{len(items)} distinct user turns; {len(done)} already rated; {len(jobs)} to rate "
          f"with {args.model} T={TEMPERATURE}", flush=True)

    fields = ["user_text_sha256", "item1", "item2", "item3", "item4", "item5", "total",
              "raw_json", "model", "ts", "parse_mode", "rating_order"]
    lock = threading.Lock()
    newfile = not outp.exists()
    fh = open(outp, "a", newline="")
    w = csv.DictWriter(fh, fieldnames=fields)
    if newfile:
        w.writeheader(); fh.flush()
    state = {"use_schema": True}

    def rate(job):
        pos, h = job
        msgs = [{"role": "system", "content": rubric}, {"role": "user", "content": items[h]}]
        content, scores, mode = "", None, "failed"
        for attempt in range(4):
            kw = dict(model=args.model, messages=msgs, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, seed=SEED)
            if state["use_schema"]:
                kw["response_format"] = {"type": "json_schema", "json_schema": SCHEMA}
            try:
                r = client.chat.completions.create(**kw)
                content = r.choices[0].message.content or ""
                if not content.strip():
                    print(f"[{h[:8]}] empty content (finish={r.choices[0].finish_reason}); retry", flush=True)
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
                print(f"[{h[:8]}] API error: {msg[:160]}; retry", flush=True)
                time.sleep(5 * (attempt + 1))
        row = {"user_text_sha256": h,
               **({k: scores[k] for k in scores} if scores else {f"item{i}": "" for i in range(1, 6)}),
               "total": sum(scores.values()) if scores else "",
               "raw_json": content[:500].replace("\n", " "), "model": args.model,
               "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "parse_mode": mode, "rating_order": pos}
        with lock:
            w.writerow(row); fh.flush()
        return row

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(rate, j) for j in jobs]
        for i, fu in enumerate(as_completed(futs), 1):
            fu.result()
            if i % 20 == 0 or i == len(jobs):
                print(f"{i}/{len(jobs)} {time.time()-t0:.0f}s", flush=True)
    fh.close()

    rows = list(csv.DictReader(open(outp, newline="")))
    ok = [r for r in rows if r["total"] != ""]
    totals = [int(r["total"]) for r in ok]
    from collections import Counter
    print(json.dumps({"n_rated": len(ok), "n_failed": len(rows) - len(ok),
                      "parse_modes": dict(Counter(r["parse_mode"] for r in rows)),
                      "total_distribution": dict(sorted(Counter(totals).items()))}, indent=1))


if __name__ == "__main__":
    main()
