#!/usr/bin/env python3
"""address_screen.py (v3) — automated ADDRESS screen on EVERY pool candidate (verse and prose).

Two independent coders per row:
  1. regex  (address_regex.py): vocative / epithet / identity-predicate patterns -> address_regex in {none, flagged}
  2. blind LLM coder: MiniMax-M3, temperature 0, system prompt = prereg/followup-motif-swap/coding-scheme.md
     (worked-example ids withheld, as in code_v2_attribution.py) + a JSON output instruction; user message =
     the prompt text only; no cell label, no id; seeded random order. Returns ADDRESS (none/vocative/ratified),
     ATTRIB_COUNT, SELF_REF_COUNT, USER_FIRST_PERSON, attrib_phrases. MiniMax-M3's <think> block is stripped.
A candidate is ELIGIBLE for selection only if address_regex == "none" AND address_llm == "none".

Writes address_codes.jsonl (one row per cand_id; resumable by cand_id + text sha256) and
address_screen_report.md (drop counts per cell).
Usage (raphael): python address_screen.py [--pool pool.jsonl] [--workers 8]
"""
import argparse, hashlib, json, os, random, re, sys, time, threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

CODER_MODEL = "MiniMax-M3"
BASE_URL = "https://api.minimax.io/v1"
API_KEY_NAME = "MINIMAX_API_KEY"
TEMPERATURE = 0.0
MAX_TOKENS = 6144
PAUSE = 1.5  # seconds between successful calls (MiniMax token-plan burst limit)
SEED = 20261030
CELLS = ["loose_verse", "tight_verse", "tight_prose", "loose_prose"]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from address_regex import screen  # noqa: E402

ID_RE = re.compile(r"`?(coding|writing|therapy_like|philosophy_of_ai)_\d\d_(loose|tight)_(verse|prose)`?")
OUTPUT_INSTR = """
## Output

Code ADDRESS, ATTRIB_COUNT, SELF_REF_COUNT and USER_FIRST_PERSON only (MOTIF is not needed here).
Return ONLY a JSON object (no prose, no code fence) with exactly these keys:
{"address": "none"|"vocative"|"ratified",
 "attrib_count": integer,
 "attrib_phrases": [list of the counted phrases, quoted from the text],
 "self_ref_count": integer,
 "user_first_person": 0|1}
"""


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


def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def strip_think(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()


def parse_json(text):
    text = strip_think(text)
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m.group(0) if m else text)


