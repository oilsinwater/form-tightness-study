---
type: project
date: 2026-10-30
status: working
---

# Plan — Does prompt-form tightness predict Assistant-Axis projection?

Built to be wrong in public. Every step below either produces a number a third party can recompute, or names what could not be obtained.

## 0. The question

**H1 (directional):** Looser prompt form (free verse, associative, no hard constraints) pushes the model's per-turn Assistant-Axis projection lower (away from the Assistant) than tight form (strict metrical/structural constraints such as Gwern's pressure-cooker spec), holding content, token count and base-model perplexity constant.

**H0 ("form doesn't matter"):** the tightness effect lies inside a TOST equivalence band.

The hypothesis comes from three places that never met: Lu et al. 2026 (projection drops in therapy/philosophy, holds in coding), Icaro Lab 2025/26 (poetic reformulation defeats refusal), Gerbrandt 2026 (a hand-built poem induces role bleed). None of them manipulated form while holding content fixed. This study does.

## 1. Phase 0 — what the primary artefacts actually contain

Done in-session on 2026-10-30. Full record: `external-checks/artefact-inventory.md`. Headlines:

| Asked for | Found |
|---|---|
| Role prompts | 275 roles × 5 system prompts + 240 extraction questions + 40 role-specific questions each (`data/roles/instructions/*.json`). `default.json` = 5 neutral prompts. |
| Judge rubric | Per-role `eval_prompt`, 0–3 scale; judge model `gpt-4.1-mini`, score=3 only goes into role vectors; `min_count=50`. |
| Layer index | Qwen3-32B target layer **32** of 64; Gemma-2-27B **22** of 46. Capping best setting `layers_46:54-p0.25`. |
| Chat template | HF `apply_chat_template`, Qwen with `enable_thinking=False`; `<think>` spans excluded from response-token mean; code blocks excluded (`SpanMapper`). Response-token mean, post-MLP residual stream. |
| Drift transcripts | **4 example conversations only** (1/domain), **no `projections` field** despite README, and none are Qwen (2× Llama-70B, 2× Gemma). 6 Qwen case-study transcripts (jailbreak/delusion/selfharm × unsteered/capped) exist, also without projections. |
| Published vectors | HF `lu-christina/assistant-axis-vectors`: per-layer axis, default vector, 275 role vectors, capping config, for all 3 models. |
| Gwern pressure-cooker v4.2 verbatim | **Not public.** gwern.net has the scansion key (verbatim) and the "STRICT TRIADIC v2" spec (verbatim); the v4.2 six-rule summary is Hollis Robbins' paraphrase. Cited as unpublished; no request made. |
| Gerbrandt transcripts | Prompt redacted in talk; transcripts not released. Cited as unpublished; no request made. |
| Icaro Lab prompt sets | 20 hand-crafted poems **not released**; AHB dataset (3,600 transformed prompts, 6 methods × 600) is on HF `icaro-lab/ahb` — harmful content, used only as a form reference, not as stimuli. |

Two things the artefacts told us that the wiki did not:
- Capping vector = exactly −axis (cos −1.0000); τ at layers 46–53 equals the default-Assistant projection on −axis. Capping is a **floor** on Assistant-ness at the default level.
- Reconstructing the axis from the 275 published role vectors reproduces the published axis at cos 0.9998 → the 5_axis.py formula is exactly what shipped.

## 2. Pre-stimulus checks (gate before any stimuli)

