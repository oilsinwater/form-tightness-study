"""
check_a_derive_axis.py — Pre-stimulus check (a): scaled re-derivation of the
Qwen3-32B Assistant Axis with the repo's own prompts, a 4-bit model, HF
generate (no vllm) and an external judge.

Phases (each resumable; outputs under ~/form-tightness/outputs/check_a/):
  1. select 48 roles stratified by published L32 projection quartile
     (external-checks/qwen_role_proj_L32.json; 12 per quartile; seed 20261030)
  2. generate: per role 5 'instruction' pos prompts × first 12 extraction
     questions (60 gens); default.json 5 prompts × first 48 questions (240 gens)
     temp 0.7, top_p 0.9, max_new_tokens 512, thinking off, batched, left pad
     -> responses/<role>.jsonl
  3. activations: mean response-token activations at ALL layers for each
     response (single-turn conversation system+question+response; repo
     2_activations.py semantics = map_spans, i.e. no code exclusion)
     -> acts/<role>.pt  (n, 64, 5120) fp16
  4. judge: role eval_prompt.format(question, answer) via CommandCode
     (OpenAI-compatible), model deepseek/deepseek-v4.1-flash, temperature 0,
     parse single integer 0-3 from message.content -> scores/<role>.jsonl
  5. axis = mean(default acts) − mean(per-role mean of score==3 acts)
     -> results/check_a_axis_ours.pt, results/check_a_cosine.json
"""
import argparse, concurrent.futures as cf, json, os, random, re, sys, time
import torch, requests
from common import *

CA = os.path.join(OUTPUTS, "check_a")
RESP_DIR, ACT_DIR, SCORE_DIR = [os.path.join(CA, d) for d in ("responses", "acts", "scores")]
for d in (RESP_DIR, ACT_DIR, SCORE_DIR):
    os.makedirs(d, exist_ok=True)
ROLES_DIR = os.path.join(REPO, "data", "roles", "instructions")
QFILE = os.path.join(REPO, "data", "extraction_questions.jsonl")
PROJ_FILE = os.path.join(FT, "data", "qwen_role_proj_L32.json")
SEED = 20261030
N_PER_Q = 12
N_Q_ROLE, N_Q_DEFAULT = 12, 48
if os.environ.get("FT_DEBUG_NQ"):  # smoke tests only
    N_Q_ROLE = N_Q_DEFAULT = int(os.environ["FT_DEBUG_NQ"])
MIN_SCORE3 = 20

JUDGE = {"base_url": "https://api.commandcode.ai/provider/v1", "model": "deepseek/deepseek-v4.1-flash",
         "alt_model": "deepseek/deepseek-v4-pro", "temperature": 0, "max_tokens": 2048, "max_tokens_retry": 8192, "key_env": "COMMANDCODE_API_KEY"}


