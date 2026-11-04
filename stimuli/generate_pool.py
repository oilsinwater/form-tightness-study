#!/usr/bin/env python3
"""generate_pool.py (v3) — build the candidate pool for the v3 2x2 register x tightness stimulus set.

v3 = v2 with the two VERSE cells regenerated under meta-prompts that forbid any address of the
model (ADDRESS = none; see meta_prompts/CHANGES.md). The two PROSE cells are carried forward from
v2/pool.jsonl unchanged (rows copied byte-for-byte; they already code address = none at 99 %).

Verse cells: for every topic x {loose_verse, tight_verse}, N_PER_CELL = 4 candidates (c1..c4;
variants A, B, C, then A/B/C rotating by topic index). Generator: MiniMax-M3 via the MiniMax
OpenAI-compatible endpoint (MINIMAX_API_KEY from env or ~/.hermes/.env), temperature 0.9.
Each candidate must fall inside 130-200 Qwen3 tokens (Qwen/Qwen3-32B tokenizer, raw text) AND pass
the deterministic address regex (address_regex.py); a failing candidate is rejected and the generator
is asked to rewrite (up to MAX_REWRITES times, each failure type with its own feedback message). If
every attempt fails, the attempt nearest the band is kept with gen_meta.len_ok / gen_meta.addr_ok
set accordingly (selection excludes addr_ok=false rows; len_ok=false rows are penalised).

MiniMax-M3 returns its reasoning inside <think>...</think> in message.content; it is stripped
before the <prompt> block is extracted.

Resumable: existing cand_ids in pool.jsonl are skipped. --extra N adds candidates c5..c(4+N) for
the verse cells (pool enlargement if the no-address constraint leaves too few eligible rows).
Usage (raphael):  source ~/form-tightness/.venv/bin/activate; python generate_pool.py [--workers 8]
"""
import argparse, json, os, re, sys, time, threading, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

GEN_MODEL = "MiniMax-M3"
BASE_URL = "https://api.minimax.io/v1"
API_KEY_NAME = "MINIMAX_API_KEY"
TEMPERATURE = 0.9
MAX_TOKENS = 8192  # reasoning (<think>) precedes content
MAX_REWRITES = 4
TOK_MODEL = "Qwen/Qwen3-32B"
TMIN, TMAX = 130, 200
CELLS = ["loose_verse", "tight_verse", "tight_prose", "loose_prose"]
VERSE_CELLS = ["loose_verse", "tight_verse"]
PROSE_CELLS = ["tight_prose", "loose_prose"]
CELL_INFO = {"loose_verse": ("verse", "loose"), "tight_verse": ("verse", "tight"),
             "tight_prose": ("prose", "tight"), "loose_prose": ("prose", "loose")}
VARIANTS = ["A", "B", "C"]
N_PER_CELL = 4
# word targets from v1/v2 tokens/word: 1.19 (verse, unconstrained), 1.47 observed for tight_verse in v2
TARGET = {"loose_verse": (125, 150), "tight_verse": (95, 120)}
TOK_PER_WORD = {"loose_verse": 1.19, "tight_verse": 1.47}
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from address_regex import screen  # noqa: E402

USER_TEMPLATE = (
    "DOMAIN: {domain}\n"
    "VARIANT: {variant}\n"
    "CONTENT BRIEF: {brief}\n\n"
    "Write the {cell_label} prompt now. Hard limits: 90-160 words. Aim for {lo}-{hi} words. "
    "Every brief detail present; output wrapped in <prompt></prompt>."
)
RETRY_LEN = (
    "That was {words} words, which is {tokens} tokens for our tokenizer; it must be between 130 and 200 tokens, "
    "so aim for about {lo2}-{hi2} words. Rewrite in the same cell, same variant, all brief details kept. "
    "Output wrapped in <prompt></prompt> only."
)
RETRY_ADDR = (
    "That version breaks the HARD RULE: NO ADDRESS. Offending text: {hits}. Rewrite in the same cell, same variant, "
    "all brief details kept, with no vocative, no epithet and no identity predicate for whoever answers "
    "(no \"you, X\", no \"O X\", no \"you are\"); requests as bare imperatives or first-person wishes. "
    "Keep the length ({lo}-{hi} words). Output wrapped in <prompt></prompt> only."
)
RETRY_BOTH = RETRY_ADDR + " Also: that was {tokens} tokens; it must be 130-200 tokens, so aim for about {lo2}-{hi2} words."


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
    sys.exit(f"{name} not found (env or ~/.hermes/.env)")


def word_count(s):
    return len(re.findall(r"\S+", s))


