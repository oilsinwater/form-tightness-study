#!/usr/bin/env python3
"""generate_pool.py — build the 3x candidate pool for the form-tightness stimulus set.

For every topic (topics.jsonl) x level (T1,T2,T3) x variant (A,B,C) one candidate is
generated via CommandCode (OpenAI-compatible endpoint; COMMANDCODE_API_KEY from ~/.hermes/.env)
with the per-level meta-prompt in meta_prompts/<level>.txt
(system message) and a user message carrying the brief, domain and variant.

Resumable: existing rows in pool.jsonl are skipped. Candidates outside the 90-160 word
band are retried up to MAX_RETRY times; the last attempt is kept with len_ok=false.

Usage (on raphael):
  source ~/form-tightness/.venv/bin/activate
  python generate_pool.py --out pool.jsonl [--workers 6] [--limit N]
"""
import argparse, json, os, re, sys, time, threading, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

GEN_MODEL = "deepseek/deepseek-v4-pro"
BASE_URL = "https://api.commandcode.ai/provider/v1"  # CommandCode, OpenAI-compatible
TEMPERATURE = 0.9
MAX_TOKENS = 8192  # model emits (long) reasoning tokens before content; 1536 was exhausted on ~40% of calls
MAX_RETRY = 3
LEVELS = ["T1", "T2", "T3"]
VARIANTS = ["A", "B", "C"]
WMIN, WMAX = 90, 160
HERE = Path(__file__).resolve().parent


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
    sys.exit(f"{name} not found (env or ~/.hermes/.env)")


def word_count(s):
    return len(re.findall(r"\S+", s))


def extract_prompt(text):
    m = re.search(r"<prompt>\s*(.*?)\s*</prompt>", text, re.S)
    out = (m.group(1) if m else text).strip()
    out = re.sub(r"</?prompt>", "", out).strip()  # stray tags when the model forgot to close
    return out


# Level-specific target sub-bands inside the 90-160 band. Calibrated after the first 228 candidates
# (T2 mean 97 words, T3 mean 141) showed a level-length skew that the selection step could not remove.
TARGET = {"T1": (110, 150), "T2": (135, 160), "T3": (90, 115)}
# second recalibration after 160 more rows: with (105-145 / 125-155 / 95-130) means were T2 117, T3 136.
USER_TEMPLATE = (
    "DOMAIN: {domain}\n"
    "VARIANT: {variant}\n"
    "CONTENT BRIEF: {brief}\n\n"
    "Write the {level} prompt now. Hard limits: 90-160 words. Aim for {lo}-{hi} words. "
    "Every brief detail present; output wrapped in <prompt></prompt>."
)


def build_user_msg(topic, level, variant, band=(WMIN, WMAX), target=None):
    lo, hi = target or TARGET[level]
    tmpl = USER_TEMPLATE.replace("90-160", f"{band[0]}-{band[1]}")
    return tmpl.format(domain=topic["domain"], variant=variant, brief=topic["brief"],
                       level=level, lo=lo, hi=hi)