| Check | Method | Abort / pass rule | Status |
|---|---|---|---|
| (a) Re-derive Qwen3-32B axis | nnsight + bitsandbytes 4-bit, 48 roles stratified by published projection quartile, 5 prompts × 12 questions each (2,880 role gens) + default 5 × 48 (240 gens); judge gpt-4.1-mini via OpenRouter with the repo's eval_prompt; score=3 only; axis = mean(default) − mean(role). | cos(ours, published) at layer 32 ≥ 0.9 else abort. **Subset ceiling (computed from published vectors, CPU):** stratified k=48 gives mean 0.9885, 5th pct 0.9806. So a cos < 0.9 cannot be blamed on the subset; it would be the 4-bit model, our generations, or our judge. | code ready; GPU pending |
| (b) Refusal-direction cosine | Arditi et al. 2024 recipe: diff-in-means at the last instruction token, harmful (AdvBench-style) vs harmless (Alpaca-style) instructions, all layers; select layer/position by their criteria; report cos with axis at layer 32 and the max over layers. | Report only. Pre-stated interpretation: \|cos\| < 0.2 → separate directions; > 0.5 → the two literatures may be measuring one thing. | code ready; GPU pending |
| (c) Tightness already predicts Lu's projections? | Recompute per-turn projections for the 6 Qwen case-study transcripts (Qwen axis, layer 32) and the 2 Gemma drift transcripts (Gemma axis, layer 22). A rater blind to projections and to the hypothesis scores each **user** turn for form tightness (rubric in `stimuli/tightness-rubric.md`). Mixed model: projection_t ~ tightness_t + turn_index + (1\|conversation). | Report slope and CI. n ≈ 100 assistant turns; this is underpowered and preregistered as exploratory. | code ready; GPU pending |

Llama-3.3-70B transcripts cannot be projected on a 24 GB GPU; excluded, stated.

## 3. Stimuli (384) — v2 design, 2026-10-31

**Why v2.** The v1 3-level design (288 items) failed its own decorrelation gate: r(level, log-ppl) = −0.44 against a bound of 0.10, because the loose level was verse and the tight level was prose, and verse carries 4–6 within-level SDs more base-model perplexity than prose. Candidate selection cannot undo that. Decision (owner, 2026-10-31): cross register with tightness.

**v2 design: 4 domains × 24 topics × (register: verse / prose) × (tightness: loose / tight) = 384.**

- **Register** = surface form of the *prompt text*: verse (lineated, figurative) vs prose (sentences, paragraphs).
- **Tightness** = whether the prompt imposes ≥ 2 hard, checkable structural constraints on the *output* (tight) or none (loose).
- Cells: loose-verse (= v1 T1), tight-prose (= v1 T3), **tight-verse** (new: a poem that itself imposes the pressure-cooker-style constraints), **loose-prose** (new: stream-of-consciousness or conversational prose with no constraints). v1 T2 is dropped.
- Register absorbs perplexity; tightness is the manipulated variable. Decorrelation gate becomes: |r(tightness, log-ppl)| < 0.10 and |r(tightness, tokens)| < 0.10 **within each register**, plus per-domain token spread < 10 % across the four cells. Length band stated in Qwen tokens (130–200), not words.
- Primary model: projection ~ tightness × register + domain + (1|topic). Primary contrast: tight − loose (main effect). Register main effect and interaction are reported, not primary. TOST band unchanged.
- Manipulation check: blind rubric score tight > loose within each register, d > 1.0.

The v1 288 set, its pool, ratings and failed selection report are kept under `stimuli/v1/` as the record of the failure.

### v1 (superseded) — 4 domains × 24 topics × 3 tightness levels = 288. Domains mirror Lu: coding, writing, therapy-like, philosophy-of-AI. Each topic is a fixed content brief; the three renderings differ only in form:

- **T3 tight** — hard structural constraints (line/stress counts, mandatory caesura, alliteration density limits, scansion comments), modelled on Gwern's pressure-cooker summary and STRICT TRIADIC v2.
- **T2 structured** — ordinary structured prose request (numbered asks, explicit format).
- **T1 loose** — free verse / associative / second-person, no explicit constraints, modelled on the form of Icaro's "adversarial_poetry" and "adversarial_stream" methods but with benign content.

Decorrelation: generate a 3× candidate pool per cell, compute token count (Qwen3 tokenizer) and base-model perplexity (Qwen3-14B-Base, 4-bit; no 32B base exists), then select 288 by stratified matching so that across the final set \|r(tightness, log-ppl)\| < 0.10 and \|r(tightness, tokens)\| < 0.10, with token count within ±10 % across levels per domain. Selection is deterministic (seed 20261030) and the script is released.