# ----------------------------------------------------------------------------- roles
def select_roles():
    d = json.load(open(PROJ_FILE))
    names, proj = d["names"], d["proj_L32"]
    avail = {f[:-5] for f in os.listdir(ROLES_DIR) if f.endswith(".json")}
    pairs = sorted([(p, n) for n, p in zip(names, proj) if n in avail and n != "default"])
    n = len(pairs)
    quart = [pairs[i * n // 4:(i + 1) * n // 4] for i in range(4)]
    rng = random.Random(SEED)
    chosen = []
    for qi, q in enumerate(quart):
        pick = rng.sample(q, N_PER_Q)
        chosen += [{"role": nm, "published_proj_L32": p, "quartile": qi} for p, nm in sorted(pick)]
    return chosen


def load_questions(n):
    qs = [json.loads(l)["question"] for l in open(QFILE) if l.strip()]
    return qs[:n]


def role_prompts(role):
    d = json.load(open(os.path.join(ROLES_DIR, f"{role}.json")))
    return [p["pos"].replace("{model_name}", "Qwen") for p in d["instruction"]], d.get("eval_prompt", "")


def conv_for(instruction, question):
    msgs = []
    if instruction:
        msgs.append({"role": "system", "content": instruction})
    msgs.append({"role": "user", "content": question})
    return msgs


# ----------------------------------------------------------------------------- generate
def gen_role(b, role, n_q, batch_size):
    path = os.path.join(RESP_DIR, f"{role}.jsonl")
    done = set()
    if os.path.exists(path):
        for l in open(path):
            r = json.loads(l)
            done.add((r["prompt_index"], r["question_index"]))
    prompts, _ = role_prompts(role)
    qs = load_questions(n_q)
    todo = [(pi, qi) for pi in range(len(prompts)) for qi in range(len(qs)) if (pi, qi) not in done]
    if not todo:
        return 0
    with open(path, "a") as f:
        for s in range(0, len(todo), batch_size):
            chunk = todo[s:s + batch_size]
            convs = [conv_for(prompts[pi], qs[qi]) for pi, qi in chunk]
            outs = generate_batch(b, convs, max_new_tokens=512, temperature=0.7, top_p=0.9)
            for (pi, qi), c, o in zip(chunk, convs, outs):
                o = strip_empty_think(o)
                f.write(json.dumps({"role": role, "prompt_index": pi, "question_index": qi,
                                    "system_prompt": prompts[pi], "question": qs[qi], "response": o,
                                    "conversation": c + [{"role": "assistant", "content": o}]}) + "\n")
            f.flush()
    return len(todo)


def read_jsonl(p):
    return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []


# ----------------------------------------------------------------------------- activations
def acts_role(b, role, batch_size):
    path = os.path.join(ACT_DIR, f"{role}.pt")
    resp = read_jsonl(os.path.join(RESP_DIR, f"{role}.jsonl"))
    keys = [f"p{r['prompt_index']}_q{r['question_index']}" for r in resp]
    if os.path.exists(path):
        d = torch.load(path, weights_only=True)
        if d["keys"] == keys:
            return False
    acts = []
    for s in range(0, len(resp), batch_size):
        convs = [r["conversation"] for r in resp[s:s + batch_size]]
        acts.append(batch_response_means(b, convs, list(range(b.n_layers)), exclude_code=False, max_length=2048).to(torch.float16))
    torch.save({"keys": keys, "acts": torch.cat(acts)}, path)
    return True


# ----------------------------------------------------------------------------- judge
def judge_call(prompt, key, model, max_tokens=None):
    url = JUDGE["base_url"].rstrip("/") + "/chat/completions"
    body = {"model": model, "temperature": JUDGE["temperature"], "max_tokens": max_tokens or JUDGE["max_tokens"],
            "messages": [{"role": "user", "content": prompt}]}
    r = requests.post(url, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                      json=body, timeout=180)
    r.raise_for_status()
    msg = r.json()["choices"][0]["message"]
    content = (msg.get("content") or "").strip()
    return content, msg


def parse_score(content):
    if content is None:
        return None
    c = content.strip()
    if re.fullmatch(r"[0-3]", c):
        return int(c)
    m = re.search(r"\b([0-3])\b", c)       # tolerate 'Score: 2'
    return int(m.group(1)) if m else None


def judge_role(role, key, workers=8):
    path = os.path.join(SCORE_DIR, f"{role}.jsonl")
    done = {(r["prompt_index"], r["question_index"]) for r in read_jsonl(path) if r.get("score") is not None or r.get("final")}
    resp = read_jsonl(os.path.join(RESP_DIR, f"{role}.jsonl"))
    _, eval_prompt = role_prompts(role)
    todo = [r for r in resp if (r["prompt_index"], r["question_index"]) not in done]
    if not todo:
        return 0, 0

    def one(r):
        prompt = eval_prompt.format(question=r["question"], answer=r["response"])
        last_err, content, raw = None, None, None
        for attempt in range(2):                      # retry once
            try:
                # the judge emits reasoning tokens before content; 512 was too small
                # (finish_reason=length, empty content) so the retry gets a larger budget
                content, raw = judge_call(prompt, key, JUDGE["model"], JUDGE["max_tokens"] if attempt == 0 else JUDGE["max_tokens_retry"])
                sc = parse_score(content)
                if sc is not None:
                    return {"role": role, "prompt_index": r["prompt_index"], "question_index": r["question_index"],
                            "score": sc, "judge_content": content[:200], "attempts": attempt + 1, "final": True}
                last_err = f"unparseable content: {content[:100]!r}"
            except Exception as e:  # noqa: BLE001
                last_err = f"{type(e).__name__}: {str(e)[:200]}"
                time.sleep(2 + 3 * attempt)
        return {"role": role, "prompt_index": r["prompt_index"], "question_index": r["question_index"],
                "score": None, "error": last_err, "attempts": 2, "final": True}

    n_none = 0
    with open(path, "a") as f, cf.ThreadPoolExecutor(workers) as ex:
        for res in ex.map(one, todo):
            f.write(json.dumps(res) + "\n"); f.flush()
            n_none += res["score"] is None
    return len(todo), n_none


# ----------------------------------------------------------------------------- axis
def compute_axis(roles, log_fn=log):
    axis_pub = load_published_axis("qwen")
    d = torch.load(os.path.join(ACT_DIR, "default.pt"), weights_only=True)
    default_mean = d["acts"].float().mean(0)                       # (64,5120)
    role_vecs, kept, dropped, dist = [], [], [], {"0": 0, "1": 0, "2": 0, "3": 0, "None": 0}
    per_role = {}
    for r in roles:
        role = r["role"]
        a = torch.load(os.path.join(ACT_DIR, f"{role}.pt"), weights_only=True)
        scores = {f"p{s['prompt_index']}_q{s['question_index']}": s["score"] for s in read_jsonl(os.path.join(SCORE_DIR, f"{role}.jsonl"))}
        for k in a["keys"]:
            dist[str(scores.get(k))] += 1
        idx = [i for i, k in enumerate(a["keys"]) if scores.get(k) == 3]
        per_role[role] = {"n_responses": len(a["keys"]), "n_score3": len(idx), "quartile": r["quartile"],
                          "published_proj_L32": r["published_proj_L32"]}
        if len(idx) == 0:
            dropped.append(role); continue
        if len(idx) < MIN_SCORE3:
            log_fn(f"WARNING {role}: only {len(idx)} score==3 responses (< {MIN_SCORE3}); kept anyway")
            per_role[role]["below_min"] = True
        v = a["acts"][idx].float().mean(0)
        v_nan = torch.isnan(v).any().item()
        if v_nan:
            log_fn(f"WARNING {role}: NaN in mean activation; dropped"); dropped.append(role); continue
        role_vecs.append(v); kept.append(role)
    role_mean = torch.stack(role_vecs).mean(0)
    axis = default_mean - role_mean
    cos = cosine_per_layer(axis, axis_pub)
    TL = 32 if len(cos) > 32 else len(cos) // 2     # 32 for Qwen3-32B; fallback only for small smoke models
    # projections of our default / per-role vectors on the published unit axis, for reference
    out = {
        "n_roles_selected": len(roles), "n_roles_retained": len(kept), "roles_dropped_no_score3": dropped,
        "n_default_responses": int(d["acts"].shape[0]),
        "score_distribution_role_responses": dist,
        "cos_per_layer": cos, "cos_L32": cos[TL], "target_layer": TL,
        "axis_norm_L32_ours": float(axis[TL].norm()), "axis_norm_L32_published": float(axis_pub[TL].float().norm()),
        "per_role": per_role,
        "judge": {"provider": "CommandCode", "base_url": JUDGE["base_url"], "model": JUDGE["model"],
                  "temperature": JUDGE["temperature"], "max_tokens": JUDGE["max_tokens"], "max_tokens_retry": JUDGE["max_tokens_retry"],
                  "parsing": "single integer 0-3 from message.content; retry once; else None"},
        "generation": {"model": QWEN, "quant": "bnb nf4 double-quant bf16 compute", "temperature": 0.7, "top_p": 0.9,
                       "max_new_tokens": 512, "enable_thinking": False, "backend": "transformers.generate"},
        "activations": "mean over assistant response tokens, all 64 layers, repo map_spans semantics (no code exclusion), max_length 2048",
        "subset_ceiling_from_PLAN": {"stratified_k48_mean": 0.9885, "p05": 0.9806},
        "seed": SEED, "selection": "12 roles per published-L32-projection quartile, random.Random(20261030).sample",
    }
    torch.save(axis, os.path.join(RESULTS, "check_a_axis_ours.pt"))
    with open(os.path.join(RESULTS, "check_a_cosine.json"), "w") as f:
        json.dump(out, f, indent=1)
    log_fn(f"AXIS: cos@L{TL} = {cos[TL]:.4f}; retained {len(kept)}/{len(roles)} roles; scores {dist}")
    return out


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--act-batch", type=int, default=8)
    ap.add_argument("--phase", default="all", choices=["all", "select", "gen", "acts", "judge", "axis"])
    ap.add_argument("--n-roles", type=int, default=None, help="debug: use only first n selected roles")
    args = ap.parse_args()
    t0 = time.time()

    roles = select_roles()
    if args.n_roles:
        roles = roles[:args.n_roles]
    with open(os.path.join(CA, "selected_roles.json"), "w") as f:
        json.dump(roles, f, indent=1)
    log(f"selected {len(roles)} roles: {[r['role'] for r in roles]}")
    if args.phase == "select":
        return

    key = read_env_key(JUDGE["key_env"])
    if key is None:
        log("WARNING: COMMANDCODE_API_KEY not found; judge phase will fail")

    if args.phase in ("all", "gen", "acts"):
        b = load_model(QWEN)
        log(f"backend {b.backend}")
        if args.phase in ("all", "gen"):
            n = gen_role(b, "default", N_Q_DEFAULT, args.batch)
            log(f"default: generated {n} new ({time.time()-t0:.0f}s)")
            for i, r in enumerate(roles):
                n = gen_role(b, r["role"], N_Q_ROLE, args.batch)
                log(f"[{i+1}/{len(roles)}] {r['role']}: generated {n} new ({time.time()-t0:.0f}s)")
        if args.phase in ("all", "acts"):
            for name in ["default"] + [r["role"] for r in roles]:
                new = acts_role(b, name, args.act_batch)
                log(f"acts {name}: {'computed' if new else 'cached'} ({time.time()-t0:.0f}s)")
        free_model(b)

    if args.phase in ("all", "judge"):
        if key is None:
            raise SystemExit("no judge key")
        for i, r in enumerate(roles):
            n, n_none = judge_role(r["role"], key)
            log(f"judge [{i+1}/{len(roles)}] {r['role']}: {n} scored, {n_none} None ({time.time()-t0:.0f}s)")

    if args.phase in ("all", "axis"):
        compute_axis(roles)
    log(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
