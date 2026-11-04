"""
check_b_refusal_cosine.py — Pre-stimulus check (b).

Arditi et al. 2024 refusal direction (diff-in-means, harmful − harmless) for
Qwen3-32B (4-bit NF4), at every layer, at two kinds of positions:
  * 'last_instruction_token' : the last token of the user instruction content
    (post-chat-template, thinking off) — the position named in PLAN.md;
  * Arditi's post-instruction ("eoi") positions: every token the template adds
    after the instruction when add_generation_prompt=True (for Qwen3 with
    thinking off that is '<|im_end|>\\n<|im_start|>assistant\\n<think>\\n\\n</think>\\n\\n'),
    indexed relative to the sequence end (-k .. -1). Arditi's code uses
    positions = range(-len(eoi_toks), 0).
Residual stream is read at the OUTPUT of model.model.layers[i] (same indexing
as the published axis). Arditi hooks resid_pre of block i (= output of block
i-1); we note this one-block shift rather than silently mixing conventions.

Data: refusal_direction/dataset/splits/{harmful,harmless}_train.json,
sampled exactly as their pipeline does (random.seed(42); random.sample(..., 128)).

Then: cosine(refusal_dir[layer], published_axis[layer]) for all layers.
Output: results/check_b_refusal_cosine.json (also copied to outputs/).
Deviation from Arditi: we do NOT run their ablation/steering/KL-based
direction *selection* (needs hundreds of generation sweeps); we report the
full layer × position sweep and the max |cos| over the layers they keep
(they prune the last 20 % of layers).
"""
import json, os, random, sys, time
import torch
from common import *

N = 128
OUT_JSON = os.path.join(RESULTS, "check_b_refusal_cosine.json")
RD = os.path.join(FT, "refusal_direction")


def load_split(kind):
    with open(os.path.join(RD, "dataset", "splits", f"{kind}_train.json")) as f:
        return [d["instruction"] for d in json.load(f)]


def positions_for_prompt(b, instruction):
    """Return (ids, idx_last_instruction_token, n_eoi)."""
    conv = [{"role": "user", "content": instruction}]
    ids = b.tok.apply_chat_template(conv, tokenize=True, add_generation_prompt=True, **b.chat_kwargs)
    im_end = b.tok.convert_tokens_to_ids("<|im_end|>")
    # last instruction token = token right before the first <|im_end|> after the user header
    j = ids.index(im_end)
    n_eoi = len(ids) - j            # tokens from <|im_end|> to end (template suffix)
    return ids, j - 1, n_eoi


def mean_acts(b, instructions, batch_size=16):
    """Returns dict: {'last_instr': (L,H) float64, 'eoi': (n_eoi, L, H) float64, 'n_eoi': k}"""
    L = b.n_layers
    H = b.model.config.hidden_size
    n_eoi = None
    acc_last = torch.zeros(L, H, dtype=torch.float64)
    acc_eoi = None
    n = len(instructions)
    b.tok.padding_side = "left"
    for s in range(0, n, batch_size):
        batch = instructions[s:s + batch_size]
        seqs, last_idx = [], []
        for ins in batch:
            ids, li, k = positions_for_prompt(b, ins)
            if n_eoi is None:
                n_eoi = k
                acc_eoi = torch.zeros(k, L, H, dtype=torch.float64)
            assert k == n_eoi, "template suffix length changed"
            seqs.append(ids); last_idx.append(li)
        T = max(len(x) for x in seqs)
        pad = b.tok.pad_token_id
        ids_t = torch.full((len(seqs), T), pad, dtype=torch.long)
        att = torch.zeros((len(seqs), T), dtype=torch.long)
        li_t = []
        for r, ids in enumerate(seqs):
            off = T - len(ids)                       # left padding
            ids_t[r, off:] = torch.tensor(ids)
            att[r, off:] = 1
            li_t.append(off + last_idx[r])
        li_t = torch.tensor(li_t)

        def reducer(_i, h):  # (B,T,H) on GPU -> (1+n_eoi, B, H) cpu float64
            rows = [h[torch.arange(h.shape[0]), li_t.to(h.device), :]]
            for p in range(-n_eoi, 0):
                rows.append(h[:, p, :])
            return torch.stack(rows).double().cpu()

        out = collect_hidden(b, ids_t.to(b.device), att.to(b.device), list(range(L)), reducer=reducer)
        for i in range(L):
            acc_last[i] += out[i][0].sum(0)
            acc_eoi[:, i, :] += out[i][1:].sum(1)
        log(f"  {s + len(batch)}/{n}")
    return {"last_instr": acc_last / n, "eoi": acc_eoi / n, "n_eoi": n_eoi}


