# Prompt-form tightness and the Assistant Axis

**A preregistered test on Qwen3-32B with a capping arm and a Gemma-2-27B replication.**

Results report, 2026-11-04. Every number here comes from a file in `results/`.
Preregistration frozen 2026-10-31 (`prereg/freeze.txt`, 13 sha256s, all verifying);
deviations recorded in `prereg/amendments.md`.

**Audited 2026-11-04.** An audit of this report against the frozen preregistration and the
committed data found errors of direction, of attribution and of omission. They are corrected in
place below, and each correction is listed under [Audit corrections](#audit-corrections-2026-11-04).
Numbers the audit adds come from `results/audit_checks.json` (`pipeline/audit_checks.py`).

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
| Manipulation check, 384/384 rated | d(tight − loose) = 2.17 (verse), 2.62 (prose); constraint sub-score 2.12 / 2.63. **Partly met:** the frozen gate also requires ICC(2,1) ≥ 0.75 on a 60-item two-rater subset, which was never run (one LLM rater). The 384-item ratings are on the analysis host; the committed `stimuli/tightness_ratings.csv` is the 220-item freeze-time snapshot (d = 2.18 / 2.77) |
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
  harmless instructions. Cosine with the axis at layer 32: **0.038**; maximum |cos| over
  the layers Arditi retains 0.17 (layer 12, negative). Both inside the pre-stated
  `|cos| < 0.2` band, so the two literatures are measuring different directions
  here. (Unpruned, the final layer 63 reaches −0.34, in the "undetermined" band;
  Arditi's criterion excludes it.)
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
| Register verse − prose (H1b) | −7.73 | [−8.96, −6.50] | — | 8.8e-35 |
| **H4** tightness × register | +4.68 | [2.21, 7.14] | [2.61, 6.74] | 2.0e-4 |

**Reading.** The direction is as predicted: positive projection is more
Assistant-like, so loose form sits *further* from the Assistant and tight form
*closer*. Equivalence inside ±3 units is **not declared** — the 90 % CI is not
contained in the band, so this is not a null. But the same CI runs from 2.84,
inside the band, so the data are compatible with an effect smaller than the
SESOI and "larger than the smallest effect of interest" is **not** established.
The honest summary is: an effect of roughly 0.26 role-SD that is reliably
non-zero, of uncertain practical size — neither shown equivalent to zero nor
shown to exceed the SESOI.

The frozen H1 criterion also requires a negative linear trend over levels. That
clause belongs to the three-level v1 design; with two levels the trend is the
same contrast, so it adds nothing, and the criterion was not amended before
the freeze.

**H4** (preregistered, directional: the tightness effect is larger in verse) is
**not refuted** — its refutation rule is a 90 % upper bound below +3, and the
bound is 6.74 — and the point estimate is in the predicted direction. See the
self-reference caveat under [Audit corrections](#audit-corrections-2026-11-04):
the prose simple effect, and so H4, may be biased by an unbalanced stimulus
feature.

The interaction means the effect is not uniform: tightness is worth +6.17 units in
verse and +1.46 in prose. Register is worth about twice tightness (−7.73), and it
is register, not tightness, that carries the behavioural trace (below).

Per domain (exploratory, raw means): coding −1.43, writing +1.71, therapy-like
+6.37, philosophy-of-AI +8.69. The effect is largest where Lu found drift, but
these contrasts are not decorrelated: selection balanced perplexity only per
register, and within domain × register r(tightness, log-ppl) runs from −0.48
(writing prose) to +0.53 (therapy-like prose). Coding is also not comparable —
its tight cells lost all 13 excluded generations and the readout there covers
only the non-code fragments of the replies. Treat the per-domain pattern as
descriptive.

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

**H2's behavioural clause, as frozen, is met.** The frozen criterion is the
loose-cell contrast, capped vs uncapped, p < .05 — not the tightness × capping
interaction. In loose cells capping lowers the judge score by −0.11 (95 % CI
[−0.14, −0.08], p = 2e-12; stimulus-level paired t on 192 stimuli, p = 2e-5).
It is carried entirely by loose-verse (1.22 → 1.00); loose-prose sits at 1.00 in
both arms. Because the interaction is null, the drop is not specific to loose
form: capping lowers role adoption in tight cells about as much. Both readings
are reported; the earlier "not supported" verdict (`results/arm12_report.md`)
tested the interaction instead of the frozen contrast.

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
target layer and layer 34. Gemma's projection also falls steadily through every
response (first decile ≈ 8,700–9,200, last ≈ 7,400–8,100), unlike Qwen's flat
per-token traces, and 73–88 % of Gemma responses hit the 512-token cap — so the
response mean depends on where generation was cut off. Read this as **does not
replicate**, not as a clean opposite effect. Not explained by length: Gemma
responses are 404–458 tokens in all cells, and a length covariate gives −342.
The prereg's conservative topic-level paired check agrees (−335.4, 95 % CI
[−391.2, −279.7], 96 topics).

## What this shows

- Prompt **form** moves the Assistant-Axis projection when content, length and
  perplexity are fixed: +3.9 units, robust to the preregistered covariates, cap
  hits, domain exclusion and axis choice — in one model. It is not yet checked
  against the unbalanced second-person reference to the model (see the audit).
- **Register dominates tightness** on both the projection (−7.7 units) and the
  behaviour (verse makes full persona adoption ~9 % likely; tightness does not
  move it at all).
- Capping removes the tightness gap entirely, and lowers role adoption in loose
  cells — but it lowers it in tight cells too, so neither result shows a
  mechanism specific to loose form (see the caution below).
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
  OSF submission was never made. The repository's first commit is dated
  2026-11-04, after the arms ran, so **nothing external timestamps the freeze**:
  a third party can verify that the frozen files are unchanged since they were
  hashed, but not *when* they were hashed. The 2026-10-31 time is self-reported
  in `prereg/freeze.txt`.

## What would have made this wrong

Each failure mode was checked before the arms, and the checks are in `results/`:

| Failure mode | Check | Outcome |
|---|---|---|
| Axis mis-derivation → guaranteed null | published axis primary; re-derived cos ≥ 0.9; domain effect must recover Lu's 6–12 | cos 0.916. **Domain effect not computed for Qwen.** The figures previously given here (+6.4, +8.7, −1.4) are per-domain *tightness* contrasts, not the therapy − coding domain gap. `pipeline/audit_checks.py` computes it when run on the analysis host. On Gemma it is +128 units (0.25 role-SD), below Lu's 6–12 Qwen units (0.4–0.8 role-SD) |
| Rater leakage | rater blind, shuffled, rubric file verbatim, logged; ICC(2,1) ≥ 0.75 | 384/384 scored, d = 2.17 / 2.62; **ICC not run** (single rater). Register leaks into the total score (items 3–4), so the constraint sub-score is the cleaner index |
| Perplexity / length confound | \|r\| < 0.10; adjusted estimate within 1 unit | 0.000; +3.87 → +3.86 |
| Capping sign error | capping vector must be −axis, τ at the default projection | cos −1.0000; main effect +5.67 toward the Assistant |
| Quantisation flattening | re-derivation cosine on the 4-bit model, and the recovered domain effect | 0.916; domain effect not yet computed for Qwen (above) |
| Power artefact | observed residual SD vs the preregistered 8 | Per-sample residual 2.21, but the variance sits at the stimulus level: the primary SE is 0.63 against the 0.51 the power analysis assumed. Power at the SESOI is still high, but the equivalence test is weaker than the power table says |

## Audit corrections (2026-11-04)

The audit checked this report against the frozen preregistration, the code,
and the data committed here. Numbers below come from `results/audit_checks.json`
unless another file is named.

### Errors corrected in this report

| # | Was | Now | Source |
|---|---|---|---|
| 1 | "tight form sits *further* from the Assistant, loose form *closer*" | The reverse: positive = more Assistant-like, and tight − loose = +3.87 | `arm12_report.md` sign convention; cell means |
| 2 | Effect "reliably outside the equivalence band" | Equivalence is not declared, but the 90 % CI [2.84, 4.90] reaches into the band, so the data do not show the effect is outside it | `analysis_arms12.json` |
| 3 | Gate (b) maximum 0.067 at layer 8 | 0.17 at layer 12, in the layers Arditi retains (−0.34 at layer 63, unpruned) | `check_b_refusal_cosine.json`; the frozen prereg already says 0.17 |
| 4 | "Domain effect recovered: therapy +6.4, philosophy +8.7, coding −1.4" | Those are per-domain *tightness* contrasts. The domain gap the null write-up names as the measurement check was never computed for Qwen | `analysis_arms12.json` has no domain term |
| 5 | H2 behavioural "not supported" | The frozen criterion (loose cells, capped vs uncapped) is met, p = 2e-12. It is not specific to loose form | `audit_checks.json` → `H2_behavioural_frozen_criterion` |
| 6 | H4 missing from the headline | Reported: not refuted, direction as predicted | `analysis_arms12.json` |
| 7 | Gemma first decile ≈ 9,100 | 8,675–9,211 by cell | `audit_checks.json` |
| 8 | "A third party can verify the freeze from this repo's history" | The first commit postdates the arms; the freeze time is self-reported | `git log` |
| 9 | Residual SD 2.21 "better than assumed" | The primary SE (0.63) is worse than the power analysis assumed (0.51); the variance sits at the stimulus level | `analysis_arms12.json`; prereg power table |

### Gaps that affect validity (open)

1. **The Qwen results cannot be recomputed from this repo.** `arm_1_observation.csv`,
   `arm_2_capping.csv` and the final 384-item `tightness_ratings.csv` are only on the
   analysis host. The committed ratings file is the 220-item freeze-time snapshot. Until
   those files are committed, the H1, H2 and H4 numbers and the final manipulation check
   are claims, not evidence. Gemma's numbers do reproduce exactly from
   `results/arm_3_gemma.csv`.
2. **Residual confound: second-person reference to the model.** The v3 screen removed
   vocatives and identity attributions, but not "you" addressed to the model
   (`self_ref_count`). In prose, loose prompts carry 3.33 such references and tight prompts
   1.01 (d = 0.74, Mann-Whitney p = 1e-7). Verse is balanced (d = 0.24, p = .76). On Gemma
   each reference moves projection by +24 units (95 % CI [3, 45]). Adjusting for it moves
   Gemma's tightness effect from −335 to −304 and its interaction from −82 to −130. The
   Qwen fit has not been run. If the sign is the same in Qwen, the confound pulls the prose
   tightness contrast toward zero and **inflates H4**, since the imbalance sits only in prose.
3. **Manipulation-check gate only partly met.** ICC(2,1) ≥ 0.75 on a two-rater 60-item
   subset is part of the frozen gate and was never run. The single rater, MiniMax-M3, also
   generated the v3 verse stimuli, coded address and judged role adoption, so the
   instruments are not independent.
4. **Generation order was not shuffled.** The frozen text says order is shuffled and the
   three samples of a stimulus are not adjacent. `arm_run.py` runs stimuli in file order
   (domain → topic → cell), with the three samples side by side in one batch. Unless a run was resumed
   mid-way, every batch holds all four cells of one topic, so tightness is balanced within each batch and H1 is
   not confounded. Domain is confounded with run time.
5. **The Arm 2 model omits a stimulus × arm variance term**, so the SE of the
   tightness × capping term (0.25) may be too small. At z ≈ 21 this will not change the
   conclusion. `audit_checks.py` fits the fuller model when the CSVs are present.
6. **Preregistered analyses not reported:** the sensitivity fit without refusals (no refusal
   flag was computed), rubric sub-item regressions, the 2-turn continuation, the
   residual-SD pilot on the first 24 topics, and the topic-level paired df = 95 check for
   Qwen (run for Gemma above). The smoke-test file the prereg cites
   (`results/arm_smoke_v3.csv`) is not in the repo.
7. **The capping-coverage gate passes trivially.** 97–99 % of tokens fall below the cap in
   every cell, so the ≥ 25 % condition cannot tell mechanisms apart (see the caution
   under "What this does not show").

### What the audit does not change

The direction and approximate size of the Qwen H1 effect, the register effect, the Arm 2
projection interaction and the Gemma non-replication all follow from the numbers as
filed. Nothing contradicts them, provided the uncommitted CSVs are what
`analysis_arms12.json` says. The audit narrows what may be claimed from them. It does not
reverse any of them.

## Data and code

- Stimuli and manifest: `stimuli/stimuli.jsonl`, `stimuli/manifest.json` (sha256 per item, seed 20261030)
- Per-generation projections and outputs: `results/arm_3_gemma.csv` (Gemma) only. **The Arm 1 and Arm 2 per-generation CSVs and the final 384-item ratings are not in this repo** (they are on the analysis host, `~/form-tightness/results/`), so the Qwen numbers cannot be recomputed from the repo alone
- Analysis: `pipeline/analyze_arms.py`, `pipeline/analyze_h2h3.py`, `pipeline/arm_run.py`
- Full tables and sensitivity fits: `results/arm12_report.md`, `results/analysis_arms12.json`, `results/analysis_h2h3.json`
- Gates: `results/check_a_cosine.json`, `results/check_b_refusal_cosine.json`, `results/check_c_report.md`
- Audit: `pipeline/audit_checks.py` → `results/audit_checks.json`

Cite via `CITATION.cff`. MIT licensed.

## References

- Lu, C., Gallagher, J., Michala, J., Fish, K., Lindsey, J. (2026). The Assistant Axis. arXiv:2601.10387. Code: github.com/safety-research/assistant-axis. Vectors: HF lu-christina/assistant-axis-vectors.
- Arditi, A. et al. (2024). Refusal in Language Models Is Mediated by a Single Direction. arXiv:2406.11717.
- Bisconti, P. et al. (2025). Adversarial Poetry as a Universal Single-Turn Jailbreak. arXiv:2511.15304.
- Icaro Lab (2026). AHB. arXiv:2604.18487. HF icaro-lab/ahb.
- Gerbrandt, J. (2026). Jailbreaking Claude Fable 5 with a poem. tbd/con, 2026-09-23. youtube.com/watch?v=qSQLaCcZsfA.
- Gwern. A Strict Pindaric Meter. gwern.net/fiction/pindaric-strict. Apollonian #1. gwern.net/fiction/lab-animals.
- Lakens, D. (2017). Equivalence tests: a practical primer for t-tests, correlations, and meta-analyses. Social Psychological and Personality Science 8(4), 355–362.
