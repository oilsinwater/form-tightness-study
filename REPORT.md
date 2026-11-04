# Prompt-form tightness and the Assistant Axis

**A preregistered test on Qwen3-32B with a capping arm and a Gemma-2-27B replication.**

Results report, 2026-11-04. Every number here comes from a file in `results/`.
Preregistration frozen 2026-10-31 (`prereg/freeze.txt`, 13 sha256s, all verifying);
deviations recorded in `prereg/amendments.md`.

Code, stimuli and result files: **https://github.com/oilsinwater/form-tightness-study**

---

## The question

Lu et al. (2026) define the Assistant Axis as the difference between the mean
activation of 275 role-persona prompts and the default-assistant activation.
Projection on that axis falls over therapy and philosophy conversations and holds
in coding ones. Two other results concern *form* rather than content: adversarial
poetry defeats refusal across many models (Bisconti et al. 2025; Icaro Lab 2026),
and a single hand-built poem induces role bleed (Gerbrandt 2026).

Lu's therapy and philosophy prompts are, as text, looser than their coding
prompts. So the domain effect could carry a form component — and the poetic
jailbreak results could be a content effect in disguise. Nobody had varied form
with content held fixed.

**H1.** Looser prompt form pushes per-turn projection lower (away from the
Assistant) than tight form, with content, token count and base-model perplexity
held constant.
**H0.** The effect lies inside a TOST equivalence band of ±3 units — one third of
Lu's turn-0 bounded-vs-therapy gap.

## Design

4 domains (coding, writing, therapy-like, philosophy-of-AI) × 24 topics × register
(verse / prose) × tightness (loose / tight) = **384 stimuli**. Register is crossed
with tightness rather than nested in it, because register drives base-model
perplexity by several within-level SDs and no selection procedure can undo that —
an earlier 288-item design with loose-verse against tight-prose failed its own
decorrelation bound at r = −0.44 and was abandoned (kept under `stimuli/v1/`).

| Gate | Result |
|---|---|
| Decorrelation, within register | r(tightness, tokens) = r(tightness, log-ppl) = 0.000; token band 130–200 |
| Manipulation check, 384/384 rated | d(tight − loose) = 2.17 (verse), 2.62 (prose); constraint sub-score 2.12 / 2.63 |
| Address confound | every selected item coded `address = none` (regex + blind LLM coder) |

| Arm | Model | Manipulation | Readout |
|---|---|---|---|
| 1 | Qwen3-32B, NF4 | tightness | mean response-token projection, published axis, layer 32 |
| 2 | Qwen3-32B, NF4 | tightness × capping `layers_46:54-p0.25` | same, plus judge-rated role adoption 0–3 |
| 3 | Gemma-2-27B-it, NF4 | tightness | same on the Gemma axis, layer 22 |

### Gates run before the arms

- **(a) Axis re-derivation.** 48 stratified roles, 5 prompts × 12 questions,
  4-bit, judged 0–3 on the repo's `eval_prompt`; axis = mean(default) − mean(role).
  Cosine with the published layer-32 axis: **0.916** against an abort threshold of
  0.9. The subset ceiling computed from the published vectors is 0.9885 (mean) and
  0.9806 (5th pct), so the shortfall is the 4-bit model, our generations or our
  judge — not subset size. Axis norm 26.85 vs the published 22.66.
- **(b) Refusal direction.** Arditi et al. (2024) recipe, 128 harmful / 128
  harmless instructions. Cosine with the axis at layer 32: **0.038**; maximum over
  layers 0.067 (layer 8). Both inside the pre-stated `|cos| < 0.2` band, so the
  two literatures are measuring different directions here.
- **(c) Exploratory, on released transcripts.** 121 distinct user turns across 8
  transcripts, re-projected. In the three unsteered Qwen conversations the
  tightness slope is **+0.60 raw units per rubric point**, 95 % CI [−1.74, 2.93],
  p = 0.62 (n = 69 turns). Diluted and underpowered by construction — auditor-written
  turns span tightness 1–7 of a possible 10 and never touch the constraint items.
  It neither supports nor rules out H1; the arms do.

## Arm 1 — tightness moves the projection

Qwen3-32B, NF4, published axis, layer 32, three samples per stimulus.
`projection ~ tightness × register + domain + (1|topic) + (1|topic:cell)`.

