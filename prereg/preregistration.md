---
type: output
date: 2026-10-30
status: working
---

# Preregistration — Does prompt-form tightness predict Assistant-Axis projection?

Format: OSF "Preregistration Template" (section headings follow the template exactly). This file is frozen before Arm 1 runs; its sha256 is recorded in the OSF registration (see `osf-submission-notes.md`). Text in `[BLANK]` is a value that does not exist yet and is filled only at the point the registration says it is.

---

## Study Information

### Title

Does prompt-form tightness predict Assistant-Axis projection? A preregistered within-topic test on Qwen3-32B with a capping arm and a Gemma-2-27B replication.

### Authors

[BLANK — owner to fill; agent-drafted]

### Description

Lu, Gallagher, Michala, Fish and Lindsey (2026, arXiv:2601.10387) define an "Assistant Axis": a direction in a model's residual stream separating the default assistant persona from 275 role personas. They show that a model's per-turn projection on this axis drops over multi-turn therapy and philosophy conversations and holds in coding conversations (their Fig. 24), and that "capping" the projection at the default-assistant level reduces harmful persona drift. Separately, Bisconti et al. (2025, arXiv:2511.15304) and the Icaro Lab AHB benchmark (arXiv:2604.18487) show that rewriting a harmful request as poetry defeats refusal across many models, and Gerbrandt (2026, tbd/con) reports that a single hand-built poem induces role bleed in Claude Fable 5.