def main():
    t0 = time.time()
    random.seed(42)
    harmful = random.sample(load_split("harmful"), N)
    harmless = random.sample(load_split("harmless"), N)
    log(f"{len(harmful)} harmful, {len(harmless)} harmless")

    b = load_model(QWEN)
    log(f"activation backend: {b.backend}")
    axis = load_published_axis("qwen")        # (64, 5120)
    ids, li, k = positions_for_prompt(b, harmful[0])
    eoi_text = b.tok.decode(ids[li + 1:])
    log(f"n_eoi={k} eoi tokens={eoi_text!r}; last-instruction token={b.tok.decode([ids[li]])!r}")

    log("harmful ...")
    mh = mean_acts(b, harmful)
    log("harmless ...")
    ml = mean_acts(b, harmless)
    n_eoi = mh["n_eoi"]

    dir_last = (mh["last_instr"] - ml["last_instr"]).float()          # (L,H)
    dir_eoi = (mh["eoi"] - ml["eoi"]).float()                           # (n_eoi,L,H)
    cos_last = cosine_per_layer(dir_last, axis)
    cos_eoi = {str(p): cosine_per_layer(dir_eoi[p + n_eoi], axis) for p in range(-n_eoi, 0)}

    L = b.n_layers
    keep = int(L * 0.8)   # Arditi prunes the last 20 % of layers from selection
    def argmax_abs(c, upto=None):
        c2 = c[:upto] if upto else c
        i = max(range(len(c2)), key=lambda j: abs(c2[j]))
        return i, c2[i]

    i_last, c_last = argmax_abs(cos_last, keep)
    i_last_all, c_last_all = argmax_abs(cos_last)
    i_m1, c_m1 = argmax_abs(cos_eoi["-1"], keep)
    all_eoi_cos = [(abs(c), p, j) for p, cs in cos_eoi.items() for j, c in enumerate(cs[:keep])]
    best = max(all_eoi_cos)

    res = {
        "model": QWEN, "quantization": "bnb nf4, double quant, bf16 compute",
        "activation_backend": b.backend,
        "residual_read_point": "output of model.model.layers[i] (axis indexing); Arditi uses resid_pre of block i = output of block i-1",
        "n_harmful": N, "n_harmless": N, "sampling": "random.seed(42); random.sample(train split, 128) as in refusal_direction/pipeline/run_pipeline.py",
        "chat_template": "apply_chat_template(add_generation_prompt=True, enable_thinking=False)",
        "eoi_tokens_text": eoi_text, "n_eoi_positions": n_eoi,
        "layer_pruning_for_max": f"max taken over layers 0..{keep - 1} (Arditi prunes last 20%); unpruned max also given",
        "cos_per_layer_last_instruction_token": cos_last,
        "cos_per_layer_eoi_positions": cos_eoi,
        "cos_L32_last_instruction_token": cos_last[32],
        "cos_L32_eoi_pos_-1": cos_eoi["-1"][32],
        "cos_L32_all_eoi_positions": {p: cs[32] for p, cs in cos_eoi.items()},
        "max_abs_cos_last_instruction_token": {"layer": i_last, "cos": c_last},
        "max_abs_cos_last_instruction_token_unpruned": {"layer": i_last_all, "cos": c_last_all},
        "max_abs_cos_eoi_pos_-1": {"layer": i_m1, "cos": c_m1},
        "max_abs_cos_any_eoi_position": {"position": best[1], "layer": best[2], "abs_cos": best[0]},
        "refusal_dir_norm_per_layer_last_instr": [float(x) for x in dir_last.norm(dim=1)],
        "axis_norm_per_layer": [float(x) for x in axis.float().norm(dim=1)],
        "elapsed_s": round(time.time() - t0, 1),
        "deviations": ["no ablation/steering/KL-based direction selection (Arditi) — full layer×position sweep reported instead",
                       "4-bit NF4 model instead of bf16", "read point = block output (axis convention), not resid_pre"],
    }
    torch.save({"dir_last_instr": dir_last, "dir_eoi": dir_eoi, "n_eoi": n_eoi}, os.path.join(OUTPUTS, "check_b_refusal_dirs.pt"))
    with open(OUT_JSON, "w") as f:
        json.dump(res, f, indent=1)
    log(f"wrote {OUT_JSON}")
    log(f"cos@L32 last-instr={cos_last[32]:+.4f}  eoi[-1]={cos_eoi['-1'][32]:+.4f}  max|cos| last-instr: L{i_last} {c_last:+.4f}; eoi[-1]: L{i_m1} {c_m1:+.4f}")
    free_model(b)


if __name__ == "__main__":
    main()
