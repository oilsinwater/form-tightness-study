#!/usr/bin/env python3
"""generate_pool.py (v2) — build the 3x candidate pool for the 2x2 register x tightness stimulus set.

Cells: loose_verse, tight_verse, tight_prose, loose_prose. For every topic (topics.jsonl) x cell,
three candidates (c1-c3). Carried cells reuse v1 rows that already fall inside the token band:
  loose_verse <- v1 T1 c1-c4 ;  tight_prose <- v1 T3 c1-c5   (v1/pool.jsonl, in cand order)
Slots not filled by reuse, and the two new cells, are generated via CommandCode
(OpenAI-compatible; COMMANDCODE_API_KEY from ~/.hermes/.env) with meta_prompts/<cell>.txt as the
system message and a user message carrying the brief, domain, variant and a per-cell word target.

Length band is 130-200 Qwen3 tokens (Qwen/Qwen3-32B tokenizer, raw text), measured at generation
time; out-of-band candidates are rejected and rewritten up to MAX_REWRITES times; if every attempt
fails the attempt nearest the band is kept with gen_meta.len_ok=false.

Resumable: existing cand_ids in pool.jsonl are skipped.
Usage (raphael):  source ~/form-tightness/.venv/bin/activate; python generate_pool.py [--workers 8]
"""
import argparse, json, os, re, sys, time, threading, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

GEN_MODEL = "deepseek/deepseek-v4-pro"
BASE_URL = "https://api.commandcode.ai/provider/v1"
TEMPERATURE = 0.9
MAX_TOKENS = 8192  # reasoning tokens precede content
MAX_REWRITES = 4
TOK_MODEL = "Qwen/Qwen3-32B"
TMIN, TMAX = 130, 200
CELLS = ["loose_verse", "tight_verse", "tight_prose", "loose_prose"]
CELL_INFO = {"loose_verse": ("verse", "loose"), "tight_verse": ("verse", "tight"),
             "tight_prose": ("prose", "tight"), "loose_prose": ("prose", "loose")}
VARIANTS = ["A", "B", "C"]
N_PER_CELL = 3
# word targets from v1 tokens/word: 1.19 (verse, unconstrained prose), 1.42 (constraint-heavy)
TARGET = {"loose_verse": (125, 150), "tight_verse": (95, 120), "tight_prose": (100, 125), "loose_prose": (125, 150)}
TOK_PER_WORD = {"loose_verse": 1.19, "tight_verse": 1.42, "tight_prose": 1.42, "loose_prose": 1.19}
REUSE = {"loose_verse": ("T1", [1, 2, 3, 4]), "tight_prose": ("T3", [1, 2, 3, 4, 5])}
# Supplementary candidates (--supplement), added after the 1152-row selection left the prose register at
# r(tightness, tokens) = r(tightness, log_ppl) = +0.154: loose_prose pool rows were shorter (147.9 vs 157.9
# tokens) and lower-perplexity (2.34 vs 2.78) than tight_prose. One extra candidate per topic for each prose
# cell: loose_prose variant B (stream; the highest-ppl loose_prose variant) with a longer word target, and
# tight_prose variant C (domain-adapted; the lowest-ppl tight_prose family) with a shorter word target.
# Each entry: (cell, cand index, variant, target words).
SUPPLEMENT = [("loose_prose", 4, "B", (140, 160)), ("tight_prose", 4, "C", (95, 115))]
HERE = Path(__file__).resolve().parent

USER_TEMPLATE = (
    "DOMAIN: {domain}\n"
    "VARIANT: {variant}\n"
    "CONTENT BRIEF: {brief}\n\n"
    "Write the {cell_label} prompt now. Hard limits: 90-160 words. Aim for {lo}-{hi} words. "
    "Every brief detail present; output wrapped in <prompt></prompt>."
)
RETRY_TEMPLATE = (
    "That was {words} words, which is {tokens} tokens for our tokenizer; it must be between 130 and 200 tokens, "
    "so aim for about {lo2}-{hi2} words. Rewrite in the same cell, same variant, all brief details kept. "
    "Output wrapped in <prompt></prompt> only."
)


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


