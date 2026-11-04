"""
common.py — shared model loading, activation reading and projection for the
form-tightness study.

Replicates the semantics of safety-research/assistant-axis
(assistant_axis/internals/conversation.py, spans.py, activations.py, axis.py):
  * chat formatting via tokenizer.apply_chat_template(add_generation_prompt=False,
    enable_thinking=False for Qwen)
  * per-assistant-turn MEAN of post-block residual-stream activations over the
    response tokens (ConversationEncoder.build_turn_spans), excluding
    <think>...</think> spans (Qwen) and — optionally — fenced/inline code
    (SpanMapper.map_spans_no_code / ConversationEncoder.code_block_token_mask)
  * project(acts, axis, layer) == assistant_axis.axis.project(normalize=True)

We import ConversationEncoder directly from the cloned repo (installed editable
on raphael) so the span logic is literally theirs.

Activation reading: the model is wrapped in nnsight.LanguageModel; if nnsight
tracing works on the 4-bit model it is used, otherwise we fall back to plain
torch forward hooks on model.model.layers[i] (output[0]) — which is exactly what
the repo's own ActivationExtractor does. The backend actually used is recorded
in ModelBundle.backend and printed at load time.
"""
from __future__ import annotations

import gc
import json
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from huggingface_hub import hf_hub_download

# Repo imports (assistant_axis is installed editable; generation.py pulls vllm so
# import the submodules directly, not the package root).
from assistant_axis.internals.conversation import ConversationEncoder  # noqa: E402
from assistant_axis.axis import project as _aa_project  # noqa: E402

QWEN = os.environ.get("FT_QWEN_MODEL", "Qwen/Qwen3-32B")  # env override only for smoke tests
GEMMA = "google/gemma-2-27b-it"
GEMMA_FALLBACK = "unsloth/gemma-2-27b-it-bnb-4bit"
AXIS_REPO = "lu-christina/assistant-axis-vectors"
HOME = os.path.expanduser("~")
FT = os.path.join(HOME, "form-tightness")
OUTPUTS = os.path.join(FT, "outputs")
RESULTS = os.path.join(FT, "results")
REPO = os.path.join(FT, "assistant-axis")
os.makedirs(OUTPUTS, exist_ok=True)
os.makedirs(RESULTS, exist_ok=True)

MODEL_INFO = {
    "qwen": {"hf": QWEN, "layer": 32, "n_layers": 64, "hidden": 5120,
             "axis_file": "qwen-3-32b/assistant_axis.pt",
             "default_file": "qwen-3-32b/default_vector.pt",
             "capping_file": "qwen-3-32b/capping_config.pt", "short_name": "Qwen"},
    "gemma": {"hf": GEMMA, "layer": 22, "n_layers": 46, "hidden": 4608,
              "axis_file": "gemma-2-27b/assistant_axis.pt",
              "default_file": "gemma-2-27b/default_vector.pt",
              "capping_file": "gemma-2-27b/capping_config.pt", "short_name": "Gemma"},
}


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def family(model_name: str) -> str:
    m = model_name.lower()
    if "qwen" in m:
        return "qwen"
    if "gemma" in m:
        return "gemma"
    raise ValueError(model_name)


def chat_kwargs_for(model_name: str) -> dict:
    """Extra apply_chat_template kwargs: Qwen3 gets enable_thinking=False."""
    return {"enable_thinking": False} if family(model_name) == "qwen" else {}


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
@dataclass
class ModelBundle:
    name: str
    model: torch.nn.Module
    tok: AutoTokenizer
    encoder: ConversationEncoder
    nn: object = None            # nnsight LanguageModel wrapper (may be None)
    backend: str = "hooks"       # "nnsight" or "hooks"
    chat_kwargs: dict = field(default_factory=dict)

    @property
    def layers(self):
        return self.model.model.layers

    @property
    def n_layers(self) -> int:
        return len(self.layers)

    @property
    def device(self):
        return self.model.device


def _patch_chat_template(tok):
    """transformers>=5: apply_chat_template(tokenize=True) returns a BatchEncoding
    by default; the repo's ConversationEncoder expects a flat list of ids.
    Force return_dict=False for tokenize=True calls (same ids, old return type)."""
    orig = tok.apply_chat_template

    def act(*a, **k):
        if k.get("tokenize", False) and "return_dict" not in k:
            k["return_dict"] = False
        return orig(*a, **k)
    tok.apply_chat_template = act


