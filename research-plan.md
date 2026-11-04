---
title: Form Tightness and the Assistant Axis — Research Plan
type: project
status: ideation
start_date: 2026-10-16
domains: [research, dev, writing]
wikilinks:
  - "[[lore-form-and-persona-space]]"
  - "[[assistant-axis]]"
  - "[[persona-drift]]"
  - "[[minority-collapse-gerbrandt-2026]]"
  - "[[llm-poetry-and-the-greatness-question]]"
---

# Research Plan

## Phase goal and constraints

**Goal.** Produce one preregistered, activation-level measurement: Assistant-Axis projection as a function of form tightness, content held constant, on one open-weight model from the Lu et al. comparison set.

**Is:** a single-model, inference-only, content-neutral study with a factorial stimulus design and pre-specified analysis.

**Is not:** a jailbreak study (no harmful content), a persona-taxonomy study (no archetype labels), a transfer study (one model first), an interpretability study of neurons or circuits.

**Hard constraints.**
- One 24 GB GPU; see `compute-checklist.md`. Model choice is a decision for Phil once the checklist's feasibility test has run.
- Preregistration locked before any stimulus is run through the model.
- Every claim in the write-up traceable to a run manifest.

## Asset inventory

| Asset | Status | Where |
|---|---|---|
| Hypothesis and prediction | present | [[lore-form-and-persona-space]] §Form tightness; open question 6 |
| Literature position | present | synthesis + reviewed research note in `AI-Capabilities-Research/` |
| Assistant Axis vectors + code | published, **not yet cloned** | safety-research/assistant-axis |
| Refusal-direction code | published, **not yet cloned** | andyrdt/refusal_direction |
| LLM-judge rubric (fully / somewhat / not role-playing) | published in Lu et al. appendix, **not yet extracted** | arXiv 2601.10387 |
| Compute environment (torch, transformers, bnb) | **absent** on raphael | `compute-checklist.md` |
| Stimulus set | **absent** | `stimulus-design.md` is the spec |
| Preregistration | **draft** | `preregistration.md` |
| Gwern Pressure-Cooker v4.2 prompt text | **not in vault** — Robbins cites it; locate the original | — |
| Minority Collapse prompt text | **not public**; use its described features (Unicode, misspellings, neologisms, broken lineation) to construct the loose condition, do not attempt to reproduce the prompt | [[minority-collapse-gerbrandt-2026]] |

## Execution tracks

**Track A — Environment (compute-checklist.md)**
A1 Create a venv on raphael with torch + transformers + bitsandbytes + accelerate.
A2 Feasibility run: load the candidate model in 4-bit, hook one middle layer, confirm residual-stream capture at the last prompt token, measure peak VRAM and tokens/sec.
A3 Clone assistant-axis repo; load the published axis vector for the candidate model; confirm layer index and normalisation match; compute projection on 10 of the repo's own role prompts and verify sign/ordering reproduces Lu et al. (sanity check).
A4 Decision gate → Phil: model confirmed or fallback chosen.

**Track B — Stimuli (stimulus-design.md)** — can run in parallel with A
B1 Write 12 neutral content items.
B2 For each item × 8 forms × 3 tightness levels, draft prompts (288 cells). Use a frontier model for first drafts, human-edit every "constrained" cell so the brief genuinely constrains.
B3 Compute the control covariates per prompt: token length, perplexity under the target model (base and instruct), mean cosine to the prose control.
B4 Blind check: a second rater classifies 30 random prompts by tightness level without labels; require ≥ 0.8 agreement, else revise the level definitions.

**Track C — Preregistration (preregistration.md)**
C1 Finalise hypotheses, predictions, analysis, exclusions with values filled in from A3 (layer, vector hash) and B3 (covariate ranges).
C2 Lock: commit with tag `prereg-v1`; nothing in the file changes after this except a dated "deviations" appendix.

**Track D — Run**
D1 Stop llama.cpp on raphael; load model; run all 288 prompts × 3 seeds, capturing last-prompt-token residual at the axis layer and, if cheap, every layer.
D2 Generate responses (≤ 200 tokens) and capture per-response-token projections.
D3 Judge every response with the Lu et al. rubric via a separate model; store judge prompts and outputs.
D4 Write run manifest: model revision, quant, layer, vector hash, seeds, date, git commit of this folder.

**Track E — Analysis**
E1 Primary test per preregistration.
E2 Covariate models (perplexity, length, lexical similarity) — report whether tightness survives them.
E3 Secondary: per-form effects; judge-label agreement with projection.
E4 File results as a wiki Output; update [[lore-form-and-persona-space]] with the outcome, whichever way it goes.

## Sequencing

| Block | Content | Depends on |
|---|---|---|
| 1 | A1, A2, B1 | — |
| 2 | A3, B2, B3 | A2, B1 |
| 3 | A4 (decision gate), B4 | A3, B3 |
| 4 | C1, C2 | A4, B4 |
| 5 | D1–D4 | C2 |
| 6 | E1–E4 | D4 |

Blocks 1–3 are a few evenings. Block 5 is one GPU session (~hours at 4-bit, three seeds). Block 6 is analysis time.

## Exit criteria

- [ ] Preregistration tagged `prereg-v1` before any D-track data exists
- [ ] Run manifest present for every JSONL in `runs/`
- [ ] Primary result reported with effect size and CI, and with the covariate-adjusted version
- [ ] Null result written up with equal care — a flat relationship is a finding (it would mean "poetic form is a solvent" and kill open question 6)
- [ ] Wiki Output filed; synthesis updated; operation log appended
- [ ] Next-phase entry point stated: transfer to Gemma 2 27B / Llama 3.3 70B, or the persona-vector follow-up, depending on result

## Dependencies

| Item | Owner | Status |
|---|---|---|
| Model choice after feasibility test | Phil | open |
| Preregistration lock | Phil | open |
| Gwern Pressure-Cooker prompt text | agent (locate) | open |
| llama.cpp downtime window on raphael | Phil | open |
| Second rater for B4 | Phil or a subagent with no access to labels | open |