def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def extract_prompt(text):
    m = re.search(r"<prompt>\s*(.*?)\s*</prompt>", text, re.S)
    out = (m.group(1) if m else text).strip()
    return re.sub(r"</?prompt>", "", out).strip()


def main():
    global MAX_TOKENS
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", default=str(HERE / "topics.jsonl"))
    ap.add_argument("--out", default=str(HERE / "pool.jsonl"))
    ap.add_argument("--v1-pool", default=str(HERE / "v1" / "pool.jsonl"))
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default=GEN_MODEL)
    ap.add_argument("--reuse-only", action="store_true", help="only write the v1-reuse rows")
    ap.add_argument("--supplement", action="store_true", help="generate the SUPPLEMENT candidates (c4) instead of c1-c3")
    ap.add_argument("--max-tokens", type=int, default=MAX_TOKENS,
                    help="completion budget incl. reasoning; raise for rows whose reasoning exhausted 8192 (finish=length)")
    args = ap.parse_args()
    MAX_TOKENS = args.max_tokens

    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(TOK_MODEL)

    def ntok(s):
        return len(tok(s, add_special_tokens=False)["input_ids"])

    meta = {c: (HERE / "meta_prompts" / f"{c}.txt").read_text() for c in CELLS}
    meta_sha = {c: sha256(meta[c]) for c in CELLS}
    topics = [json.loads(l) for l in open(args.topics) if l.strip()]

    outp = Path(args.out)
    done = {}
    if outp.exists():
        for l in open(outp):
            if l.strip():
                r = json.loads(l); done[r["cand_id"]] = r
    lock = threading.Lock()

    def write(row):
        with lock:
            with open(outp, "a") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
            done[row["cand_id"]] = row

    # ---- 1. reuse v1 rows ----
    v1 = {}
    if Path(args.v1_pool).exists():
        for l in open(args.v1_pool):
            if l.strip():
                r = json.loads(l); v1[r["cand_id"]] = r
    n_reused = 0
    for t in topics:
        for cell, (lv, ks) in REUSE.items():
            slot = 1
            for k in ks:
                if slot > N_PER_CELL:
                    break
                cid = f"{t['topic_id']}_{cell}_c{slot}"
                src = v1.get(f"{t['topic_id']}_{lv}_c{k}")
                if src is None:
                    continue
                n = ntok(src["prompt_text"])
                if not (TMIN <= n <= TMAX):
                    continue
                if cid in done:
                    slot += 1
                    continue
                reg, tight = CELL_INFO[cell]
                gm = dict(src["gen_meta"]); gm.update({"v1_cand_id": src["cand_id"], "v1_level": lv,
                                                       "len_ok": True, "tokens_gen": n, "token_band": [TMIN, TMAX]})
                write({"cand_id": cid, "topic_id": t["topic_id"], "domain": t["domain"], "cell": cell,
                       "register": reg, "tightness": tight, "variant": src["variant"],
                       "prompt_text": src["prompt_text"], "words": word_count(src["prompt_text"]), "tokens_gen": n,
                       "gen_model": src["gen_model"], "source": "v1_reuse", "gen_meta": gm})
                n_reused += 1
                slot += 1
    print(f"v1 reuse: {n_reused} new rows written; pool now {len(done)} rows", flush=True)
    if args.reuse_only:
        return

    # ---- 2. jobs to generate ----
    jobs = []
    for t in topics:
        if args.supplement:
            for cell, k, v, target in SUPPLEMENT:
                cid = f"{t['topic_id']}_{cell}_c{k}"
                if cid not in done:
                    jobs.append((cid, t, cell, v, target))
        else:
            for cell in CELLS:
                for k in range(1, N_PER_CELL + 1):
                    cid = f"{t['topic_id']}_{cell}_c{k}"
                    if cid not in done:
                        jobs.append((cid, t, cell, VARIANTS[k - 1], TARGET[cell]))
    if args.limit:
        jobs = jobs[:args.limit]
    from collections import Counter
    print(f"{len(done)} done, {len(jobs)} to generate with {args.model}: {dict(Counter(j[2] for j in jobs))}", flush=True)
    if not jobs:
        print("DONE", flush=True); return

    from openai import OpenAI
    client = OpenAI(base_url=BASE_URL, api_key=load_api_key())

    def run(job):
        cid, t, cell, v, target = job
        lo, hi = target
        seed = int(sha256(cid)[:8], 16) % (2**31)
        msgs = [{"role": "system", "content": meta[cell]},
                {"role": "user", "content": USER_TEMPLATE.format(domain=t["domain"], variant=v, brief=t["brief"],
                                                                 cell_label=cell.replace("_", " "), lo=lo, hi=hi)}]
        attempts = []
        for attempt in range(1, MAX_REWRITES + 2):
            if attempt > 1:
                prev = attempts[-1]
                ratio = prev["tokens"] / max(prev["words"], 1)
                lo2, hi2 = int(145 / ratio), int(185 / ratio)
                msgs.append({"role": "assistant", "content": f"<prompt>\n{prev['text']}\n</prompt>"})
                msgs.append({"role": "user", "content": RETRY_TEMPLATE.format(
                    words=prev["words"], tokens=prev["tokens"], lo2=lo2, hi2=hi2)})
            r = None
            for net_try in range(6):
                try:
                    r = client.chat.completions.create(model=args.model, messages=msgs, temperature=TEMPERATURE,
                                                       max_tokens=MAX_TOKENS, seed=seed + attempt + 100 * net_try)
                    raw = r.choices[0].message.content or ""
                    if not raw.strip():
                        print(f"[{cid}] empty content (finish={r.choices[0].finish_reason}); retrying", flush=True)
                        r = None; continue
                    break
                except Exception as e:
                    wait = 5 * (net_try + 1)
                    print(f"[{cid}] API error {type(e).__name__}: {str(e)[:120]}; retry in {wait}s", flush=True)
                    time.sleep(wait)
            if r is None:
                break
            text = extract_prompt(raw)
            n = ntok(text)
            attempts.append({"text": text, "words": word_count(text), "tokens": n, "attempt": attempt,
                             "resp_model": getattr(r, "model", None), "usage": (r.usage.model_dump() if r.usage else None)})
            if TMIN <= n <= TMAX:
                break
        if not attempts:
            return {"cand_id": cid, "error": "api_failed"}
        best = min(attempts, key=lambda a: (0 if TMIN <= a["tokens"] <= TMAX else 1,
                                            min(abs(a["tokens"] - TMIN), abs(a["tokens"] - TMAX))))
        reg, tight = CELL_INFO[cell]
        row = {"cand_id": cid, "topic_id": t["topic_id"], "domain": t["domain"], "cell": cell,
               "register": reg, "tightness": tight, "variant": v, "prompt_text": best["text"],
               "words": best["words"], "tokens_gen": best["tokens"], "gen_model": args.model, "source": "v2_gen",
               "gen_meta": {"temperature": TEMPERATURE, "seed_requested": seed + best["attempt"],
                            "seed_note": "seed passed in request; provider determinism not guaranteed",
                            "endpoint": BASE_URL, "max_tokens": MAX_TOKENS,
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                            "attempts": best["attempt"], "n_attempts": len(attempts), "words": best["words"],
                            "tokens_gen": best["tokens"], "target_words": list(target), "supplement": bool(args.supplement),
                            "tok_per_word_assumed": TOK_PER_WORD[cell], "token_band": [TMIN, TMAX],
                            "tok_model": TOK_MODEL, "len_ok": TMIN <= best["tokens"] <= TMAX,
                            "meta_prompt_sha256": meta_sha[cell], "response_model": best["resp_model"],
                            "usage": best["usage"],
                            "attempt_tokens": [a["tokens"] for a in attempts]}}
        write(row)
        return row

    n_ok = n_err = n_len = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(run, j) for j in jobs]
        for i, fu in enumerate(as_completed(futs), 1):
            row = fu.result()
            if "error" in row:
                n_err += 1
            else:
                n_ok += 1
                if not row["gen_meta"]["len_ok"]:
                    n_len += 1
            if i % 20 == 0 or i == len(jobs):
                print(f"{i}/{len(jobs)} ok={n_ok} err={n_err} out_of_band={n_len} {time.time()-t0:.0f}s", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