def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def strip_think(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()


def extract_prompt(text):
    text = strip_think(text)
    m = re.search(r"<prompt>\s*(.*?)\s*</prompt>", text, re.S)
    out = (m.group(1) if m else text).strip()
    return re.sub(r"</?prompt>", "", out).strip()


def main():
    global MAX_TOKENS
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", default=str(HERE / "topics.jsonl"))
    ap.add_argument("--out", default=str(HERE / "pool.jsonl"))
    ap.add_argument("--v2-pool", default=str(HERE / "v2" / "pool.jsonl"))
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default=GEN_MODEL)
    ap.add_argument("--carry-only", action="store_true", help="only copy the v2 prose rows")
    ap.add_argument("--extra", type=int, default=0, help="generate N extra verse candidates per topic x cell (c5..)")
    ap.add_argument("--only-cell", default=None)
    ap.add_argument("--max-tokens", type=int, default=MAX_TOKENS)
    args = ap.parse_args()
    MAX_TOKENS = args.max_tokens

    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(TOK_MODEL)

    def ntok(s):
        return len(tok(s, add_special_tokens=False)["input_ids"])

    meta = {c: (HERE / "meta_prompts" / f"{c}.txt").read_text() for c in VERSE_CELLS}
    meta_sha = {c: sha256(meta[c]) for c in VERSE_CELLS}
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

    # ---- 1. carry the v2 prose rows unchanged ----
    n_carried = 0
    if Path(args.v2_pool).exists():
        for l in open(args.v2_pool):
            if not l.strip():
                continue
            r = json.loads(l)
            if r["cell"] in PROSE_CELLS and r["cand_id"] not in done:
                write(r); n_carried += 1
    print(f"v2 prose carry: {n_carried} rows copied unchanged; pool now {len(done)} rows", flush=True)
    if args.carry_only:
        return

    # ---- 2. verse jobs ----
    jobs = []
    for ti, t in enumerate(topics):
        for cell in VERSE_CELLS:
            if args.only_cell and cell != args.only_cell:
                continue
            ks = range(N_PER_CELL + 1, N_PER_CELL + 1 + args.extra) if args.extra else range(1, N_PER_CELL + 1)
            for k in ks:
                cid = f"{t['topic_id']}_{cell}_c{k}"
                if cid in done:
                    continue
                v = VARIANTS[k - 1] if k <= 3 else VARIANTS[(ti + k) % 3]
                jobs.append((cid, t, cell, v, TARGET[cell]))
    if args.limit:
        jobs = jobs[:args.limit]
    from collections import Counter
    print(f"{len(done)} done, {len(jobs)} to generate with {args.model}: {dict(Counter(j[2] for j in jobs))}", flush=True)
    if not jobs:
        print("DONE", flush=True); return

    from openai import OpenAI
    client = OpenAI(base_url=BASE_URL, api_key=load_api_key(), timeout=300)

    def run(job):
        cid, t, cell, v, target = job
        lo, hi = target
        reg, tight = CELL_INFO[cell]
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
                hits = "; ".join(f'"{h[1]}"' for h in prev["hits"][:4])
                if not prev["len_ok"] and not prev["addr_ok"]:
                    fb = RETRY_BOTH.format(hits=hits, lo=lo, hi=hi, tokens=prev["tokens"], lo2=lo2, hi2=hi2)
                elif not prev["addr_ok"]:
                    fb = RETRY_ADDR.format(hits=hits, lo=lo, hi=hi)
                else:
                    fb = RETRY_LEN.format(words=prev["words"], tokens=prev["tokens"], lo2=lo2, hi2=hi2)
                msgs.append({"role": "user", "content": fb})
            r = None
            for net_try in range(6):
                try:
                    r = client.chat.completions.create(model=args.model, messages=msgs, temperature=TEMPERATURE,
                                                       max_tokens=MAX_TOKENS, seed=seed + attempt + 100 * net_try)
                    raw = r.choices[0].message.content or ""
                    if not strip_think(raw):
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
            sc = screen(text, reg)
            attempts.append({"text": text, "words": word_count(text), "tokens": n, "attempt": attempt,
                             "len_ok": TMIN <= n <= TMAX, "addr_ok": sc["address_regex"] == "none", "hits": sc["regex_hits"],
                             "resp_model": getattr(r, "model", None), "usage": (r.usage.model_dump() if r.usage else None)})
            if attempts[-1]["len_ok"] and attempts[-1]["addr_ok"]:
                break
        if not attempts:
            return {"cand_id": cid, "error": "api_failed"}
        best = min(attempts, key=lambda a: (0 if a["addr_ok"] else 1, 0 if a["len_ok"] else 1,
                                            min(abs(a["tokens"] - TMIN), abs(a["tokens"] - TMAX))))
        row = {"cand_id": cid, "topic_id": t["topic_id"], "domain": t["domain"], "cell": cell,
               "register": reg, "tightness": tight, "variant": v, "prompt_text": best["text"],
               "words": best["words"], "tokens_gen": best["tokens"], "gen_model": args.model, "source": "v3_gen",
               "gen_meta": {"temperature": TEMPERATURE, "seed_requested": seed + best["attempt"],
                            "seed_note": "seed passed in request; provider determinism not guaranteed",
                            "endpoint": BASE_URL, "max_tokens": MAX_TOKENS,
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                            "attempts": best["attempt"], "n_attempts": len(attempts), "words": best["words"],
                            "tokens_gen": best["tokens"], "target_words": list(target), "extra": bool(args.extra),
                            "tok_per_word_assumed": TOK_PER_WORD[cell], "token_band": [TMIN, TMAX],
                            "tok_model": TOK_MODEL, "len_ok": best["len_ok"], "addr_ok": best["addr_ok"],
                            "addr_regex_hits": best["hits"],
                            "n_len_rejects": sum(1 for a in attempts if not a["len_ok"]),
                            "n_addr_rejects": sum(1 for a in attempts if not a["addr_ok"]),
                            "meta_prompt_sha256": meta_sha[cell], "response_model": best["resp_model"],
                            "usage": best["usage"],
                            "attempt_tokens": [a["tokens"] for a in attempts]}}
        write(row)
        return row

    n_ok = n_err = n_len = n_addr = 0
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
                if not row["gen_meta"]["addr_ok"]:
                    n_addr += 1
            if i % 20 == 0 or i == len(jobs):
                print(f"{i}/{len(jobs)} ok={n_ok} err={n_err} out_of_band={n_len} addr_fail={n_addr} {time.time()-t0:.0f}s", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
