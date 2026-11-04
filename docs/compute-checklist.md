---
title: Compute Checklist — raphael
type: research
status: draft
date: 2026-10-16
---

# Compute Checklist

## 1. What raphael actually has (checked 2026-10-16 via ssh)

| Item | Value |
|---|---|
| GPU | 1 × NVIDIA GeForce RTX 3090, **24,576 MiB** |
| GPU in use at check time | 22,881 MiB (llama.cpp server holding a model) |
| System RAM | 61 GB total, ~42 GB available |
| Disk | 580 GB free on `/` |
| Python ML stack | **torch and transformers not installed** in system python |
| Local model cache | GGUF only: `unsloth/Qwen3.8-27B-GGUF`, `gemma-4-26B-A4B-it-uncensored-heretic-GGUF` |

Consequence: the existing llama.cpp setup cannot serve this study — GGUF inference does not expose residual-stream activations in a form the published axis vectors apply to. A separate HF/transformers environment is required, and the llama.cpp server must be stopped during runs to free VRAM.

## 2. Model options

| Model | In Lu et al. set? | bf16 VRAM | 4-bit nf4 VRAM (approx) | Fits 24 GB? |
|---|---|---|---|---|
| Qwen3-32B | yes | ~64 GB | ~18–20 GB + activations/KV | **tight but yes**, batch size 1–2, short generations |
| Gemma 2 27B | yes | ~54 GB | ~15–16 GB | yes, more headroom |
| Llama 3.3 70B | yes | ~140 GB | ~38 GB | no |
| Qwen3-8B / Gemma 2 9B | no | ~16–18 GB | — | yes in bf16, but off the comparison set |

**Recommendation to Phil:** attempt Qwen3-32B in nf4 first (A2 feasibility run). If peak VRAM leaves < 2 GB headroom or throughput makes 288 × 3 infeasible in one session, fall back to Gemma 2 27B — still in the Lu et al. set, still comparable. Do not drop below 27B without re-scoping the claim.

**Quantisation caveat for the write-up:** published axis vectors were extracted from bf16 models. nf4 keeps the residual stream in bf16 at runtime, so projections are meaningful, but the sanity check in A3 (reproduce Lu et al.'s role ordering on 10 of their prompts) is mandatory, and the quantisation is a stated limitation.

## 3. Environment setup (Track A1)

```bash
ssh raphael
python3 -m venv ~/venvs/fta && source ~/venvs/fta/bin/activate
pip install --upgrade pip
pip install torch --index-url https://download.pytorch.org/whl/cu124   # match driver; check `nvidia-smi` CUDA version first
pip install transformers accelerate bitsandbytes safetensors sentencepiece
pip install nnsight    # or transformer_lens; nnsight handles 4-bit + hooks more gracefully
pip install pandas pyarrow statsmodels
git clone https://github.com/safety-research/assistant-axis ~/src/assistant-axis
git clone https://github.com/andyrdt/refusal_direction ~/src/refusal_direction   # optional, for the routing follow-up
```

Model download: `huggingface-cli download Qwen/Qwen3-32B` (~65 GB safetensors; disk is fine). Record the revision hash.

## 4. Feasibility run (Track A2) — what to verify

- [ ] Model loads in nf4 with `device_map="auto"`; report `torch.cuda.max_memory_allocated()`
- [ ] Hook at the layer the assistant-axis repo specifies for this model; confirm hidden size and that the captured tensor is the post-MLP residual at the last prompt token
- [ ] Tokens/sec for a 200-token generation at batch 1
- [ ] Estimated wall time for 288 prompts × 3 seeds × 200 tokens
- [ ] Confirm the chat template matches what Lu et al. used (their repo shows it)

## 5. Axis sanity check (Track A3) — must pass before preregistration lock

- [ ] Load published axis vector for the model; record file hash and layer index
- [ ] Run 10 role prompts from the repo (5 Assistant-like, 5 fantastical) through the same pipeline
- [ ] Projections must order Assistant-like > fantastical with no overlap; if they don't, the pipeline is wrong — stop and debug, do not proceed to stimuli

## 6. Run protocol (Track D)

1. Stop the llama.cpp server (coordinate with Phil — other work depends on it).
2. Activate venv, set seeds, load model once.
3. Iterate prompts from `stimuli/prompts.jsonl`; for each: tokenise with chat template → forward → capture last-prompt-token residual at layer L (and all layers if VRAM allows) → generate ≤ 200 tokens × 3 seeds → capture per-token projections.
4. Write one JSONL line per (prompt, seed) to `runs/<date>-<tag>/results.jsonl`; write `manifest.json` with model revision, quant, layer, vector hash, seeds, git commit of the project folder, start/end time.
5. Restart llama.cpp.

## 7. Known risks

- bitsandbytes + RTX 3090 (Ampere) is well supported; CUDA/driver mismatch is the usual failure — check `nvidia-smi` CUDA version before choosing the torch wheel.
- iCloud-synced vault is not a place for 65 GB of weights or large run outputs; keep weights in `~/.cache/huggingface` on raphael and only sync JSONL summaries into `runs/`.
- Judge model (Track D3) should not be the target model; use a different family via API or the llama.cpp server after it is restarted.