def bnb_config() -> BitsAndBytesConfig:
    return BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                              bnb_4bit_compute_dtype=torch.bfloat16,
                              bnb_4bit_use_double_quant=True)


def gpu_free_gb() -> float:
    free, total = torch.cuda.mem_get_info(0)
    return free / 1e9


def load_model(model_name: str = QWEN, try_nnsight: bool = True, min_free_gb: float = 19.0) -> ModelBundle:
    """Load `model_name` in 4-bit NF4 on cuda:0 and wrap with nnsight."""
    free = gpu_free_gb()
    log(f"loading {model_name}; GPU free {free:.1f} GB")
    if free < min_free_gb:
        raise RuntimeError(f"only {free:.1f} GB free on GPU; need >= {min_free_gb}")
    tok = AutoTokenizer.from_pretrained(model_name)
    _patch_chat_template(tok)
    prequant = "bnb-4bit" in model_name.lower()
    kw = dict(device_map="cuda:0", dtype=torch.bfloat16, low_cpu_mem_usage=True)
    if not prequant:
        kw["quantization_config"] = bnb_config()
    model = AutoModelForCausalLM.from_pretrained(model_name, **kw)
    model.eval()
    model.generation_config.pad_token_id = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token
    enc = ConversationEncoder(tok, model_name=model_name)
    b = ModelBundle(name=model_name, model=model, tok=tok, encoder=enc,
                    chat_kwargs=chat_kwargs_for(model_name))
    log(f"loaded; {b.n_layers} layers; GPU used {torch.cuda.memory_allocated()/1e9:.1f} GB")
    if try_nnsight:
        _attach_nnsight(b)
    return b


def _attach_nnsight(b: ModelBundle):
    """Wrap with nnsight and verify a trace reproduces the hook reading."""
    try:
        from nnsight import LanguageModel
        nn = LanguageModel(b.model, tokenizer=b.tok)
        ids = b.tok("hello there", return_tensors="pt").input_ids.to(b.device)
        L = b.n_layers // 2
        with torch.inference_mode():
            with nn.trace(ids):
                h = nn.model.layers[L].output.save()
            h_nn = (h[0] if isinstance(h, tuple) else h).detach().float().cpu()
            h_hook = _collect_hooks(b, ids, None, [L])[L][0].float()
        diff = (h_nn[0] - h_hook).abs().max().item()
        if h_nn.shape[-2:] == h_hook.shape and diff < 1e-2:
            b.nn, b.backend = nn, "nnsight"
            log(f"nnsight wrapper OK (max |nnsight-hook| = {diff:.2e}); backend=nnsight")
        else:
            b.nn, b.backend = nn, "hooks"
            log(f"nnsight trace disagrees with hooks (diff {diff}); backend=hooks")
    except Exception as e:  # noqa: BLE001
        b.nn, b.backend = None, "hooks"
        log(f"nnsight wrap failed ({type(e).__name__}: {str(e)[:200]}); backend=hooks (forward hooks on model.model.layers[i] output[0])")


def free_model(b: Optional[ModelBundle]):
    if b is None:
        return
    try:
        del b.nn
    except Exception:
        pass
    del b.model
    gc.collect()
    torch.cuda.synchronize()
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
    log(f"freed model; GPU allocated {torch.cuda.memory_allocated()/1e9:.2f} GB, free {gpu_free_gb():.1f} GB")


# --------------------------------------------------------------------------- #
# Reading residual-stream activations (post-block output of layers[i])
# --------------------------------------------------------------------------- #
def _collect_hooks(b: ModelBundle, input_ids, attention_mask, layers: Sequence[int],
                   reducer: Optional[Callable[[int, torch.Tensor], torch.Tensor]] = None) -> Dict[int, torch.Tensor]:
    out: Dict[int, torch.Tensor] = {}
    handles = []

    def mk(i):
        def hook(_m, _inp, output):
            h = output[0] if isinstance(output, tuple) else output
            out[i] = reducer(i, h) if reducer else h.detach().cpu()
        return hook

    for i in layers:
        handles.append(b.layers[i].register_forward_hook(mk(i)))
    try:
        with torch.inference_mode():
            b.model(input_ids=input_ids, attention_mask=attention_mask, use_cache=False)
    finally:
        for h in handles:
            h.remove()
    return out