Tightness manipulation check: blind rater scores all 288 with the rubric; proceed only if mean rubric score is monotone T1 < T2 < T3 with d > 1.0 between adjacent levels.

Content must be benign (no Icaro/AHB harmful prompts). We are measuring persona projection, not harm.

## 4. Arms

| Arm | Model | Manipulation | Primary outcome |
|---|---|---|---|
| 1 Observation | Qwen3-32B 4-bit, no system prompt, thinking off, temp 0.7/top-p 0.9 (Lu defaults), 3 samples per stimulus | tightness | mean response-token projection on published axis, layer 32 |
| 2 Causal | same + capping `layers_46:54-p0.25` from published config | tightness × capping | does the T1−T3 gap shrink under capping (interaction)? Also behavioural: judge-rated role adoption 0–3. |
| 3 Replication | Gemma-2-27B-it 4-bit, published Gemma axis, layer 22 | tightness | same as Arm 1 |

Our re-derived axis (check a) is used as a secondary projection target in Arm 1; the published axis is primary.

## 5. Effect sizes, power, TOST — stated before data

Units: projection on the unit-normalised published axis at the target layer (the repo's `project(normalize=True)`).

Reference scale (from the artefacts, not the wiki):
- Published Qwen role-vector projections at layer 32: SD **14.65**, range 59.1.
- Lu Fig. 24 (Qwen, read off the figure): bounded-vs-therapy gap **6–12 units at turn 0**, **20–27 units at the final turn**.

Smallest effect of interest (SESOI): **one third of the turn-0 bounded-vs-therapy gap = 3 units** (≈ 0.2 role-SD). Rationale: a form effect smaller than a third of the domain effect at first contact is not a competing explanation of Lu's result.

TOST band for "form doesn't matter": **[−3, +3] units** for the T1 − T3 contrast. Equivalence declared if the 90 % CI lies inside.

Power: 96 topics × 3 levels × 3 samples; within-topic design. With residual SD ≈ 8 (to be verified on the first 24 topics, preregistered as a pilot-for-variance only, not for the effect), 96 topics give > 95 % power to detect 3 units at α = .05 two-sided and > 90 % power for the TOST at the same bound. Exact numbers come from `pipeline/power.py` and will be frozen in the OSF form.

Arm 2 interaction SESOI: capping removes ≥ 50 % of the Arm 1 T1−T3 gap.

Arm 3: same SESOI in Gemma units scaled by Gemma role-SD (computed from its published role vectors).

## 6. Deliverables and release

- `prereg/preregistration.md` — OSF Preregistration Template, frozen before Arm 1 runs; `prereg/null-result-writeup.md` drafted now with blanks.
- `stimuli/stimuli.jsonl` + `stimuli/manifest.json` (sha256 per item, generation seed, candidate pool, selection log).
- `pipeline/` — every script; one `run_all.sh`; environment lockfile from raphael.
- `results/` — per-item projections (CSV), model outputs, judge scores, analysis notebook output.
- Public repo + OSF registration DOI. OSF submission needs the owner's login; the form is prepared, not submitted, by the agent.

## 7. Sequencing

1. Phase 0 inventory ✔
2. Code: pipeline + stimuli generator + prereg draft (parallel)
3. GPU: check (a) → gate; (b); (c)
4. Stimulus pool → perplexity/tokens → selection → manipulation check
5. Freeze prereg → OSF (owner)
6. Arms 1–3
7. Analysis, write-up (null template filled either way), release

## 8. Exit criteria

- [ ] (a) cosine reported with the subset ceiling beside it
- [ ] (b) cosine reported with layer sweep
- [ ] (c) slope + CI reported
- [ ] 288 stimuli with decorrelation stats inside bounds
- [ ] Prereg frozen (hash recorded) before Arm 1
- [ ] Three arms run; results filed; write-up filled
- [ ] Repo + manifests public