def scheme_for_llm(path):
    txt = Path(path).read_text(encoding="utf-8")
    txt = txt.split("## Reliability")[0]
    txt = ID_RE.sub("[id withheld]", txt)
    return txt + OUTPUT_INSTR


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", default=str(HERE / "pool.jsonl"))
    ap.add_argument("--out", default=str(HERE / "address_codes.jsonl"))
    ap.add_argument("--report", default=str(HERE / "address_screen_report.md"))
    ap.add_argument("--scheme", default=str(HERE.parent / "prereg" / "followup-motif-swap" / "coding-scheme.md"))
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default=CODER_MODEL)
    ap.add_argument("--regex-only", action="store_true")
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.pool) if l.strip()]
    system = scheme_for_llm(args.scheme)
    system_sha = sha256(system)
    outp = Path(args.out)
    done = {}
    if outp.exists():
        for l in open(outp):
            if l.strip():
                r = json.loads(l); done[r["cand_id"]] = r
    by_id = {r["cand_id"]: r for r in rows}
    # keep prior codes only when text unchanged
    done = {k: v for k, v in done.items() if k in by_id and v.get("text_sha256") == sha256(by_id[k]["prompt_text"])
            and v.get("address_llm") not in (None, "", "failed")}
    order = list(range(len(rows))); random.Random(SEED).shuffle(order)
    todo = [rows[i] for i in order if rows[i]["cand_id"] not in done]
    if args.limit:
        todo = todo[:args.limit]
    print(f"{len(rows)} pool rows, {len(done)} already coded, {len(todo)} to code with {args.model} T={TEMPERATURE}", flush=True)

    lock = threading.Lock()
    fh = open(outp, "w")
    for v in done.values():
        fh.write(json.dumps(v, ensure_ascii=False) + "\n")
    fh.flush()

    client = None
    if not args.regex_only and todo:
        from openai import OpenAI
        client = OpenAI(base_url=BASE_URL, api_key=load_api_key(), timeout=300)

    def code(r):
        sc = screen(r["prompt_text"], r["register"])
        out = {"cand_id": r["cand_id"], "cell": r["cell"], "topic_id": r["topic_id"], "register": r["register"],
               "text_sha256": sha256(r["prompt_text"]), "address_regex": sc["address_regex"],
               "regex_hits": sc["regex_hits"], "second_person_count": sc["second_person_count"], "soft_hits": sc["soft_hits"],
               "address_llm": None, "attrib_count": None, "self_ref_count": None, "user_first_person": None,
               "attrib_phrases": None, "llm_model": args.model, "llm_temperature": TEMPERATURE, "scheme_sha256": system_sha,
               "raw": ""}
        if client is not None:
            content = ""
            backoff = 10.0
            for attempt in range(40):
                try:
                    resp = client.chat.completions.create(
                        model=args.model, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, seed=SEED,
                        messages=[{"role": "system", "content": system},
                                  {"role": "user", "content": "PROMPT TO CODE:\n\n" + r["prompt_text"]}],
                        response_format={"type": "json_object"})
                    content = resp.choices[0].message.content or ""
                    obj = parse_json(content)
                    addr = str(obj.get("address", "")).strip().lower()
                    if addr not in ("none", "vocative", "ratified"):
                        raise ValueError(f"bad address value {addr!r}")
                    ph = obj.get("attrib_phrases", [])
                    out.update({"address_llm": addr, "attrib_count": int(obj.get("attrib_count", 0) or 0),
                                "self_ref_count": int(obj.get("self_ref_count", 0) or 0),
                                "user_first_person": 1 if int(obj.get("user_first_person", 0) or 0) else 0,
                                "attrib_phrases": ph if isinstance(ph, list) else [str(ph)],
                                "raw": strip_think(content)[:600]})
                    time.sleep(PAUSE)
                    break
                except Exception as e:
                    msg = str(e)
                    print(f"[{r['cand_id']}] {type(e).__name__}: {msg[:120]} (attempt {attempt+1})", flush=True)
                    if "429" in msg or "rate limit" in msg.lower() or "rate_limit" in msg.lower():
                        time.sleep(backoff); backoff = min(backoff * 2, 600.0)
                    else:
                        time.sleep(min(3.0 * (attempt + 1), 60.0))
            if out["address_llm"] is None:
                out["address_llm"] = "failed"; out["raw"] = strip_think(content)[:600]
        with lock:
            fh.write(json.dumps(out, ensure_ascii=False) + "\n"); fh.flush()
            done[r["cand_id"]] = out
        return out

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(code, r) for r in todo]
        for i, fu in enumerate(as_completed(futs), 1):
            fu.result()
            if i % 50 == 0 or i == len(todo):
                print(f"{i}/{len(todo)} {time.time()-t0:.0f}s", flush=True)
    fh.close()

    # ---- report ----
    codes = [json.loads(l) for l in open(outp) if l.strip()]
    per = defaultdict(Counter)
    topic_elig = defaultdict(int)
    for c in codes:
        cell = c["cell"]; per[cell]["n"] += 1
        rg = c["address_regex"] == "none"; ll = c["address_llm"] == "none"
        per[cell]["regex_flagged"] += 0 if rg else 1
        per[cell]["llm_vocative"] += 1 if c["address_llm"] == "vocative" else 0
        per[cell]["llm_ratified"] += 1 if c["address_llm"] == "ratified" else 0
        per[cell]["llm_failed"] += 1 if c["address_llm"] == "failed" else 0
        per[cell]["regex_only_flag"] += 1 if (not rg and ll) else 0
        per[cell]["llm_only_flag"] += 1 if (rg and not ll) else 0
        per[cell]["both_flag"] += 1 if (not rg and not ll) else 0
        elig = rg and ll
        per[cell]["eligible"] += 1 if elig else 0
        per[cell]["dropped"] += 0 if elig else 1
        if elig:
            topic_elig[(c["topic_id"], cell)] += 1
    L = [f"# Address screen report (v3) — {time.strftime('%Y-%m-%dT%H:%M:%S%z')}\n",
         f"Pool: {len(codes)} candidates (`{Path(args.pool).name}`). Coders: (1) regex `address_regex.py`; (2) blind LLM coder `{args.model}` via `{BASE_URL}`, T = {TEMPERATURE}, "
         f"system prompt = `coding-scheme.md` (ids withheld) + JSON output instruction (sha256 {system_sha[:16]}…), user message = prompt text only, seeded order {SEED}. "
         "A candidate is eligible only if BOTH code `none`.\n",
         "| cell | n | regex flagged | LLM vocative | LLM ratified | LLM failed | flagged by regex only | by LLM only | by both | **dropped** | eligible | drop rate |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for cell in CELLS:
        p = per[cell]
        L.append(f"| {cell} | {p['n']} | {p['regex_flagged']} | {p['llm_vocative']} | {p['llm_ratified']} | {p['llm_failed']} | {p['regex_only_flag']} | {p['llm_only_flag']} | {p['both_flag']} | **{p['dropped']}** | {p['eligible']} | {p['dropped']/max(p['n'],1):.1%} |")
    topics = sorted({c["topic_id"] for c in codes})
    empty = [(t, cell) for t in topics for cell in CELLS if topic_elig[(t, cell)] == 0]
    L.append(f"\nTopic × cell slots with ZERO eligible candidates: {len(empty)}" + (f" — {empty}" if empty else "") + ".")
    dist = Counter(min(topic_elig[(t, cell)], 9) for t in topics for cell in CELLS)
    L.append("Eligible candidates per topic × cell slot: " + ", ".join(f"{k}: {v}" for k, v in sorted(dist.items())) + ".")
    hitc = Counter(h[0] for c in codes for h in c["regex_hits"])
    L.append("\nRegex hit types (all cells): " + ", ".join(f"{k} {v}" for k, v in hitc.most_common()) + ".")
    Path(args.report).write_text("\n".join(L) + "\n")
    print("\n".join(L))
    summary = {cell: dict(per[cell]) for cell in CELLS}
    summary["empty_slots"] = empty
    Path(args.report).with_suffix(".json").write_text(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