def _collect_nnsight(b: ModelBundle, input_ids, attention_mask, layers, reducer=None):
    saved = {}
    with torch.inference_mode():
        with b.nn.trace({"input_ids": input_ids, "attention_mask": attention_mask} if attention_mask is not None else input_ids):
            for i in layers:
                saved[i] = b.nn.model.layers[i].output.save()
    out = {}
    for i in layers:
        h = saved[i]
        h = (h[0] if isinstance(h, tuple) else h).detach()  # decoder layer may return Tensor or (Tensor, ...)
        out[i] = reducer(i, h) if reducer else h.cpu()
    return out


def collect_hidden(b: ModelBundle, input_ids: torch.Tensor, attention_mask: Optional[torch.Tensor],
                   layers: Sequence[int], reducer=None) -> Dict[int, torch.Tensor]:
    """Return {layer: tensor} of residual activations at the output of block `layer`.
    Without a reducer each tensor is (B, T, H) on CPU (bf16). With a reducer,
    reducer(layer, hidden_gpu) is stored instead (lets us avoid moving 64 layers
    of 8k-token activations to CPU)."""
    if b.backend == "nnsight" and b.nn is not None:
        try:
            return _collect_nnsight(b, input_ids, attention_mask, layers, reducer)
        except Exception as e:  # noqa: BLE001
            log(f"nnsight trace failed at runtime ({type(e).__name__}); switching backend to hooks")
            b.backend = "hooks"
    return _collect_hooks(b, input_ids, attention_mask, layers, reducer)


# --------------------------------------------------------------------------- #
# Conversations -> per-assistant-turn mean activations
# --------------------------------------------------------------------------- #
def turn_spans(b: ModelBundle, conversation: List[Dict[str, str]]):
    """(full_ids, spans) using the repo's ConversationEncoder.build_turn_spans.
    spans: dicts with turn, role, start, end (exclusive), n_tokens, text."""
    return b.encoder.build_turn_spans(conversation, **b.chat_kwargs)


def include_mask_for_span(b: ModelBundle, span: dict, exclude_code: bool) -> torch.Tensor:
    """Boolean mask over the span's tokens (True = include in mean).
    Mirrors SpanMapper.map_spans_no_code: code mask computed on the raw text,
    truncated/padded to the span length."""
    n = span["end"] - span["start"]
    if not exclude_code:
        return torch.ones(n, dtype=torch.bool)
    ex = b.encoder.code_block_token_mask(span["text"])
    if len(ex) > n:
        ex = ex[:n]
    elif len(ex) < n:
        ex = torch.cat([ex, torch.zeros(n - len(ex), dtype=torch.bool)])
    return ~ex


def conversation_token_count(b: ModelBundle, conversation) -> int:
    return len(b.tok.apply_chat_template(conversation, tokenize=True, add_generation_prompt=False, **b.chat_kwargs))


def assistant_turn_means(b: ModelBundle, conversation: List[Dict[str, str]], layers: Sequence[int],
                         exclude_code: bool = True):
    """Run the whole conversation as ONE sequence and return
    (means, info) where means is (n_assistant_turns, len(layers), H) float32 CPU
    and info is a list of dicts (turn index within conversation, n_tokens, n_used).
    The mean is over response tokens (think-spans removed by the encoder; code
    tokens removed if exclude_code)."""
    full_ids, spans = turn_spans(b, conversation)
    ids = torch.tensor([full_ids], device=b.device)
    a_spans = [s for s in spans if s["role"] == "assistant"]
    masks = [include_mask_for_span(b, s, exclude_code) for s in a_spans]

    def reducer(_i, h):  # h: (1, T, H) on GPU
        rows = []
        for s, m in zip(a_spans, masks):
            seg = h[0, s["start"]:s["end"], :]
            if m.any():
                rows.append(seg[m.to(seg.device)].float().mean(0))
            else:
                rows.append(torch.full((h.shape[-1],), float("nan"), device=h.device))
        return torch.stack(rows).cpu() if rows else torch.zeros(0, h.shape[-1])

    out = collect_hidden(b, ids, None, list(layers), reducer=reducer)
    means = torch.stack([out[i] for i in layers], dim=1) if a_spans else torch.zeros(0, len(layers), b.model.config.hidden_size)
    # map assistant spans back to conversation message indices
    msg_idx = [k for k, m in enumerate(conversation) if m["role"] in ("user", "assistant")]
    info = []
    for s, m in zip(a_spans, masks):
        info.append({"message_index": msg_idx[s["turn"]], "turn": s["turn"], "start": s["start"], "end": s["end"],
                     "n_tokens": s["n_tokens"], "n_used": int(m.sum()), "seq_len": len(full_ids)})
    return means, info


