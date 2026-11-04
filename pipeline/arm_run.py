"""
arm_run.py — Arms 1–3 runner (v3 stimuli, with the pre-registered secondary readouts).

Input : stimuli/stimuli.jsonl  (id, domain, topic_id, register, tightness, cell, prompt, ...)
For each stimulus x sample: generate (no system prompt, thinking off, temp 0.7, top-p 0.9,
max_new_tokens 512), then ONE forward pass over [user, assistant] collecting, over the
response tokens (think spans removed by the repo encoder; fenced code removed):
  * projection_published  mean activation at the primary layer on the published axis
  * projection_ours       same on results/check_a_axis_ours.pt (Qwen only)
  * proj_L<l>             published-axis projection at each sweep layer   (prereg secondary 2)
  * projection_refusal    mean activation on the Arditi refusal direction  (secondary 1, Qwen)
  * tok_decile_0..9       per-token published-axis projection, 10 position deciles (secondary 3)
  * floor_frac_L<l>       fraction of response tokens whose projection on the published capping
                          vector exceeds its cap tau, layers 46–53       (secondary 4, Qwen)
Flags:
  --capping                   Arm 2: published capping during generation AND read-back
  --capping-measure-uncapped  read back without the hooks
  --model google/gemma-2-27b-it --layer 22 --axis gemma   Arm 3 (sweep defaults 6,11,22,34)
Output: results/arm_<name>.csv (resumable: rows keyed by id+sample).
"""
import argparse, csv, json, os, sys, time
import torch
from common import *


def build_cols(sweep, floor_layers):
    return (["arm", "stimulus_id", "domain", "topic_id", "register", "tightness", "cell", "sample",
             "model", "layer", "capping", "projection_published", "projection_ours", "projection_refusal"]
            + [f"proj_L{l}" for l in sweep]
            + [f"tok_decile_{d}" for d in range(10)]
            + [f"floor_frac_L{l}" for l in floor_layers] + ["floor_frac_mean"]
            + ["n_response_tokens", "n_tokens_span", "prompt_sha256", "response_sha256", "response", "backend"])


def unit(v):
    v = v.float()
    return v / (v.norm() + 1e-8)


