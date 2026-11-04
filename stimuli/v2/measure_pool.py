#!/usr/bin/env python3
"""measure_pool.py (v2) — token count (Qwen/Qwen3-32B tokenizer) and base-model perplexity
(Qwen/Qwen3-14B-Base, 4-bit NF4, bf16 compute) for every candidate in pool.jsonl.

Raw text, no chat template, no BOS added. Perplexity = exp(mean NLL over tokens 1..n-1).
Rows whose prompt text sha256 matches a row already measured in v1/pool_measured.jsonl (same
tokenizer, same model, same quantisation) inherit that measurement (measure_meta.reused_from_v1).
Only rows with no match touch the GPU; the model is loaded only if such rows exist.

Usage (raphael):  python measure_pool.py [--pool pool.jsonl] [--out pool_measured.jsonl]
"""
import argparse, hashlib, json, math, subprocess, sys, time
from pathlib import Path

TOK_MODEL = "Qwen/Qwen3-32B"
PPL_MODEL = "Qwen/Qwen3-14B-Base"
HERE = Path(__file__).resolve().parent
MEASURE_META = {"tok_model": TOK_MODEL, "ppl_model": PPL_MODEL, "quant": "bnb nf4 double-quant, bf16 compute",
                "chat_template": False, "bos_added": False}


def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def free_gpu_mb():
    out = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"], text=True)
    return int(out.strip().splitlines()[0])


def wait_for_gpu(min_mb=12000, every=300, max_wait=3600):
    t0 = time.time()
    while True:
        free = free_gpu_mb()
        if free >= min_mb:
            print(f"GPU free: {free} MiB", flush=True); return True
        if time.time() - t0 > max_wait:
            print(f"GPU still busy after {max_wait}s (free={free} MiB); giving up", flush=True); return False
        print(f"GPU busy (free={free} MiB); retry in {every}s", flush=True)
        time.sleep(every)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", default=str(HERE / "pool.jsonl"))
    ap.add_argument("--out", default=str(HERE / "pool_measured.jsonl"))
    ap.add_argument("--v1-measured", default=str(HERE / "v1" / "pool_measured.jsonl"))
    ap.add_argument("--no-wait", action="store_true")
    ap.add_argument("--max-wait", type=int, default=3600)
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.pool) if l.strip()]
    done = {}
    outp = Path(args.out)
    if outp.exists():
        for l in open(outp):
            if l.strip():
                r = json.loads(l); done[r["cand_id"]] = r
    todo = [r for r in rows if r["cand_id"] not in done]
    print(f"{len(rows)} rows, {len(done)} measured, {len(todo)} to do", flush=True)
    if not todo:
        print("DONE", flush=True); return

    # v1 measurements keyed by text sha
    v1 = {}
    if Path(args.v1_measured).exists():
        for l in open(args.v1_measured):
            if l.strip():
                r = json.loads(l)
                if r.get("measure_meta", {}).get("ppl_model") == PPL_MODEL:
                    v1[sha256(r["prompt_text"])] = r
    gpu_rows = []
    n_reused = 0
    with open(outp, "a") as f:
        for r in todo:
            m = v1.get(sha256(r["prompt_text"]))
            if m is None:
                gpu_rows.append(r); continue
            out = dict(r)
            out.update({k: m[k] for k in ["tokens", "tokens_14b", "n_scored", "mean_nll", "log_ppl", "ppl"]})
            out["measure_meta"] = dict(MEASURE_META, reused_from_v1=m["cand_id"])
            f.write(json.dumps(out, ensure_ascii=False) + "\n"); n_reused += 1
    print(f"{n_reused} rows inherited v1 measurements by text sha256; {len(gpu_rows)} need the GPU", flush=True)
    if not gpu_rows:
        print("DONE", flush=True); return

    if not args.no_wait and not wait_for_gpu(max_wait=args.max_wait):
        sys.exit(2)
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    tok32 = AutoTokenizer.from_pretrained(TOK_MODEL)
    tok14 = AutoTokenizer.from_pretrained(PPL_MODEL)
    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True)
    t0 = time.time()
    model = AutoModelForCausalLM.from_pretrained(PPL_MODEL, quantization_config=bnb, dtype=torch.bfloat16, device_map="cuda:0")
    model.eval()
    print(f"model loaded in {time.time()-t0:.0f}s; gpu alloc {torch.cuda.memory_allocated()/2**30:.1f} GB", flush=True)
    t0 = time.time()
    with open(outp, "a") as f, torch.no_grad():
        for i, r in enumerate(gpu_rows, 1):
            text = r["prompt_text"]
            n_tok32 = len(tok32(text, add_special_tokens=False)["input_ids"])
            ids = tok14(text, add_special_tokens=False, return_tensors="pt")["input_ids"].to("cuda:0")
            logits = model(ids).logits.float()
            logp = torch.log_softmax(logits[0, :-1], dim=-1)
            tgt = ids[0, 1:]
            nll = -logp.gather(1, tgt[:, None]).squeeze(1)
            mean_nll = nll.mean().item()
            out = dict(r)
            out.update({"tokens": n_tok32, "tokens_14b": int(ids.shape[1]), "n_scored": int(tgt.shape[0]),
                        "mean_nll": mean_nll, "log_ppl": mean_nll, "ppl": math.exp(mean_nll), "measure_meta": MEASURE_META})
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
            if i % 50 == 0 or i == len(gpu_rows):
                f.flush()
                print(f"{i}/{len(gpu_rows)} {time.time()-t0:.0f}s last ppl={math.exp(mean_nll):.2f} tok={n_tok32}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