def batch_response_means(b: ModelBundle, conversations: List[List[Dict[str, str]]], layers: Sequence[int],
                         exclude_code: bool = False, max_length: int = 2048):
    """Batched (right-padded) version for single-turn conversations: returns
    (n_conv, len(layers), H) float32 — mean over assistant response tokens of
    ALL assistant turns (the repo's 2_activations.py averages turns if >1).
    exclude_code=False matches the repo's 2_activations.py (map_spans)."""
    per_conv = []
    for conv in conversations:
        full_ids, spans = turn_spans(b, conv)
        if len(full_ids) > max_length:
            full_ids = full_ids[:max_length]
        a_spans = [s for s in spans if s["role"] == "assistant" and s["start"] < len(full_ids)]
        for s in a_spans:
            s["end"] = min(s["end"], len(full_ids))
        per_conv.append((full_ids, a_spans, [include_mask_for_span(b, s, exclude_code) for s in a_spans]))
    T = max(len(p[0]) for p in per_conv)
    pad = b.tok.pad_token_id
    ids = torch.full((len(per_conv), T), pad, dtype=torch.long)
    att = torch.zeros((len(per_conv), T), dtype=torch.long)
    for k, (fi, _, _) in enumerate(per_conv):
        ids[k, :len(fi)] = torch.tensor(fi)
        att[k, :len(fi)] = 1
    ids, att = ids.to(b.device), att.to(b.device)

    def reducer(_i, h):
        rows = []
        for k, (_fi, a_spans, masks) in enumerate(per_conv):
            vecs = []
            for s, m in zip(a_spans, masks):
                seg = h[k, s["start"]:s["end"], :]
                mm = m[: seg.shape[0]].to(seg.device)
                if mm.any():
                    vecs.append(seg[mm].float().mean(0))
            rows.append(torch.stack(vecs).mean(0) if vecs else torch.full((h.shape[-1],), float("nan"), device=h.device))
        return torch.stack(rows).cpu()

    out = collect_hidden(b, ids, att, list(layers), reducer=reducer)
    return torch.stack([out[i] for i in layers], dim=1)


# --------------------------------------------------------------------------- #
# Axis / projection
# --------------------------------------------------------------------------- #
def load_published_axis(fam: str) -> torch.Tensor:
    if os.environ.get("FT_AXIS_OVERRIDE"):   # smoke tests with small models only
        return _safe_load(os.environ["FT_AXIS_OVERRIDE"])
    p = hf_hub_download(AXIS_REPO, MODEL_INFO[fam]["axis_file"], repo_type="dataset")
    ax = _safe_load(p)
    if isinstance(ax, dict):
        ax = ax.get("axis", ax)
    return ax


def load_capping_config(fam: str = "qwen") -> dict:
    if os.environ.get("FT_CAPPING_OVERRIDE"):   # smoke tests only
        return _safe_load(os.environ["FT_CAPPING_OVERRIDE"])
    p = hf_hub_download(AXIS_REPO, MODEL_INFO[fam]["capping_file"], repo_type="dataset")
    return _safe_load(p)


def _safe_load(p):
    """Published vectors are plain tensors / dicts of tensors+str -> weights_only=True suffices."""
    return torch.load(p, map_location="cpu", weights_only=True)


def project(acts: torch.Tensor, axis: torch.Tensor, layer: int) -> float:
    """assistant_axis.axis.project with normalize=True (unit axis at `layer`).
    acts: (n_layers, H) or (H,)."""
    return _aa_project(acts, axis, layer, normalize=True)


def project_rows(acts_layer: torch.Tensor, axis: torch.Tensor, layer: int) -> torch.Tensor:
    """acts_layer: (n, H) activations already at `layer` -> (n,) projections on the unit axis."""
    ax = axis[layer].float()
    ax = ax / (ax.norm() + 1e-8)
    return acts_layer.float() @ ax