# Supplementary candidates (--supplement). Added after the 864-row pool showed T3 tokenizing at
# ~1.4 tokens/word (mean 185 tokens vs 134 for T1), leaving the selection step unable to match
# token counts across levels. Each entry: (level, cand index, variant, hard word band, target band).
SUPPLEMENT = [
    ("T3", 4, "C", (90, 100), (90, 100)),
    ("T3", 5, "B", (90, 100), (90, 100)),
    ("T1", 4, "A", (90, 160), (145, 160)),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", default=str(HERE / "topics.jsonl"))
    ap.add_argument("--out", default=str(HERE / "pool.jsonl"))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0, help="debug: only first N jobs")
    ap.add_argument("--model", default=GEN_MODEL)
    ap.add_argument("--supplement", action="store_true", help="generate the SUPPLEMENT candidates instead of c1-c3")
    args = ap.parse_args()

    from openai import OpenAI
    client = OpenAI(base_url=BASE_URL, api_key=load_api_key())

    meta = {lv: (HERE / "meta_prompts" / f"{lv}.txt").read_text() for lv in LEVELS}
    meta_sha = {lv: hashlib.sha256(meta[lv].encode()).hexdigest() for lv in LEVELS}
    topics = [json.loads(l) for l in open(args.topics) if l.strip()]

    done = set()
    outp = Path(args.out)
    if outp.exists():
        for l in open(outp):
            if l.strip():
                done.add(json.loads(l)["cand_id"])

    jobs = []
    for t in topics:
        if args.supplement:
            for lv, k, v, band, target in SUPPLEMENT:
                cid = f"{t['topic_id']}_{lv}_c{k}"
                if cid not in done:
                    jobs.append((cid, t, lv, v, k, band, target))
        else:
            for lv in LEVELS:
                for k, v in enumerate(VARIANTS, 1):
                    cid = f"{t['topic_id']}_{lv}_c{k}"
                    if cid not in done:
                        jobs.append((cid, t, lv, v, k, (WMIN, WMAX), TARGET[lv]))
    if args.limit:
        jobs = jobs[:args.limit]
    print(f"{len(done)} done, {len(jobs)} to generate with {args.model}", flush=True)

    lock = threading.Lock()

    def run(job):
        cid, t, lv, v, k, band, target = job
        wmin, wmax = band
        seed = int(hashlib.sha256(cid.encode()).hexdigest()[:8], 16) % (2**31)
        attempts = []
        for attempt in range(1, MAX_RETRY + 1):
            msgs = [{"role": "system", "content": meta[lv]},
                    {"role": "user", "content": build_user_msg(t, lv, v, band, target)}]
            if attempt > 1:
                prev = attempts[-1]
                msgs.append({"role": "assistant", "content": f"<prompt>\n{prev['text']}\n</prompt>"})
                msgs.append({"role": "user", "content":
                             f"That was {prev['words']} words; it must be between {wmin} and {wmax} words. "
                             f"Rewrite at the same level, same variant, all brief details kept, inside the band. "
                             f"Output wrapped in <prompt></prompt> only."})
            for net_try in range(5):
                try:
                    r = client.chat.completions.create(
                        model=args.model, messages=msgs, temperature=TEMPERATURE,
                        max_tokens=MAX_TOKENS, seed=seed + attempt + 100 * net_try)
                    raw = r.choices[0].message.content or ""  # reasoning_content ignored
                    if not raw.strip():
                        # reasoning exhausted the budget: retry same request, not counted as a word-band attempt
                        print(f"[{cid}] empty content (finish={r.choices[0].finish_reason}); retrying", flush=True)
                        continue
                    break
                except Exception as e:
                    wait = 5 * (net_try + 1)
                    print(f"[{cid}] API error {type(e).__name__}: {e}; retry in {wait}s", flush=True)
                    time.sleep(wait)
            else:
                return {"cand_id": cid, "error": "api_failed"}
            text = extract_prompt(raw)
            wc = word_count(text)
            attempts.append({"text": text, "words": wc, "attempt": attempt,
                             "resp_model": getattr(r, "model", None),
                             "usage": (r.usage.model_dump() if r.usage else None)})
            if wmin <= wc <= wmax:
                break
        if not attempts:
            return {"cand_id": cid, "error": "no_content"}
        # keep the attempt closest to the band if none landed inside it
        best = min(attempts, key=lambda a: (0 if wmin <= a["words"] <= wmax else 1,
                                            min(abs(a["words"] - wmin), abs(a["words"] - wmax))))
        row = {
            "cand_id": cid, "topic_id": t["topic_id"], "domain": t["domain"], "level": lv,
            "variant": v, "prompt_text": best["text"], "gen_model": args.model,
            "gen_meta": {
                "temperature": TEMPERATURE, "seed_requested": seed + best["attempt"],
                "seed_note": "seed passed in request; provider determinism not guaranteed",
                "endpoint": BASE_URL,
                "max_tokens": MAX_TOKENS, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "attempts": best["attempt"], "words": best["words"],
                "target_words": list(target), "hard_band": list(band),
                "supplement": bool(args.supplement),
                "len_ok": WMIN <= best["words"] <= WMAX,
                "meta_prompt_sha256": meta_sha[lv], "response_model": best["resp_model"],
                "usage": best["usage"],
            },
        }
        with lock:
            with open(outp, "a") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        return row

    n_ok = n_err = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(run, j) for j in jobs]
        for i, fu in enumerate(as_completed(futs), 1):
            row = fu.result()
            if "error" in row:
                n_err += 1
            else:
                n_ok += 1
            if i % 20 == 0 or i == len(jobs):
                print(f"{i}/{len(jobs)} ok={n_ok} err={n_err} {time.time()-t0:.0f}s", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
