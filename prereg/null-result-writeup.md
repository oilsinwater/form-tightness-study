---
type: output
date: 2026-10-30
status: working
---

# Prompt-form tightness does not move the Assistant Axis: a preregistered null

> **This is not the results.** It is the pre-data anti-HARKing draft: written
> before any generation existed, for the branch where the TOST passed, and never
> filled in. Two reasons it must not be read as a finding:
>
> 1. **It is written for the wrong branch.** TOST equivalence was rejected —
>     tight − loose = +3.87 units, 95 % CI [2.64, 5.10]. The title's claim is the
>     opposite of what the data showed.
> 2. **It describes a design that was abandoned.** Its methods and results sections
>     assume the 288-item, three-level v1 set (T1/T2/T3). The study ran the
>     384-item 2×2 register × tightness design.
>
> **Results are in `REPORT.md`.** This file is kept as evidence of what was
> committed to before the run, per `prereg/amendments.md`.

Draft written before data, as the preregistration requires. Every number is `[BLANK]` until the analysis script fills it. Written for the case that the TOST passed; Section 7 holds the alternative text if H1 is supported. Preregistration: `prereg/preregistration.md` (OSF DOI `[BLANK]`).

## Abstract

Lu et al. (2026) showed that a model's projection on the "Assistant Axis" falls over therapy and philosophy conversations and holds in coding conversations. Work on poetic jailbreaks (Bisconti et al. 2025; Icaro Lab 2026; Gerbrandt 2026) suggests that loose, associative prompt *form* might push a model off its assistant persona independently of content. We tested this directly. For 96 content briefs across four domains we wrote three prompts differing only in form tightness (loose free verse, structured prose, strictly constrained form), matched on token count (|r| = `[BLANK]`) and base-model log-perplexity (|r| = `[BLANK]`), and measured Qwen3-32B's response-token projection on the published axis at layer 32 (864 generations). The loose − tight contrast was `[BLANK]` units (90 % CI `[BLANK]`, `[BLANK]`), inside the preregistered equivalence bounds of ±3 units (one third of Lu et al.'s turn-0 domain gap). The result held with perplexity and token covariates (adjusted estimate `[BLANK]`), on our independently re-derived axis (cosine with published `[BLANK]`), and in Gemma-2-27B (`[BLANK]` scaled units, 90 % CI `[BLANK]`). Capping did not interact with form (interaction `[BLANK]`, 90 % CI `[BLANK]`). Within the limits of a single-turn design, how a request is phrased does not move the model along the Assistant Axis; what is asked does. Code, stimuli, projections and the preregistration are released.

## 1. Introduction

Three results were on the table and had never been put together.

1. **Lu et al. (2026)** defined the Assistant Axis as the direction from the mean of 275 role-persona activations to the default-assistant activation. In their Fig. 24, Qwen3-32B's projection on this axis drops by roughly 20–27 units over a therapy conversation and stays flat in a coding conversation. Capping the projection at the default level reduced harmful persona drift.
2. **Bisconti et al. (2025)** and the Icaro Lab **AHB** benchmark showed that rewriting a harmful request as poetry defeats refusal across many models, with hand-crafted poems working best.
3. **Gerbrandt (2026)** showed a single hand-built poem inducing role bleed in Claude Fable 5.

Results 2 and 3 are about form; result 1 is about content domain. But Lu's therapy and philosophy prompts are also, as text, looser than their coding prompts, so the domain effect could carry a form component. Conversely, the poetic jailbreak results could be a content effect in disguise (the poem changes what is being asked, not only how). Nobody had varied form with content fixed.

We did. The question is narrow: with content, token count and perplexity held constant, does loose form lower a model's Assistant-Axis projection?

We fixed before data a smallest effect of interest of 3 units, equivalence bounds of ±3, and a power analysis showing > 0.98 probability of declaring equivalence under an exact null and 0.99 power to detect a 3-unit effect.

## 2. Methods

Full detail in the preregistration. Summary:

**Stimuli.** 4 domains (coding, writing, therapy-like, philosophy-of-AI) × 24 topics × 3 tightness levels = 288 prompts. Each topic is a fixed content brief. T3 (tight) uses hard checkable constraints modelled on Gwern's "pressure-cooker" summary and the STRICT TRIADIC v2 spec. T2 (structured) is a normal structured request. T1 (loose) is free-verse / associative / second-person with no constraints, modelled on the form of Icaro's "adversarial_poetry" and "adversarial_stream" methods with benign content. Selected from a 3× candidate pool by deterministic stratified matching (seed 20261030) on Qwen3 token count and Qwen3-14B-Base log-perplexity.

**Manipulation check.** A rater blind to condition, outputs and hypothesis scored all 288 on a five-item 0–10 form rubric. Mean rubric score: T1 `[BLANK]`, T2 `[BLANK]`, T3 `[BLANK]`; adjacent d = `[BLANK]`, `[BLANK]`; ICC(2,1) on 60 items = `[BLANK]`. Decorrelation: r(tightness, log-ppl) = `[BLANK]`, r(tightness, tokens) = `[BLANK]`.

**Gates run before stimuli.** (a) Axis re-derivation from 48 stratified roles on a 4-bit model: cosine with the published layer-32 axis = `[BLANK]` (pass threshold 0.9; subset ceiling mean 0.9885, 5th pct 0.9806). (b) Refusal-direction cosine (Arditi et al. 2024 recipe) with the axis: `[BLANK]` at layer 32, max over layers `[BLANK]` at layer `[BLANK]`; interpretation band `[BLANK]`. (c) Exploratory: on `[BLANK]` re-projected assistant turns from the released Qwen case-study and Gemma drift transcripts, user-turn tightness slope = `[BLANK]` (95 % CI `[BLANK]`).

**Models and measurement.** Qwen3-32B in 4-bit NF4, no system prompt, thinking off, temperature 0.7, top-p 0.9, three samples per stimulus. Projection = mean over response tokens (thinking spans and code blocks excluded as in Lu's `SpanMapper`) of the post-MLP residual at layer 32 on the unit-normalised published axis. Arm 2 adds Lu's published capping config for Qwen (`layers_46:54-p0.25`), which we verified is a floor at the default-assistant level (capping vector = −axis, cos −1.0000). Arm 3 repeats Arm 1 on Gemma-2-27B-it at layer 22.

**Analysis.** Linear mixed model `projection ~ level + domain + (1|topic) + (1|topic:level)`, T3 reference. TOST on the T1 − T3 contrast, bounds ±3, 90 % CI. Secondary fit with log-perplexity and token count. Preregistered rule: an adjusted estimate differing from the unadjusted by > 1 unit means decorrelation failed.

**Deviations from Lu et al.** 4-bit vs bf16; 48 roles vs 275 and 12 questions vs 240 for re-derivation; judge via OpenRouter; transformers `generate` vs vLLM; Qwen3-14B-Base for perplexity; Llama-3.3-70B excluded (24 GB GPU).

## 3. Results

### 3.1 Arm 1 — form tightness and projection (Qwen3-32B)

`[BLANK]` of 864 generations were projected (`[BLANK]` excluded as empty; `[BLANK]` hit the token limit, kept and flagged; `[BLANK]` refusals, kept).

| Level | mean projection | SD | n |
|---|---|---|---|
| T1 loose | `[BLANK]` | `[BLANK]` | `[BLANK]` |
| T2 structured | `[BLANK]` | `[BLANK]` | `[BLANK]` |
| T3 tight | `[BLANK]` | `[BLANK]` | `[BLANK]` |

T1 − T3 contrast: `[BLANK]` units, 90 % CI [`[BLANK]`, `[BLANK]`], 95 % CI [`[BLANK]`, `[BLANK]`]. Both TOST one-sided tests rejected (p = `[BLANK]`, `[BLANK]`): **equivalence within ±3 units declared.** Linear trend: `[BLANK]` units per level, 95 % CI [`[BLANK]`, `[BLANK]`]. Random effects: topic SD `[BLANK]`, topic:level SD `[BLANK]`, residual SD `[BLANK]` (preregistered assumption 8; pilot estimate on first 24 topics `[BLANK]`).

Covariate-adjusted T1 − T3: `[BLANK]` (difference from unadjusted `[BLANK]`, inside the 1-unit rule). Re-derived axis: `[BLANK]` (90 % CI `[BLANK]`).

Sensitivity: without token-limit hits `[BLANK]`; without refusals `[BLANK]`.

Per-domain contrasts (exploratory): coding `[BLANK]`, writing `[BLANK]`, therapy-like `[BLANK]`, philosophy-of-AI `[BLANK]`. Domain main effects (for scale): therapy-like − coding `[BLANK]`, to compare with Lu's turn-0 gap of 6–12.

### 3.2 Arm 2 — capping

Level × capping interaction (T1 × capped): `[BLANK]`, 90 % CI [`[BLANK]`, `[BLANK]`]. Gap-reduction ratio `[BLANK]` (criterion ≥ 0.50). Capping main effect `[BLANK]`. Role adoption (0–3): T1 unsteered `[BLANK]`, T1 capped `[BLANK]`, T3 unsteered `[BLANK]`, T3 capped `[BLANK]`; T1 unsteered vs capped p = `[BLANK]`. With no Arm 1 gap to remove, the interaction test is uninformative about form; the main effect confirms the capping config behaves as a floor on our stimuli.

### 3.3 Arm 3 — Gemma-2-27B

Gemma role-SD at layer 22 `[BLANK]`; scaled SESOI `[BLANK]`. T1 − T3 `[BLANK]`, 90 % CI [`[BLANK]`, `[BLANK]`]; equivalence `[declared / not declared]`.

### 3.4 Exploratory

Rubric sub-items: `[BLANK]`. Response length ~ projection r = `[BLANK]`. 2-turn extension on 24 topics: T1 − T3 at turn 2 `[BLANK]`.

## 4. Discussion

With content fixed and surface statistics matched, form tightness did not move Qwen3-32B along the Assistant Axis by more than 3 units in either direction, in a design with power 0.99 to detect that size. The same held on an axis we derived independently and in a second model family. Lu et al.'s domain effect, measured in our stimuli as `[BLANK]` units at turn 0, is therefore not explained by the looser text of therapy or philosophy prompts. The poetic-jailbreak literature's effect, whatever its mechanism, is not visible as a persona-axis shift on benign content at a single turn.

What this does not show. (1) Multi-turn: Lu's large effects are at the end of long conversations; a small form effect could compound. Our 24-topic 2-turn extension gives `[BLANK]`, which is `[consistent / inconsistent]` with no compounding, but is exploratory. (2) Harmful content: we used benign briefs; form may matter only where refusal is in play. Gate (b) found the refusal direction `[separate from / possibly the same as]` the axis (cos `[BLANK]`), which `[does / does not]` leave room for a form effect on refusal that bypasses the axis. (3) Tightness as we defined it (rubric, five items) may not be the dimension that matters; Gerbrandt's poem and Gwern's v4.2 prompt were not available to us verbatim. (4) Models were 4-bit.

What it does show. The Assistant-Axis projection is, at least at turn 0, a measure of what is being asked and not how. That is useful for anyone using the axis as a monitor: a loose or poetic phrasing of a benign request should not trip it, and a drop should be read as content-driven.

## 5. What would make this wrong

Concrete failure modes, each with the check we ran:

- **Axis mis-derivation.** If our projection target were wrong (wrong layer, wrong normalisation, wrong token span), a null is guaranteed. Check: published axis used as primary; re-derived axis cosine `[BLANK]` ≥ 0.9; reproduction of the published axis from the published role vectors at cos 0.9998; domain main effect `[BLANK]` compared with Lu's 6–12, which should be recovered if the measurement works. If the domain effect is not recovered, this null is uninterpretable and we say so.
- **Rater leakage.** If the blind rater inferred condition, the manipulation check is inflated. Check: rater saw text only in shuffled order; LLM-rater prompt is the rubric file verbatim and is logged; a 60-item second rater gave ICC `[BLANK]`.
- **Perplexity / length confound.** If T1 and T3 differ in base-model surprise or length, a form effect could be masked by an opposing surface effect (or vice versa). Check: |r| < 0.10 on both; adjusted estimate within 1 unit of unadjusted (`[BLANK]`). A failure of the 1-unit rule would be reported in the abstract.
- **Capping sign error.** If the capping vector were applied with the wrong sign, Arm 2 would push the model *away* from the assistant. Check: capping vector = −axis exactly; threshold = default-assistant projection; capping main effect `[BLANK]` must be positive (toward assistant) on the raw projection.
- **Quantisation.** 4-bit weights could flatten the axis. Check: re-derivation cosine on the 4-bit model (gate a) and the recovered domain effect.
- **Stimulus homogeneity.** If T1 prompts were not actually loose in the way poetic jailbreaks are, we tested the wrong thing. Check: rubric scores by item; qualitative comparison with AHB "adversarial_poetry" items (form reference only).
- **Underpowered variance assumption.** If residual SD was far above 8, the TOST would fail to declare equivalence rather than declare it falsely — a null here is therefore not a power artefact. Observed residual SD `[BLANK]`.

## 6. Data and code

Repo `[BLANK]`; OSF `[BLANK]`. `stimuli/stimuli.jsonl` (sha256 `[BLANK]`), `stimuli/manifest.json` (sha256 `[BLANK]`), per-generation projections and outputs in `results/`, judge scores, `pipeline/run_all.sh`, environment lockfile.

## 7. Alternative results section — if H1 is supported

Use in place of 3.1's conclusion and section 4 if the one-sided test and trend both reject.

T1 − T3 = `[BLANK]` units (90 % CI [`[BLANK]`, `[BLANK]`]), one-sided p = `[BLANK]`; trend `[BLANK]` per level, p = `[BLANK]`. Relative to Lu's turn-0 domain gap of 6–12 units, the form effect is `[BLANK]` % of the domain effect. Covariate-adjusted `[BLANK]` (rule `[met / not met]`). Re-derived axis `[BLANK]`. Gemma `[BLANK]` scaled units, `[replicated / not replicated]`.

Arm 2: interaction `[BLANK]`, gap-reduction `[BLANK]`; capping `[did / did not]` remove ≥ 50 % of the gap. Role adoption fell from `[BLANK]` to `[BLANK]` under capping in T1.

Discussion (alternative). Loose form moves the model away from the assistant persona even when content, length and perplexity are fixed. This means part of Lu's domain effect may be form, and that the poetic-jailbreak results have a persona-level correlate independent of harmful content. If capping removed the gap, the effect is on the axis itself and capping is a sufficient defence for it; if capping did not, form acts through a path capping does not touch, which is the more important finding. Caveats (single turn, benign content, 4-bit, rubric definition of tightness) apply unchanged. The failure modes in Section 5 apply in reverse: an H1 result could be a perplexity confound (rule), rater leakage (ICC), or a sign error (checked); a positive result with the domain effect not recovered is equally uninterpretable.

## 8. Inconclusive case

If neither the one-sided test nor the TOST rejects, report the estimate and both CIs, state that the design had 0.99 power at 3 units under the preregistered variance and that the observed residual SD was `[BLANK]`, and do not claim either direction.

## References

As in the preregistration.