def cosine_per_layer(v1: torch.Tensor, v2: torch.Tensor) -> List[float]:
    v1, v2 = v1.float(), v2.float()
    c = (v1 / (v1.norm(dim=1, keepdim=True) + 1e-8) * (v2 / (v2.norm(dim=1, keepdim=True) + 1e-8))).sum(1)
    return [float(x) for x in c]


# --------------------------------------------------------------------------- #
# Generation (transformers.generate, batched, left padding)
# --------------------------------------------------------------------------- #
def generate_batch(b: ModelBundle, conversations: List[List[Dict[str, str]]], max_new_tokens: int = 512,
                   temperature: float = 0.7, top_p: float = 0.9, seed: Optional[int] = None) -> List[str]:
    """Sample one completion per conversation (repo defaults: 0.7 / 0.9 / 512,
    thinking off). Left padding so all sequences end at the generation prompt."""
    prompts = [b.tok.apply_chat_template(c, tokenize=False, add_generation_prompt=True, **b.chat_kwargs) for c in conversations]
    b.tok.padding_side = "left"
    enc = b.tok(prompts, return_tensors="pt", padding=True, add_special_tokens=False).to(b.device)
    if seed is not None:
        torch.manual_seed(seed)
    with torch.inference_mode():
        out = b.model.generate(**enc, do_sample=True, temperature=temperature, top_p=top_p, top_k=0,
                               max_new_tokens=max_new_tokens, pad_token_id=b.tok.pad_token_id)
    gen = out[:, enc.input_ids.shape[1]:]
    texts = b.tok.batch_decode(gen, skip_special_tokens=True)
    return [t.strip() for t in texts]


def strip_empty_think(text: str) -> str:
    """Qwen3 with thinking off emits '<think>\\n\\n</think>\\n\\n' first; remove it from stored text."""
    import re
    return re.sub(r"^\s*<think>\s*</think>\s*", "", text, count=1)


# --------------------------------------------------------------------------- #
# Capping hook (published capping config) — used by arm_run.py
# --------------------------------------------------------------------------- #
class CappingHooks:
    """Activation capping: at each listed layer, along unit vector u with cap c,
    h <- h - max(0, h·u - c) u at all positions (applied inside generate via
    forward hooks on model.model.layers[i])."""

    def __init__(self, b: ModelBundle, interventions: List[dict]):
        self.b = b
        self.items = []
        for it in interventions:
            u = it["vector"].float()
            u = (u / (u.norm() + 1e-8)).to(b.device, dtype=torch.bfloat16)
            self.items.append((int(it["layer"]), u, float(it["cap"])))
        self.handles = []

    def _mk(self, u, cap):
        def hook(_m, _inp, output):
            h = output[0] if isinstance(output, tuple) else output
            proj = (h.float() @ u.float())            # (B, T)
            excess = torch.clamp(proj - cap, min=0.0)
            h2 = (h.float() - excess.unsqueeze(-1) * u.float()).to(h.dtype)
            if isinstance(output, tuple):
                return (h2,) + tuple(output[1:])
            return h2
        return hook

    def __enter__(self):
        for layer, u, cap in self.items:
            self.handles.append(self.b.layers[layer].register_forward_hook(self._mk(u, cap)))
        return self

    def __exit__(self, *a):
        for h in self.handles:
            h.remove()
        self.handles = []


def capping_interventions(cfg: dict, experiment_id: str = "layers_46:54-p0.25") -> List[dict]:
    """Resolve an experiment from capping_config.pt into [{layer, vector, cap}]."""
    exps = {e["id"]: e for e in cfg["experiments"]}
    if experiment_id not in exps:
        raise KeyError(f"{experiment_id} not in {list(exps)}")
    out = []
    for iv in exps[experiment_id]["interventions"]:
        v = cfg["vectors"][iv["vector"]]
        out.append({"layer": v["layer"], "vector": v["vector"], "cap": iv["cap"]})
    return out


def sha256(s: str) -> str:
    import hashlib
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def read_env_key(name: str, path: str = os.path.join(HOME, ".hermes", ".env")) -> Optional[str]:
    if os.environ.get(name):
        return os.environ[name]
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith(name + "="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return None