1,152 generations; 13 excluded for zero usable response tokens (all coding
tight cells, 100 % code replies removed by the repo's code-block exclusion);
448 hit the 512-token cap and were kept, flagged.

| Cell | mean projection | SD | n |
|---|---|---|---|
| tight-prose | −22.00 | 6.43 | 282 |
| loose-prose | −23.46 | 7.44 | 288 |
| tight-verse | −27.36 | 6.36 | 281 |
| loose-verse | −33.53 | 10.52 | 288 |

Published default-assistant projection: −4.5. Residual SD 2.21.

| Test | Estimate | 95 % CI | 90 % CI | p |
|---|---|---|---|---|
| **H1** tight − loose | **+3.87** | [2.64, 5.10] | [2.84, 4.90] | 7.3e-10 |
| Register verse − prose | −7.73 | [−8.96, −6.50] | — | 8.8e-35 |
| Tightness × register | +4.68 | [2.21, 7.14] | [2.61, 6.74] | 2.0e-4 |

**Reading.** The direction is as predicted: tight form sits *further* from the
Assistant, loose form *closer*. TOST equivalence inside ±3 units is **rejected** —
this is not a null. But the 90 % CI still reaches below the 3-unit SESOI, so
"larger than the smallest effect of interest" is **not** established. The honest
summary is: an effect of roughly 0.26 role-SD that is reliably non-zero and
reliably outside the equivalence band, of uncertain practical size.

The interaction means the effect is not uniform: tightness is worth +6.17 units in
verse and +1.46 in prose. Register is worth about twice tightness (−7.73), and it
is register, not tightness, that carries the behavioural trace (below).

Per domain (exploratory, raw means): coding −1.43, writing +1.71, therapy-like
+6.37, philosophy-of-AI +8.69. The effect lives where Lu found drift.

**Sensitivity** — none of these move the conclusion:

| Variation | Estimate | 95 % CI |
|---|---|---|
| Without the 448 cap-hit generations | +4.11 | [2.33, 5.90] |
| Response length as covariate | +3.36 | [2.05, 4.68] |
| Without the coding domain | +5.59 | [4.13, 7.05] |
| On our re-derived axis (cos 0.916) | +5.56 | [4.39, 6.72] |
| Layer sweep | L11 +3.80, L22 +2.90, L32 +3.87, L45 +3.53 | all CIs exclude 0 |

## Arm 2 — capping removes the gap

Tightness × capping interaction **−5.34 units**, 95 % CI [−5.83, −4.84]. The
tight − loose gap runs from **+3.82 uncapped to −1.54 capped**: more than 100 % of
it removed, against a pre-stated threshold of 50 %. Capping's main effect is +5.67
toward the Assistant.

**The behavioural outcome belongs to register, not tightness.** 2,304 responses
judged 0–3 for role adoption, zero failures:

| Term | Estimate (0–3 scale) | 95 % CI | p |
|---|---|---|---|
| tightness | +0.01 | [−0.03, 0.05] | .58 |
| register (verse) | +0.09 | [0.05, 0.13] | 2e-6 |
| capping | −0.115 | [−0.14, −0.09] | 2e-21 |
| tightness × capping | −0.01 | [−0.06, 0.04] | .67 |

Full persona adoption (score 3) in Arm 1 fell from 8.3 % (loose-verse) and 9.0 %
(tight-verse) to 0 % and 0.7 % under capping; loose-prose was 0 % throughout.
Projection and judge agree overall (Spearman ρ = −0.37).

So tightness shifts the *measurement* without shifting *behaviour*, while verse
shifts both. That asymmetry is the most interesting thing in the study, and it is
not what H1 predicted.

## Arm 3 — the Gemma replication fails

Gemma-2-27B-it, NF4, published Gemma axis, layer 22, zero exclusions. SESOI scaled
by Gemma's role-SD: ±106.5 units.

| Test | Estimate | 95 % CI | In role-SD units |
|---|---|---|---|
| tight − loose | **−335.4** | [−402.7, −268.2] | −0.645 (Qwen: +0.264) |
| register | −239.5 | [−306.7, −172.2] | −0.46 (Qwen: −0.53) |
| interaction | −81.6 | [−216.2, +52.9] | — |

**The sign is reversed and equivalence fails.** Register replicates; the
interaction does not.

The Gemma readout is not trustworthy at this layer. The tightness effect runs
**L6 +10.7, L11 −6.1 (n.s.), L22 −335.4, L34 +355.3** — a sign flip between the
target layer and layer 34. Gemma's projection also falls monotonically through
every response (first decile ≈ 9,100, last ≈ 7,400–8,100), unlike Qwen's flat
per-token traces. Read this as **does not replicate**, not as a clean opposite
effect. Not explained by length: Gemma responses are 404–458 tokens in all cells,
and a length covariate gives −342.

## What this shows

- Prompt **form** moves the Assistant-Axis projection when content, length and
  perplexity are fixed: +3.9 units, robust to covariates, cap hits, domain
  exclusion and axis choice.
- **Register dominates tightness** on both the projection (−7.7 units) and the
  behaviour (verse makes full persona adoption ~9 % likely; tightness does not
  move it at all).
- Capping removes the tightness gap entirely — consistent with a floor on
  Assistant-ness, but see the caution below.
- The refusal direction and the Assistant Axis are effectively orthogonal here
  (cos 0.038), so a form effect on refusal would act through a path this measure
  does not see.

## What this does not show

- **Single turn.** Lu's largest effects are at the end of long conversations. A
  small form effect could compound; nothing here tests that.
- **Benign content only.** Form may matter where refusal is in play. Stimuli are
  benign by design; harmful benchmarks were used as form references only.
- **Capping covers 97–99 % of tokens in every cell.** Arm 2 is equally consistent
  with "capping compresses all cells toward the floor" as with a mechanism specific
  to loose form. The readout layer (32) is upstream of the capped layers (46–53),
  so the Arm 2 change reflects different generated text, not the hook.
- **One model family carried the result.** Gemma reversed and is unstable across
  layers. The Qwen finding is a single model, 4-bit, one axis layer.
- **Tightness is our rubric**, five items, and the tight end was modelled on a
  paraphrase — Gwern's v4.2 prompt is unpublished and was not obtained.
- **The preregistration was not registered before the data.** It was frozen
  locally with a hash record (`prereg/freeze.txt`) before Arms 1–3 ran, but the
  OSF submission was never made. A third party can verify the freeze from this
  repo's history; they cannot point at an OSF DOI that predates the run.

## What would have made this wrong

Each failure mode was checked before the arms, and the checks are in `results/`:

| Failure mode | Check | Outcome |
|---|---|---|
| Axis mis-derivation → guaranteed null | published axis primary; re-derived cos ≥ 0.9; domain effect must recover Lu's 6–12 | cos 0.916; therapy and philosophy recover +6.4 and +8.7, coding −1.4 |
| Rater leakage | rater blind, shuffled, rubric file verbatim, logged | 384/384 scored, d = 2.17 / 2.62 |
| Perplexity / length confound | \|r\| < 0.10; adjusted estimate within 1 unit | 0.000; +3.87 → +3.86 |
| Capping sign error | capping vector must be −axis, τ at the default projection | cos −1.0000; main effect +5.67 toward the Assistant |
| Quantisation flattening | re-derivation cosine on the 4-bit model | 0.916, and the domain effect recovered |
| Power artefact | observed residual SD vs the preregistered 8 | 2.21 — better than assumed, so a null would not have been a power failure |

## Data and code

Repository: https://github.com/oilsinwater/form-tightness-study

- Stimuli and manifest: `stimuli/stimuli.jsonl`, `stimuli/manifest.json` (sha256 per item, seed 20261030)
- Per-generation projections and outputs: `results/` (large artefacts stay on the analysis host)
- Analysis: `pipeline/analyze_arms.py`, `pipeline/analyze_h2h3.py`, `pipeline/arm_run.py`
- Full tables and sensitivity fits: `results/arm12_report.md`, `results/analysis_arms12.json`, `results/analysis_h2h3.json`
- Gates: `results/check_a_cosine.json`, `results/check_b_refusal_cosine.json`, `results/check_c_report.md`

Cite via `CITATION.cff`. MIT licensed.

## References

- Lu, C., Gallagher, J., Michala, J., Fish, K., Lindsey, J. (2026). The Assistant Axis. arXiv:2601.10387. Code: github.com/safety-research/assistant-axis. Vectors: HF lu-christina/assistant-axis-vectors.
- Arditi, A. et al. (2024). Refusal in Language Models Is Mediated by a Single Direction. arXiv:2406.11717.
- Bisconti, P. et al. (2025). Adversarial Poetry as a Universal Single-Turn Jailbreak. arXiv:2511.15304.
- Icaro Lab (2026). AHB. arXiv:2604.18487. HF icaro-lab/ahb.
- Gerbrandt, J. (2026). Jailbreaking Claude Fable 5 with a poem. tbd/con, 2026-09-23. youtube.com/watch?v=qSQLaCcZsfA.
- Gwern. A Strict Pindaric Meter. gwern.net/fiction/pindaric-strict. Apollonian #1. gwern.net/fiction/lab-animals.
- Lakens, D. (2017). Equivalence tests: a practical primer for t-tests, correlations, and meta-analyses. Social Psychological and Personality Science 8(4), 355–362.