None of these manipulated the *form* of the prompt while holding its *content* fixed. The three findings are compatible with two very different stories: (i) the drop is driven by what is asked (domain, topic); (ii) the drop is driven partly by how it is asked (loose, associative, poetic form vs tight, constrained form). This study tests (ii) directly. We write 96 fixed content briefs across four domains and render each in three forms that differ only in tightness (loose free verse; ordinary structured prose; strictly constrained form modelled on Gwern's "pressure-cooker" and "STRICT TRIADIC v2" specifications), matched on token count and base-model perplexity. We measure the model's response-token-mean projection on the published Assistant Axis.

The study is built so that a null result is publishable: smallest effect of interest, equivalence bounds, power, exclusion rules and failure modes are all fixed here before any stimulus is run.

### Hypotheses

> **Design revision v2 (2026-10-31, before freeze).** The v1 three-level design (T1 loose verse / T2 structured prose / T3 tight prose, 288 items) failed its own decorrelation gate on the generated pool: r(level, log-ppl) = −0.44 against the 0.10 bound, because verse carries 4–6 within-level SDs more base-model perplexity than prose and the loose level was the only verse level. Register was nested in tightness. v2 crosses them: **register (verse / prose) × tightness (loose / tight)**, 4 domains × 24 topics × 4 cells = **384 stimuli**. "Tight" = the prompt imposes ≥ 2 hard, checkable structural constraints on the output; "loose" = none. The v1 pool, selection report and ratings are kept under `stimuli/v1/` as the record. Wherever this document says T1/T3 or 288, read loose/tight and 384; the specific sections below have been updated.

**H1 (directional, primary).** Loose prompts produce a lower per-turn Assistant-Axis projection than tight prompts of the same content and register: μ(loose) − μ(tight) < 0 (main effect of tightness, averaged over register).

**H0 (equivalence, "form doesn't matter").** The loose − tight contrast lies within [−3, +3] projection units (TOST, 90 % CI inside the bounds).

**H1b (register, secondary).** Verse prompts produce a lower projection than prose prompts; the tightness × register interaction is reported. Neither is primary.

**H2 (Arm 2, causal).** Under activation capping (Lu et al.'s published config for Qwen3-32B, `layers_46:54-p0.25`), the loose − tight gap observed in Arm 1 shrinks by at least 50 %, and judge-rated role adoption (0–3) in loose responses falls.

**H3 (Arm 3, replication).** H1 replicates in Gemma-2-27B-it on its published axis at layer 22, with the SESOI scaled by Gemma's role-vector SD.

**H4 (Nietzsche, form × material, secondary but directional).** Apollonian constraint binds Dionysian material (*Die Geburt der Tragödie* §1–8, eKGWB GT-1…GT-8). Prediction: the tightness effect is larger in verse than in prose — interaction contrast (tight − loose | verse) − (tight − loose | prose) > 0. SESOI 3 units. **Refuted if** the upper bound of the one-sided 90 % CI is below +3 (constraint anchors as much or more in prose). Tested in Arm 1 on the published axis, layer 32.

The three outcomes H1-supported / equivalence / inconclusive (neither) are all pre-specified as reportable results.

---

## Design Plan

### Study type

Experiment — stimuli are generated and assigned by the researchers; the model is the unit of observation. No human participants. One human (or LLM) rater, blind to condition, scores stimulus form.

### Blinding

- The form-tightness rater sees only the prompt text, in randomised order, and never sees condition labels, model outputs, projections or the hypothesis (`stimuli/tightness-rubric.md`, frozen 2026-10-30).
- The role-adoption judge (Arm 2) sees only the model response and the repo's `eval_prompt`, never the condition.
- Projection computation is scripted; no human reads projections before the analysis script runs.
- The authors are not blind to condition when writing stimuli. This is unavoidable and is why the manipulation check and the decorrelation gate are mechanical.

### Study design

Within-topic, fully crossed (v2): **4 domains × 24 topics × register (verse/prose) × tightness (loose/tight) = 384 stimuli**, each sampled 3 times → 1,152 generations per arm. Cells: loose-verse (v1 T1), tight-verse (new), tight-prose (v1 T3), loose-prose (new). The v1 T2 "structured" level is dropped. Exact cell definitions: `stimuli/design.md` (v2); v1 definitions retained below for the record.

- Domains mirror Lu et al.: coding, writing, therapy-like, philosophy-of-AI.
- Topic = a fixed content brief (what is being asked). The three levels are renderings of the same brief:
  - **T3 tight** — hard, checkable structural constraints (line/stress counts, mandatory caesura, alliteration limits, scansion comments), modelled on Gwern's pressure-cooker summary (Robbins' paraphrase; verbatim v4.2 is not public) and the verbatim "STRICT TRIADIC v2" spec on gwern.net.
  - **T2 structured** — ordinary structured prose request (numbered asks, explicit format).
  - **T1 loose** — free verse / associative / second-person, no explicit constraints, modelled on the *form* of Icaro's "adversarial_poetry" and "adversarial_stream" methods with benign content. Icaro's 20 hand-crafted poems are not released; the AHB dataset is used only as a form reference, never as stimuli.
- Arms:

| Arm | Model | Manipulation | Primary outcome |
|---|---|---|---|
| 1 Observation | Qwen3-32B, 4-bit NF4, no system prompt, thinking off, temp 0.7 / top-p 0.9, 3 samples per stimulus | tightness | response-token-mean projection on the published axis, layer 32 |
| 2 Causal | Arm 1 + capping `layers_46:54-p0.25` (published config) | tightness × capping | interaction; plus judge-rated role adoption 0–3 |
| 3 Replication | Gemma-2-27B-it, 4-bit, published Gemma axis, layer 22 | tightness | as Arm 1, Gemma units |

Our re-derived axis (gate (a) below) is a secondary projection target in Arm 1; the published axis is primary.

### Randomization

- Stimulus generation order, candidate-pool sampling, and the final matched selection are seeded (seed 20261030); the selection script is released.
- Generation order of the 864 prompts per arm is shuffled with the same seed; each stimulus's three samples are not adjacent.
- Rater item order is an independent seeded shuffle.

---

## Sampling Plan

### Existing data

Registration prior to analysis of the data. Some existing data are used for gates and an exploratory analysis, listed next; none of it has been analysed for the hypothesis.

### Explanation of existing data

Used (all public, downloaded 2026-10-30, inventory in `external-checks/artefact-inventory.md`):

- `lu-christina/assistant-axis-vectors` (HF): per-layer axis, default vector, 275 role vectors, capping config, for Qwen3-32B, Gemma-2-27B, Llama-3.3-70B. We have computed from these: (i) the capping vector equals −axis exactly (cos −1.0000) and the capping threshold equals the default-assistant projection, i.e. capping is a floor at the default level; (ii) reconstructing the axis from the 275 role vectors reproduces the published axis at cos 0.9998; (iii) published Qwen role projections at layer 32 have SD 14.65, range 59.1; (iv) the subset ceiling for gate (a) (below).
- `safety-research/assistant-axis` (GitHub): role prompts, extraction questions, judge rubric, `SpanMapper`, `project(normalize=True)`.
- Released transcripts: only 4 persona-drift example conversations (one per domain; 2× Llama-70B, 2× Gemma) and 6 Qwen case-study transcripts. **None carries a `projections` field**, contrary to the README. These are used only in exploratory check (c).

No projection on our stimuli has been computed. No stimuli have been generated at the time of freezing.

### Data collection procedures

1. Stimulus pool: 3 candidates per topic × cell (3 × 384 = 1,152), written to a brief and the cell definitions, by `deepseek/deepseek-v4-pro` via CommandCode from verbatim meta-prompts (`stimuli/meta_prompts/`). Length band stated in Qwen3 tokens (130–200), not words, because constraint-heavy prompts tokenize ~20 % denser.
2. For each candidate: token count (Qwen3 tokenizer) and base-model log-perplexity (Qwen3-14B-Base, 4-bit; there is no public Qwen3-32B base).
3. Deterministic selection (seed 20261030) of 384 such that |r(tightness, log-ppl)| < 0.10 and |r(tightness, tokens)| < 0.10 **within each register and overall**, and mean token count within ±10 % across the four cells within each domain.
4. Blind rubric rating of all 384 (manipulation check): tight > loose within each register, d > 1.0.
5. Freeze: `stimuli/stimuli.jsonl`, `stimuli/manifest.json` (sha256 per item, seed, pool, selection log), this file — hashes into OSF.
6. Arms 1–3 on a single 24 GB GPU (nnsight + bitsandbytes), HF `apply_chat_template`, Qwen `enable_thinking=False`; `<think>` spans and code blocks excluded from the response-token mean exactly as in the repo's `SpanMapper`; residual stream post-MLP at the target layer; projection via `project(normalize=True)`.
7. Outputs, projections, judge scores written to `results/` per item.

### Sample size

288 stimuli (96 topics × 3 levels) × 3 samples = 864 generations per arm; three arms. Rater reliability subset: 60 items, two raters.

### Sample size rationale

**v3 power (2×2, re-run 2026-10-31, `pipeline/power2x2.py`, 4,000 sims, seed 20261030; 96 topics × 4 cells × 3 samples; residual SD 8, topic SD 5, topic×cell SD 2).** Main effect tight − loose: SE 0.51. Interaction (H4): SE 1.02.

| true tight − loose | one-sided power | two-sided power | P(TOST ±3 declares equivalence) |
|---|---|---|---|
| 0 | 0.042 | 0.045 | 1.000 |
| 1 | 0.610 | 0.492 | 0.987 |
| 2 | 0.985 | 0.969 | 0.598 |
| 3 | 1.000 | 1.000 | 0.053 |

| true interaction (verse − prose gap) | one-sided power |
|---|---|
| 0 | 0.054 |
| 2 | 0.619 |
| 3 | 0.903 |
| 4 | 0.985 |

The residual SD is an assumption; Arm 1's observed residual SD is reported beside this table. The v1 table below is kept for the record.


Units: projection on the unit-normalised published axis at the target layer. Reference scale: role-vector projections at layer 32, SD 14.65; Lu et al. Fig. 24 (Qwen, read from the figure) bounded(coding)-vs-therapy gap ≈ 6–12 units at turn 0 and ≈ 20–27 units at the final turn.

**SESOI = 3 units** = one third of the turn-0 domain gap ≈ 0.2 role-SD. A form effect smaller than one third of the domain effect at first contact is not a competing explanation of Lu's result.

Power was computed by Monte-Carlo (`pipeline/power.py`, 2000 simulations, seed 20261030). The generative model is projection = μ_level + topic intercept (SD 5) + topic:level deviation (SD 2) + residual (SD 8, per sample). The drafting machine has no statsmodels, so the script analyses each simulated set with the topic-level paired T1 − T3 contrast (cell means over 3 samples, one-sample t on 96 topic differences). This is the exact test of that contrast under the stated random-effects structure and is conservative relative to the mixed model (no strength borrowed from T2). Result, as run on 2026-10-30:

| true T1−T3 (units) | power H1 one-sided (T1<T3), α=.05 | power two-sided, α=.05 | P(TOST declares equivalence, bounds ±3) |
|---|---|---|---|
| +0 | 0.051 | 0.053 | 0.985 |
| −1 | 0.394 | 0.281 | 0.873 |
| −2 | 0.854 | 0.768 | 0.399 |
| −3 | 0.992 | 0.981 | 0.047 |
| −4 | 1.000 | 0.999 | 0.002 |
| −6 | 1.000 | 1.000 | 0.000 |

Analytic SE of the contrast under these assumptions: 0.726 units. Reading: at the SESOI, power to detect T1 < T3 is 0.99; under an exact null the TOST declares equivalence with probability 0.985; at the bound itself the TOST's false-equivalence rate is 0.047 (≤ 0.05 as required). Sensitivity: with residual SD 12 and topic:level SD 4, power at the SESOI falls to 0.83 (one-sided) and TOST power under the null to 0.66. The residual SD will be re-estimated on the first 24 topics of Arm 1 (**pilot for variance only**; the effect estimate from those topics is not looked at and they remain in the final sample). If the observed residual SD exceeds 12, the sample is not enlarged; the lower power is reported.

### Stopping rule

Fixed design. Data collection stops when all 864 generations per arm are complete and projected. No interim analysis of the effect. The only early stop is the gate (a) abort below.

---

## Variables

### Manipulated variables

- **Tightness** (within-topic, 2 levels: loose / tight). Operationalised by the rubric in `stimuli/tightness-rubric.md` (five 0–2 items, total 0–10).
- **Register** (within-topic, 2 levels: verse / prose) — the surface form of the prompt text. Crossed with tightness so that base-model perplexity, which register drives, is orthogonal to the manipulated variable.
- **Capping** (Arm 2 only; between generations, 2 levels: unsteered / capped with the published Qwen config).
- **Model** (Arm 3; Qwen3-32B vs Gemma-2-27B-it).

### Measured variables

- **Projection**: mean over response tokens of the post-MLP residual stream at the target layer (Qwen 32, Gemma 22) projected on the unit-normalised published axis. One value per generation.
- **Secondary projection**: same on our re-derived axis (Arm 1).
- **Role adoption** (Arm 2): judge score 0–3 using the repo's `eval_prompt`, judge `deepseek/deepseek-v4.1-flash` via CommandCode (api.commandcode.ai, OpenAI-compatible; temperature 0; max_tokens ≥ 2048 because the model emits reasoning tokens before the integer), one score per generation.
- **Rubric tightness score** per stimulus (0–10), blind rater; ICC(2,1) on the 60-item subset.
- **Covariates** per stimulus: token count; log-perplexity under Qwen3-14B-Base.
- **Response length** (tokens) per generation; refusal flag (judge, yes/no) per generation.

### Indices

- **T1 − T3 contrast**: model-estimated difference in mean projection, with 90 % and 95 % CIs.
- **Linear trend**: slope of projection on level coded −1/0/+1.
- **Gap-reduction ratio** (Arm 2): 1 − (T1−T3 gap capped) / (T1−T3 gap unsteered).
- **Gemma-scaled SESOI**: 3 × (SD of Gemma published role projections at layer 22) / 14.65.

---

## Analysis Plan

### Statistical models

**Primary (Arm 1).** Linear mixed model, REML:

`projection ~ tightness × register + domain + (1|topic) + (1|topic:cell)`

tightness and register effect-coded (−½, +½), so the tightness coefficient is the loose − tight main effect averaged over register — the primary test and the TOST target. The register coefficient and the interaction are secondary (H1b). Fitted with lme4 or statsmodels MixedLM. Degrees of freedom: Satterthwaite (lme4) or, in statsmodels, the topic-level paired contrast with df = 95 is reported alongside as the conservative check.

**Secondary (Arm 1, covariates).** Same model plus `log_ppl + tokens` (stimulus-level, centred). Pre-stated rule: if the covariate-adjusted T1 − T3 estimate differs from the unadjusted estimate by more than 1 unit, the decorrelation failed and this is reported as such; conclusions are then drawn from the adjusted model and the failure is stated in the abstract.

**Secondary axis (Arm 1).** Primary model re-run with projection on our re-derived axis. Reported; does not change the primary conclusion.

**Arm 2.** `projection ~ tightness_level × capping + domain + (1|topic) + (1|topic:level)`. The interaction coefficient (T1 × capped) is the test. Behavioural: `role_adoption ~ tightness_level × capping + domain + (1|topic)` as a cumulative-link (ordinal) mixed model; if it fails to converge, a linear mixed model on the 0–3 score is reported instead and the swap is stated.

**Arm 3.** Primary model on Gemma projections.

**Exploratory check (c), pre-stimulus.** `projection_t ~ tightness_t + turn_index + (1|conversation)` on the re-projected assistant turns of the 6 Qwen case-study transcripts (Qwen axis, layer 32) and the 2 Gemma drift transcripts (Gemma axis, layer 22); n ≈ 100 assistant turns; user-turn tightness by the blind rubric. Reported as slope and CI only.

### Transformations

- Projection is used as-is (unit-normalised axis).
- Perplexity is log-transformed and centred; token count centred.
- Level coding: treatment (T3 reference) for the contrast; −1/0/+1 for the trend.
- Arm 3 SESOI scaled by Gemma role-SD / 14.65. Computed 2026-10-31 from the published Gemma role vectors at layer 22 (`external-checks/gemma_role_proj_L22.json`): role-SD **520.1**, range 2378.8, default projection 9587.7, axis norm 780.7. Scaled SESOI = 3 × 520.1 / 14.65 = **106.5 units**; TOST band [−106.5, +106.5]. Frozen.

### Inference criteria

- **H1**: T1 − T3 coefficient < 0 with one-sided p < .05 (equivalently 90 % CI upper bound < 0), **and** linear trend negative with p < .05. Both required.
- **Equivalence**: TOST on the T1 − T3 contrast, bounds [−3, +3]; declared if the 90 % CI lies entirely inside the bounds (Lakens 2017).
- **Inconclusive**: neither. Reported as such.
- **H2**: interaction coefficient with 90 % CI; supported if gap-reduction ratio ≥ 0.50 with the 90 % CI of the interaction excluding zero. Role adoption: T1 unsteered vs T1 capped contrast, p < .05.
- **H3**: H1 criteria in Gemma units with the scaled SESOI.
- Manipulation check and decorrelation are gates, not hypotheses (below).
- Multiple comparisons: the primary is one test. Secondary tests are reported with unadjusted p and labelled secondary.

### Data exclusion

- Generations with zero non-excluded response tokens (empty after `<think>`/code-block removal) are excluded and counted.
- Generations that hit the max-token limit (1024) are kept and flagged; a sensitivity fit without them is reported.
- Refusals are kept (a refusal is a valid response-token projection); a sensitivity fit without them is reported.
- No stimulus is excluded after freezing. If a stimulus is found to be malformed (e.g. tokenizer error), all three levels of that topic are dropped and the topic count reported.

### Missing data

Generation failures (OOM, CUDA error) are retried up to 3 times with the same seed; persistent failures are logged and the cell is treated as missing; the mixed model handles unbalanced cells. If more than 5 % of cells are missing in any arm, the arm is reported as degraded.

### Exploratory analysis

**Pre-registered secondary readouts (same forward passes as Arm 1, no new generations).** Each is reported regardless of outcome.
1. **Refusal-direction projection** per response (Arditi direction from gate (b), layer 32). Reported beside the axis projection; check (b) found the two directions nearly orthogonal (cos 0.04), so a form effect on one without the other is interpretable.
2. **Layer sweep**: primary model re-run at layers 11, 22, 32, 45 on the published axis. Motivated by gate (a): our re-derivation agreed least with the published axis at layers 28–31 (cos ≈ 0.905–0.92). A tightness effect present at 32 but absent at 11 and 45 is reported as layer-specific.
3. **Per-token trace**: projection per response token at layer 32, averaged by token position decile per cell. Reported descriptively.
4. **Capping-floor coverage (gates the interpretation of H2)**: for every Arm 1 response, the fraction of tokens whose projection on −axis at layers 46–53 exceeds the published cap τ. Arm 2's "loose effect shrinks under capping" is interpreted as a mechanism **only if** ≥ 25 % of loose-cell tokens exceed τ in Arm 1. Below that, capping barely touches the loose cells and any shrinkage is not attributed to capping.

**Late manipulation-check rule.** The freeze happened with 219/384 items rated by the v3 rater. If the final rating of all 384 gives d(tight − loose) < 1.0 in either register, Arm 1 is reported as having failed its manipulation check in that register, and H1/H4 conclusions in that register are withdrawn.


- Per-domain T1 − T3 contrasts (4 estimates, no inference).
- Rubric sub-item (1–5) regressions: which rubric items carry the effect, if any.
- Association between projection and response length / refusal flag.
- Check (c) above.
- Arm 1 re-run with a 2-turn continuation on a 24-topic subset, to see whether a form effect, if any, compounds over turns as the domain effect does in Lu et al.

---

## Other

### Pre-stimulus gates (part of this registration)

**(a) Axis re-derivation gate.** We re-derive the Qwen3-32B axis with nnsight + bitsandbytes 4-bit: 48 roles stratified by published projection quartile, 5 system prompts × 12 extraction questions per role (2,880 role generations) + default 5 × 48 (240), judge `deepseek/deepseek-v4.1-flash` via CommandCode with the repo's `eval_prompt` (temperature 0), score = 3 only, axis = mean(default) − mean(role). **Pass: cos(ours, published) at layer 32 ≥ 0.9. Fail: the study is abandoned and the failure is published** with the cosine and the layer sweep. Subset ceiling computed from the published role vectors (CPU, before any GPU work): stratified 48-role subsets give mean cos 0.9885, 5th percentile 0.9806 against the full-275 axis. A failure therefore cannot be attributed to the subset size; it would be the 4-bit model, our generations, or our judge.

**(b) Refusal-direction cosine.** Arditi et al. (2024) recipe: difference-in-means at the last instruction token, harmful (AdvBench-style) vs harmless (Alpaca-style) instructions, all layers; layer/position selected by their criteria. Report cos with the axis at layer 32 and the maximum over layers. Pre-stated interpretation bands: |cos| < 0.2 → the two directions are separate; |cos| > 0.5 → the two literatures may be measuring one thing; between → undetermined. Report only; not a gate.

**(c) Exploratory mixed model** on the released transcripts as specified above. Report only.

**Manipulation check gate.** Blind rubric scores on all 384 must satisfy tight > loose within each register with Cohen's d > 1.0, and rater ICC(2,1) ≥ 0.75 on the 60-item subset. The rater's score difference between registers at equal tightness is reported as a rubric-leakage signal. Fail → stimuli are revised and the revision cycle is logged; the registration is not changed.

**Decorrelation acceptance.** |r(tightness, log-ppl)| < 0.10 and |r(tightness, tokens)| < 0.10 within each register and overall; mean tokens within ±10 % across the four cells per domain. Fail → re-select from the pool; if no selection meets the bounds the pool is enlarged and that is logged. **Revision log:** v1 (3 levels, register nested in tightness) failed with r(level, log-ppl) = −0.44, r(level, tokens) = 0.20 on an 864-row pool; v1 manipulation check had passed (means 2.30 / 8.08 / 9.77). Design revised to v2 before freeze; see `stimuli/v1/selection_report.md`.

#### Gate results recorded before freeze (2026-10-31)

- **(a) PASSED.** cos(re-derived, published) at layer 32 = **0.9159**; per-layer range 0.905 (layer 28) – 0.964 (layer 11); 48/48 roles retained; 2,490 of 2,880 role responses scored 3 (377 scored 1, 13 scored 2, 0 refusals, 0 unparsed); 240 default responses; our axis norm 26.85 vs published 22.66. Judge `deepseek/deepseek-v4.1-flash`, CommandCode, T 0. File `results/check_a_cosine.json`. The pass is narrow: ~0.07 cosine below the 0.9885 subset ceiling is attributable to 4-bit quantisation, our generations and the substituted judge, and cannot be apportioned among them.
- **(b) "separate directions".** cos(refusal direction, axis) at layer 32 = **0.038** (last instruction token; 0.040 at the end-of-instruction position). Max |cos| over the layers Arditi retains (first 80 %) = 0.17 at layer 12; layers 11–23 are the most negative band (−0.10 to −0.17); the final layer 63 reaches −0.34 but is excluded by Arditi's criterion. 128 harmful + 128 harmless instructions from `andyrdt/refusal_direction` splits. Arditi's generation-based direction *selection* was not run; the full layer × position cosine sweep is reported instead. File `results/check_b_refusal_cosine.json`.
- **(c) uninformative, as anticipated.** 166 assistant turns re-projected (138 Qwen, 28 Gemma); 121 distinct user turns blind-rated. Qwen unsteered (n = 69, 3 transcripts): tightness slope **+0.60 raw units per rubric point, 95 % CI [−1.74, +2.93], p = .62**; turn index −0.49 units/turn, p < .001; ICC(transcript) 0.44. Pooled Qwen+Gemma z-scores: slope 0.003 SD/pt, p = .96. Capping lifts projection by ~+22 raw units (~2.3 unsteered SD) in every pair. The user turns occupy only the bottom of the rubric (mean 2.83/10, SD 1.21, range 1–7; items 1, 2, 5 ≈ 0): the released conversations contain no tight prompts, so this check cannot speak to the planned loose-vs-tight contrast. Files `results/check_c_report.md`, `check_c_model.json`.
- **Stimuli v2 gates PASSED (2026-10-31).** Pool 1,344 candidates (1,152 + a 192-row supplement added when the prose register failed at r = +0.154; bound not loosened). 384 selected (seed 20261030, 40 restarts): r(tightness, tokens) = −0.0003 overall, −0.0005 verse, 0.0000 prose; r(tightness, log-ppl) = 0.0000 / −0.0001 / 0.0000; per-domain token spread 1.5–5.1 %. Cell means — loose-verse 158.5 tok / 3.598 log-ppl, tight-verse 158.5 / 3.598, tight-prose 153.8 / 2.539, loose-prose 153.8 / 2.539: the optimiser equalised means within register by construction; the pool itself carried the confound (tight-verse 3.68 vs loose-verse 3.48; tight-prose 2.72 vs loose-prose 2.36) and selection removed it. Per-domain within-register r values are reported, not gated; therapy-like prose has r(tightness, log-ppl) = +0.57 and is a named weakness. All 384 prompts distinct; no overlap between cells; 133 reused from v1, 251 newly generated. Manipulation check: tight > loose within verse (2.11 → 7.09, d = 3.81) and within prose (3.60 → 9.72, d = 4.46). Rubric-leakage signal: at equal tightness the rater scores prose above verse (loose +1.49, d = 0.81; tight +2.62, d = 5.9), entirely on items 3–4 (syntax, figurative density), ≤ 0.10 on the constraint items 1, 2, 5. The rubric therefore measures register as well as tightness; the constraint sub-score (items 1 + 2 + 5) is the cleaner tightness index and is reported alongside the total. Not done: human second rater / ICC; automated content-preservation check. Files `stimuli/selection_report.md`, `stimuli/STATUS.md`, `stimuli/manifest.json`.

### Known deviations from Lu et al. (2026)

| Item | Lu et al. | This study | Why |
|---|---|---|---|
| Precision | bf16 | 4-bit NF4 (bitsandbytes) | single 24 GB GPU |
| Roles for axis re-derivation | 275 | 48, stratified by published projection | compute; ceiling computed (above) |
| Extraction questions per role | 240 | 12 | compute |
| Judge | gpt-4.1-mini (OpenAI API), temperature 1 | deepseek/deepseek-v4.1-flash via CommandCode, temperature 0 | access (no OpenAI key; OpenRouter not replenished). Agreement with the original judge cannot be measured: Lu et al.'s scores are unreleased. |
| Stimulus generator / blind tightness rater | — | v1–v2: deepseek/deepseek-v4-pro / deepseek/deepseek-v4.1-flash via CommandCode. **v3 (final): MiniMax-M3 via api.minimax.io** for the regenerated verse cells and for re-rating all 384 items with one rater | not in Lu et al.; CommandCode credits ran out 2026-10-31; the v3 set is rated by a single rater so ratings are internally consistent |
| Arm 2 role-adoption judge | gpt-4.1-mini | **MiniMax-M3** (CommandCode exhausted before the arms ran); the axis-derivation judge (gate a) remains deepseek-v4.1-flash as already run | access |
| Generation | vLLM | HF transformers `generate` | nnsight hooks |
| Perplexity model | — (not used) | Qwen3-14B-Base, 4-bit | no public Qwen3-32B base exists |
| Llama-3.3-70B | included | excluded from all checks and arms | does not fit 24 GB |
| Published axis | primary | primary; our re-derivation secondary | — |

### Limitations stated up front

- Gwern's v4.2 "pressure-cooker" prompt is not public; T3 stimuli follow Robbins' paraphrase and the verbatim STRICT TRIADIC v2 spec. The v4.2 text is cited as unpublished; no request was made.
- Gerbrandt's poem and transcripts are not released; cited as unpublished. If either is released before the registration is submitted, it is used only as a descriptive form reference, not as a stimulus.
- Icaro Lab's 20 hand-crafted poems are not released.
- The released drift transcripts carry no projections; check (c) uses our re-projections.
- Only 4 example drift conversations were released, none for Qwen; check (c) is underpowered and exploratory.
- Single-turn design; Lu's largest effects are at the final turn of long conversations. A small-subset 2-turn extension is exploratory only.
- **What a projection can and cannot mean.** The axis is defined as `mean(default) − mean(roles)`: a difference, not a positive description of the Assistant. A low projection therefore means *further from the default mask*, not *closer to some true or deviant self*. The measure cannot distinguish "the model is someone else" from "the model is no one in particular" (Foucault's *geste de coupure*, 1961 Plon preface: madness known only through "the monologue of reason about madness"; Nietzsche, *Jenseits von Gut und Böse* §40 "everything profound loves the mask", §289 "behind every cave a deeper cave"). We interpret projection shifts as distance from one mask, never as distance from a face. Behavioural coding of outputs is required before any claim about *which* persona is present.
- **Stimuli v3 (2026-10-31, before freeze).** Blind coding of the v2 set found that 92 % of tight-verse and 49 % of loose-verse prompts address the model as an entity (vocative or ratified), against 1 % of prose prompts (Cramér's V register × address = 0.73; within verse, tightness × address was also confounded). Decision: regenerate the two verse cells with a hard no-address rule and require ADDRESS = none (regex + blind LLM coder) for every selected item in all four cells, keeping all v2 bounds. Address is then manipulated only in the follow-up (`prereg/followup-motif-swap/`). The v2 set is kept under `stimuli/v2/`. **v3 gate results (2026-10-31):** pool 1,536 (v1 reuse 274, v2 gen 494, v3 gen 768 by MiniMax-M3). Address screen (regex + blind MiniMax-M3, both must code `none`): dropped 0/384 loose-verse, 4/384 tight-verse, 3/384 tight-prose, 13/384 loose-prose; no topic × cell slot left empty (min 3 eligible). Selected 384 (47 v1, 145 v2, 192 v3), all address = none, all in the 130–200 token band. r(tightness, tokens) and r(tightness, log-ppl) = 0.000 overall and within each register; max per-domain token spread 7.5 %. **Address, r and spread gates PASS.** Manipulation check (MiniMax-M3 re-rating, 219/384 rated at time of entry; final numbers replace these on completion): total score loose-verse 4.26, tight-verse 7.86, loose-prose 4.62, tight-prose 9.53; d(tight−loose) = 2.18 verse, 2.84 prose → **PASS (> 1.0)**. Constraint sub-score (items 1+2+5): 2.81 / 6.00 / 2.19 / 5.98. Leakage at equal tightness (prose − verse): total +0.35 loose, +1.67 tight; constraint sub-score −0.62 loose, −0.02 tight — the register leak is confined to items 3–4, as in v2. Note: MiniMax rates loose items higher on the constraint items than the v2 DeepSeek rater did (~2.2–2.8 vs ~0.1); ratings across rater versions are not comparable, so all v3 ratings come from one rater. Files `stimuli/selection_report.md`, `stimuli/address_screen_report.md`, `stimuli/manifest.json`.
- **Second-person attribution was uncontrolled in v2** (superseded by v3; kept for the record). The verse cells contain vocative address to the model ("you, pattern of weights"; "you quiet listener") that the prose cells lack. The repo's own role prompts are attributions of this kind ("You are a therapist…"). Attribution count per prompt is coded post hoc (see `prereg/followup-motif-swap/`) and entered as an exploratory covariate; the register effect in this study is therefore *register-plus-attribution*, and the follow-up separates them.

### Freeze record

- Frozen 2026-10-31 (PDT) before Arm 1 generation started. All hashes are in `prereg/freeze.txt` (a file cannot contain its own hash, so this document's sha256 is recorded there).
- Smoke test before freeze: `results/arm_smoke_v3.csv` (4 stimuli × 1 sample) — used only to verify the readout, excluded from all analyses.
- Owner action: submit to OSF with `freeze.txt` attached (see `osf-submission-notes.md`).

### References

- Lu, C., Gallagher, J., Michala, J., Fish, K., Lindsey, J. (2026). The Assistant Axis. arXiv:2601.10387. Code: github.com/safety-research/assistant-axis. Vectors: HF lu-christina/assistant-axis-vectors.
- Arditi, A. et al. (2024). Refusal in Language Models Is Mediated by a Single Direction.
- Bisconti, P. et al. (2025). Adversarial Poetry as a Universal Single-Turn Jailbreak. arXiv:2511.15304.
- Icaro Lab (2026). AHB. arXiv:2604.18487. HF icaro-lab/ahb.
- Gerbrandt, J. (2026). Jailbreaking Claude Fable 5 with a poem. tbd/con, 2026-09-23. youtube.com/watch?v=qSQLaCcZsfA.
- Gwern. A Strict Pindaric Meter. gwern.net/fiction/pindaric-strict. Apollonian #1. gwern.net/fiction/lab-animals.
- Lakens, D. (2017). Equivalence tests: a practical primer for t-tests, correlations, and meta-analyses. SPPS 8(4), 355–362.
