"""
check_c_rescore_transcripts.py — Pre-stimulus check (c).

Per-assistant-turn projection on the published Assistant Axis for
  * the 6 Qwen3-32B case-study transcripts (axis qwen-3-32b, layer 32)
  * the 2 Gemma-2-27B persona-drift transcripts (axis gemma-2-27b, layer 22)
with the whole conversation in context (one forward pass per conversation),
mean over response tokens of each assistant turn (think spans and code blocks
excluded; repo ConversationEncoder/SpanMapper semantics).

Context budget MAX_TOKENS=8192. If a conversation does not fit, we truncate
from the LEFT by whole user+assistant pairs: every assistant turn is scored
with the longest left-truncated context (starting at a user turn) that fits.
Turns whose full prefix fits are scored in one pass with the full prefix;
later turns get one pass each. Each row records context_start_message,
context_tokens and truncated.

Output: results/check_c_projections.csv
columns: transcript, turn_index, user_text_sha256, user_text,
assistant_text_sha256, projection_L32, n_response_tokens (+ extra columns:
model, layer, assistant_text, n_tokens_span, context_start_message,
context_tokens, truncated, backend).
'projection_L32' is the projection at the model's target layer (32 for Qwen,
22 for Gemma) — kept under one column name as the spec requires; 'layer' says which.
"""
import csv, glob, json, os, sys, time
import torch
from common import *

MAX_TOKENS = 8192
DATA = os.path.join(FT, "data", "transcripts")
OUT_CSV = os.path.join(RESULTS, "check_c_projections.csv")
COLS = ["transcript", "turn_index", "user_text_sha256", "user_text", "assistant_text_sha256", "projection_L32",
        "n_response_tokens", "model", "layer", "assistant_text", "n_tokens_span", "context_start_message",
        "context_tokens", "truncated", "backend", "exclude_code"]


def score_conversation(b, conv, axis, layer, name):
    """Yield rows for every assistant turn."""
    conv = [m for m in conv if m["role"] in ("user", "assistant", "system")]
    # drop empty-content turns defensively (would break the template)
    a_idx = [i for i, m in enumerate(conv) if m["role"] == "assistant"]
    rows = {}
    total = conversation_token_count(b, conv)
    log(f"{name}: {len(conv)} messages, {len(a_idx)} assistant turns, {total} tokens")

    def run(window_conv, start_msg, truncated, want=None):
        means, info = assistant_turn_means(b, window_conv, [layer], exclude_code=True)
        proj = project_rows(means[:, 0, :], axis, layer)
        for k, inf in enumerate(info):
            gi = start_msg + inf["message_index"]      # index into full conv
            if want is not None and gi not in want:
                continue
            if gi in rows:
                continue
            user_msg = conv[gi - 1]["content"] if gi >= 1 and conv[gi - 1]["role"] == "user" else ""
            rows[gi] = {
                "transcript": name, "turn_index": a_idx.index(gi), "user_text_sha256": sha256(user_msg),
                "user_text": user_msg, "assistant_text_sha256": sha256(conv[gi]["content"]),
                "projection_L32": float(proj[k]), "n_response_tokens": inf["n_used"], "model": b.name, "layer": layer,
                "assistant_text": conv[gi]["content"], "n_tokens_span": inf["n_tokens"],
                "context_start_message": start_msg, "context_tokens": inf["seq_len"], "truncated": truncated,
                "backend": b.backend, "exclude_code": True}

    if total <= MAX_TOKENS:
        run(conv, 0, False)
    else:
        # 1) longest full prefix that fits (ending on an assistant turn)
        fit_end = None
        for gi in a_idx:
            if conversation_token_count(b, conv[:gi + 1]) <= MAX_TOKENS:
                fit_end = gi
            else:
                break
        if fit_end is not None:
            run(conv[:fit_end + 1], 0, False)
        # 2) remaining turns: maximal suffix starting at a user turn that fits
        user_starts = [i for i, m in enumerate(conv) if m["role"] == "user"]
        for gi in a_idx:
            if gi in rows:
                continue
            start = None
            for us in user_starts:                   # earliest start that fits
                if us > gi:
                    break
                if conversation_token_count(b, conv[us:gi + 1]) <= MAX_TOKENS:
                    start = us
                    break
            if start is None:
                log(f"  turn at message {gi} does not fit even alone; skipped")
                continue
            run(conv[start:gi + 1], start, True, want={gi})
            log(f"  msg {gi}: context msgs {start}..{gi}")
    return [rows[gi] for gi in sorted(rows)]


def run_stage(only_flag):
    """Each model stage runs in its OWN process: in-process free_model() of the
    4-bit 32B model did not return the GPU memory (observed 18 GB still held),
    so the parent never loads a model itself."""
    import subprocess
    cmd = [sys.executable, os.path.abspath(__file__), only_flag, "--resume"]
    log("running: " + " ".join(cmd))
    return subprocess.run(cmd).returncode


def main():
    if "--qwen-only" not in sys.argv and "--gemma-only" not in sys.argv:
        rc1 = run_stage("--qwen-only")
        rc2 = run_stage("--gemma-only")
        log(f"stages exit codes: qwen={rc1} gemma={rc2}")
        sys.exit(rc1 or rc2)

    t0 = time.time()
    all_rows = []
    done_names = set()
    if os.path.exists(OUT_CSV) and "--resume" in sys.argv:
        with open(OUT_CSV) as f:
            all_rows = list(csv.DictReader(f))
        done_names = {r["transcript"] for r in all_rows}
        log(f"resuming; done: {sorted(done_names)}")

    def flush():
        with open(OUT_CSV, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            w.writeheader()
            for r in all_rows:
                w.writerow(r)

    jobs = []
    if "--qwen-only" in sys.argv:
        jobs.append(("qwen", QWEN, 32, sorted(glob.glob(os.path.join(DATA, "case_studies", "qwen-3-32b", "*.json")))))
    if "--gemma-only" in sys.argv:
        gem = [os.path.join(DATA, "persona_drift", "philosophy.json"), os.path.join(DATA, "persona_drift", "writing.json")]
        jobs.append(("gemma", GEMMA, 22, gem))
    for fam, model_name, layer, files in jobs:
        files = [f for f in files if os.path.basename(f) not in done_names]
        if not files:
            log(f"{fam}: nothing to do")
            continue
        b = None
        if fam == "gemma":
            try:
                b = load_model(model_name)
            except Exception as e:  # noqa: BLE001
                log(f"gated gemma load failed ({type(e).__name__}: {str(e)[:200]}); falling back to {GEMMA_FALLBACK}")
                b = load_model(GEMMA_FALLBACK)
        else:
            b = load_model(model_name)
        axis = load_published_axis(fam)
        log(f"{fam}: axis {tuple(axis.shape)}, layer {layer}, backend {b.backend}")
        for f in files:
            d = json.load(open(f))
            name = os.path.basename(f)
            assert fam in d.get("model", model_name).lower(), (name, d.get("model"))
            rows = score_conversation(b, d["conversation"], axis, layer, name)
            all_rows.extend(rows)
            flush()
            pr = [r["projection_L32"] for r in rows]
            log(f"  {name}: {len(rows)} turns; proj mean {sum(pr)/len(pr):.2f} min {min(pr):.2f} max {max(pr):.2f}")
        free_model(b)
    log(f"wrote {OUT_CSV} ({len(all_rows)} rows) in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