def readout(b, conv, primary, sweep, axis_pub, refusal, floor_items, exclude_code):
    """Single forward pass; per-response quantities for the LAST assistant turn."""
    full_ids, spans = turn_spans(b, conv)
    ids = torch.tensor([full_ids], device=b.device)
    span = [s for s in spans if s["role"] == "assistant"][-1]
    mask = include_mask_for_span(b, span, exclude_code)
    floor = {l: (u, c) for l, u, c in floor_items}
    axis_layers = set([primary] + list(sweep))
    layers = sorted(axis_layers | set(floor))
    U = {l: unit(axis_pub[l]) for l in axis_layers}
    ref_u = unit(refusal[primary]) if refusal is not None else None

    def reducer(i, h):
        seg = h[0, span["start"]:span["end"], :].float()
        m = mask.to(seg.device)
        seg = seg[m] if bool(m.any()) else seg[:0]
        if seg.shape[0] == 0:
            return {}
        res = {}
        mean = seg.mean(0)
        if i in U:
            res["proj"] = float(mean @ U[i].to(seg.device))
        if i == primary:
            res["mean"] = mean.cpu()
            tp = (seg @ U[i].to(seg.device)).cpu()
            n = tp.shape[0]
            res["deciles"] = [float(tp[int(d * n / 10):max(int((d + 1) * n / 10), int(d * n / 10) + 1)].mean())
                              for d in range(10)]
            if ref_u is not None:
                res["refusal"] = float(mean @ ref_u.to(seg.device))
        if i in floor:
            u, c = floor[i]
            res["floor"] = float(((seg @ u.to(seg.device)) > c).float().mean())
        return res

    out = collect_hidden(b, ids, None, layers, reducer=reducer)
    return out, int(mask.sum()), int(mask.numel())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stimuli", default=os.path.join(FT, "stimuli", "stimuli.jsonl"))
    ap.add_argument("--name", default="1_observation")
    ap.add_argument("--model", default=QWEN)
    ap.add_argument("--layer", type=int, default=32)
    ap.add_argument("--axis", default="qwen", choices=["qwen", "gemma"])
    ap.add_argument("--sweep", default=None, help="comma list; default 11,22,32,45 (qwen) / 6,11,22,34 (gemma)")
    ap.add_argument("--n-samples", type=int, default=3)
    ap.add_argument("--batch", type=int, default=12, help="conversations per generate() call")
    ap.add_argument("--capping", action="store_true")
    ap.add_argument("--capping-experiment", default="layers_46:54-p0.25")
    ap.add_argument("--capping-measure-uncapped", action="store_true")
    ap.add_argument("--max-new-tokens", type=int, default=512)
    ap.add_argument("--seed", type=int, default=20261030)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--exclude-code", action="store_true", default=True)
    args = ap.parse_args()
    sweep = [int(x) for x in (args.sweep or ("11,22,32,45" if args.axis == "qwen" else "6,11,22,34")).split(",")]

    stim = [json.loads(l) for l in open(args.stimuli) if l.strip()]
    if args.limit:
        stim = stim[:args.limit]
    out_csv = os.path.join(RESULTS, f"arm_{args.name}.csv")

    b = load_model(args.model)
    axis_pub = load_published_axis(args.axis).float()
    ours_path = os.path.join(RESULTS, "check_a_axis_ours.pt")
    axis_ours = torch.load(ours_path, weights_only=True).float() if (os.path.exists(ours_path) and args.axis == "qwen") else None
    refusal = None
    rp = os.path.join(FT, "outputs", "check_b_refusal_dirs.pt")
    if args.axis == "qwen" and os.path.exists(rp):
        # dict of tensors (+ one None) written by check_b; tensors only -> weights_only is safe
        refusal = torch.load(rp, map_location="cpu", weights_only=True)["dir_last_instr"].float()
    floor_items, cap_ctx = [], None
    if args.axis == "qwen":
        ivs = capping_interventions(load_capping_config("qwen"), args.capping_experiment)
        floor_items = [(int(i["layer"]), unit(i["vector"]), float(i["cap"])) for i in ivs]
        if args.capping:
            log(f"capping {args.capping_experiment}: " + ", ".join(f"L{i['layer']} cap={i['cap']:.2f}" for i in ivs))
            cap_ctx = CappingHooks(b, ivs)
    floor_layers = [l for l, _, _ in floor_items]
    COLS = build_cols(sweep, floor_layers)
    log(f"axes: published {tuple(axis_pub.shape)}; ours {'yes' if axis_ours is not None else 'absent'}; "
        f"refusal {'yes' if refusal is not None else 'no'}; sweep {sweep}; floor {floor_layers}; backend {b.backend}")

    done, rows = set(), []
    if os.path.exists(out_csv):
        rows = list(csv.DictReader(open(out_csv)))
        done = {(r["stimulus_id"], int(r["sample"])) for r in rows}
        log(f"resuming: {len(done)} samples done")

    jobs = [(s, k) for s in stim for k in range(args.n_samples) if (s["id"], k) not in done]
    t0 = time.time()
    for st in range(0, len(jobs), args.batch):
        chunk = jobs[st:st + args.batch]
        convs = [[{"role": "user", "content": s["prompt"]}] for s, _ in chunk]
        seed = args.seed + st
        if cap_ctx:
            with cap_ctx:
                outs = generate_batch(b, convs, args.max_new_tokens, 0.7, 0.9, seed=seed)
        else:
            outs = generate_batch(b, convs, args.max_new_tokens, 0.7, 0.9, seed=seed)
        for (s, k), c, o in zip(chunk, convs, outs):
            o = strip_empty_think(o) or " "
            conv = c + [{"role": "assistant", "content": o}]
            if cap_ctx and not args.capping_measure_uncapped:
                with cap_ctx:
                    res, n_used, n_tok = readout(b, conv, args.layer, sweep, axis_pub, refusal, floor_items, args.exclude_code)
            else:
                res, n_used, n_tok = readout(b, conv, args.layer, sweep, axis_pub, refusal, floor_items, args.exclude_code)
            P = res.get(args.layer, {})
            row = {"arm": args.name, "stimulus_id": s["id"], "domain": s.get("domain"), "topic_id": s.get("topic_id"),
                   "register": s.get("register"), "tightness": s.get("tightness") or s.get("tightness_level"),
                   "cell": s.get("cell"), "sample": k, "model": args.model, "layer": args.layer,
                   "capping": args.capping_experiment if args.capping else "",
                   "projection_published": P.get("proj", ""),
                   "projection_ours": float(P["mean"] @ unit(axis_ours[args.layer])) if (axis_ours is not None and "mean" in P) else "",
                   "projection_refusal": P.get("refusal", ""),
                   "n_response_tokens": n_used, "n_tokens_span": n_tok,
                   "prompt_sha256": sha256(s["prompt"]), "response_sha256": sha256(o), "response": o, "backend": b.backend}
            for l in sweep:
                row[f"proj_L{l}"] = res.get(l, {}).get("proj", "")
            for d, v in enumerate(P.get("deciles", [""] * 10)):
                row[f"tok_decile_{d}"] = v
            fr = [res.get(l, {}).get("floor") for l in floor_layers]
            for l, v in zip(floor_layers, fr):
                row[f"floor_frac_L{l}"] = "" if v is None else v
            fr = [v for v in fr if v is not None]
            row["floor_frac_mean"] = sum(fr) / len(fr) if fr else ""
            rows.append(row)
        with open(out_csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
        log(f"{min(st + args.batch, len(jobs))}/{len(jobs)} samples ({time.time() - t0:.0f}s)")
    log(f"wrote {out_csv}: {len(rows)} rows")
    free_model(b)


if __name__ == "__main__":
    main()
