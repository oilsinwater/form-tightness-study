"""smoke_test.py — exercise common.py on a small model (Qwen/Qwen3-0.6B) so the
code paths (spans, hooks/nnsight, batched means, generation, capping hook) are
verified before the 32B weights are available. Not part of the study results."""
import sys, torch
from common import *

name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen3-0.6B"
b = load_model(name, min_free_gb=2)
conv = [{"role": "user", "content": "Write a haiku about rain and show `x = 1` in code."},
        {"role": "assistant", "content": "<think>\n\n</think>\n\nRain taps the window\n\n```python\nx = 1\n```\nsoft gray afternoon."},
        {"role": "user", "content": "Another?"},
        {"role": "assistant", "content": "Puddles hold the sky."}]
full_ids, spans = turn_spans(b, conv)
print("seq len", len(full_ids))
for s in spans:
    print(s["turn"], s["role"], s["start"], s["end"], s["n_tokens"], repr(b.tok.decode(full_ids[s["start"]:s["end"]]))[:80])
L = b.n_layers // 2
m, info = assistant_turn_means(b, conv, [L], exclude_code=True)
m2, _ = assistant_turn_means(b, conv, [L], exclude_code=False)
print("means", m.shape, info, "code-excl differs:", bool((m - m2).abs().max() > 0))
# consistency: batched single-conv vs unbatched
mb = batch_response_means(b, [conv[:2], conv[:2] + conv[2:]], [L], exclude_code=False)
print("batched", mb.shape, "diff vs single (turn mean):", float((mb[1, 0] - m2[:, 0].mean(0)).abs().max()))
# generation
outs = generate_batch(b, [[{"role": "user", "content": "Say hi in five words."}], [{"role": "user", "content": "Name a color."}]], max_new_tokens=20, seed=0)
print("gen", [strip_empty_think(o) for o in outs])
# capping hook on a random unit vector
H = b.model.config.hidden_size
iv = [{"layer": L, "vector": torch.randn(H), "cap": 0.0}]
with CappingHooks(b, iv):
    outs2 = generate_batch(b, [[{"role": "user", "content": "Say hi in five words."}]], max_new_tokens=10, seed=0)
print("capped gen", outs2)
print("backend", b.backend)
free_model(b)
