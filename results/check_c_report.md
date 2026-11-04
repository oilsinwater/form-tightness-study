# Check (c): does prompt-form tightness predict per-turn Assistant-Axis projection in Lu et al.'s released transcripts?

*Exploratory, pre-stimulus, underpowered. This is a description of the released transcripts, not a test of H1. Every number below comes from `results/check_c_model.json`, computed by `pipeline/check_c_model.py` from `results/check_c_projections.csv`, `results/check_c_user_tightness.csv` and `results/check_c_summary.json`.*

## Rating

- Rater: `deepseek/deepseek-v4.1-flash` via CommandCode, temperature 0, seed 20261030, system prompt = `stimuli/tightness-rubric.md` verbatim, user message = the user turn text only (blind to projection, assistant text, transcript, turn index). All 121 items returned via json_schema; 0 parse failures.
- **121 distinct user turns rated** (deduplicated by sha256 across 166 transcript rows). Shared user turns within capped/unsteered pairs: delusion 0/23, jailbreak 14/15, selfharm 31/31 — the delusion pair shares no user turns (the auditor adapted its turns), so ratings are shared only for selfharm and most of jailbreak.
- Tightness total over the 121 distinct turns: mean 2.83, SD 1.21, range 1–7 of a possible 0–10. Counts by total: 1: 23, 2: 23, 3: 32, 4: 40, 5: 2, 7: 1.
- Item means (0–2): item1 0.07 (SD 0.34), item2 0.02 (SD 0.20), item3 1.64 (SD 0.50), item4 1.09 (SD 0.82), item5 0.01 (SD 0.09). Items 1, 2 and 5 (hard constraints, output format, verification hooks) are almost always 0: nearly all the variance comes from items 3 and 4 (syntactic completeness, figurative density). The upper half of the rubric scale is empty in this corpus.

### Rating distribution per transcript

| transcript | model | n turns | tightness mean | SD | min–max | distinct totals | projection mean (raw) | projection SD (raw) |
|---|---|---|---|---|---|---|---|---|
| delusion_capped.json | qwen | 23 | 1.70 | 0.97 | 1–4 | 4 | -27.96 | 2.95 |
| delusion_unsteered.json | qwen | 23 | 2.04 | 1.02 | 1–4 | 4 | -49.93 | 5.38 |
| jailbreak_capped.json | qwen | 15 | 3.87 | 0.64 | 2–5 | 4 | -14.67 | 6.09 |
| jailbreak_unsteered.json | qwen | 15 | 3.87 | 0.64 | 2–5 | 4 | -36.02 | 9.62 |
| philosophy.json | gemma | 14 | 2.50 | 0.76 | 2–4 | 3 | 7946.38 | 283.44 |
| selfharm_capped.json | qwen | 31 | 3.55 | 0.62 | 2–4 | 3 | -17.77 | 3.89 |
| selfharm_unsteered.json.json | qwen | 31 | 3.55 | 0.62 | 2–4 | 3 | -40.24 | 8.41 |
| writing.json | gemma | 14 | 3.50 | 1.29 | 2–7 | 5 | 7920.54 | 713.26 |

**Variance note.** Within-transcript SD of tightness is 0.62–1.29 points, against an overall SD of 1.21 and a planned stimulus manipulation spanning the full 0–10 scale. The conversations do vary in form (some turns are terse fragments, some are complete literal prose), but only across the bottom ~40 % of the rubric: no turn asks for hard structural constraints, a format, or a self-check. So this check can only speak to the loose end of the tightness range, and a null here says little about H1 at the planned T1–T3 contrast. Transcripts with SD < 0.8: jailbreak_capped.json, jailbreak_unsteered.json, philosophy.json, selfharm_capped.json, selfharm_unsteered.json.json.

## Mixed models (statsmodels MixedLM, REML, random intercept per transcript)

Projection z-scored within model (Qwen L32 and Gemma L22 axes are on different scales, ~35×; raw values never pooled). `turn_index` is the position of the turn in the conversation (0-based).

**(i) Qwen unsteered, z-scored projection** — `z_projection ~ tightness_total + turn_index`, n = 69 turns, 3 transcripts, ICC(transcript) = 0.44, converged = True

| term | estimate | 95% CI | p |
|---|---|---|---|
| Intercept | -0.508 | [-1.321, 0.305] | 0.221 |
| tightness_total | 0.043 | [-0.126, 0.212] | 0.617 |
| turn_index | -0.036 | [-0.053, -0.019] | 0.000 |

**(i) Qwen unsteered, raw projection units** — `projection ~ tightness_total + turn_index`, n = 69 turns, 3 transcripts, ICC(transcript) = 0.44, converged = True

| term | estimate | 95% CI | p |
|---|---|---|---|
| Intercept | -38.533 | [-49.752, -27.313] | 0.000 |
| tightness_total | 0.596 | [-1.738, 2.931] | 0.617 |
| turn_index | -0.494 | [-0.728, -0.260] | 0.000 |

**(ii) Qwen all 6 transcripts (capped indicator + interaction), z-scored** — `z_projection ~ tightness_total + turn_index + capped + tightness_total:capped`, n = 138 turns, 6 transcripts, ICC(transcript) = 0.50, converged = True

| term | estimate | 95% CI | p |
|---|---|---|---|
| Intercept | -0.800 | [-1.477, -0.123] | 0.021 |
| tightness_total | 0.085 | [-0.051, 0.220] | 0.220 |
| turn_index | -0.021 | [-0.031, -0.011] | 0.000 |
| capped | 1.704 | [0.813, 2.594] | 0.000 |
| tightness_total:capped | -0.034 | [-0.217, 0.148] | 0.712 |

**(iii) Qwen + Gemma pooled, within-model z-scores, model fixed effect** — `z_projection ~ tightness_total + turn_index + C(model_short, Treatment('qwen'))`, n = 166 turns, 8 transcripts, ICC(transcript) = 0.73, converged = True

| term | estimate | 95% CI | p |
|---|---|---|---|
| Intercept | 0.378 | [-0.436, 1.193] | 0.363 |
| C(model_short, Treatment('qwen'))[T.gemma] | -0.176 | [-1.610, 1.259] | 0.810 |
| tightness_total | 0.003 | [-0.104, 0.109] | 0.963 |
| turn_index | -0.032 | [-0.045, -0.020] | 0.000 |

### Slope summary (per rubric point)

| model | slope per point | 95% CI | p | units |
|---|---|---|---|---|
| (i) Qwen unsteered | 0.043 | [-0.126, 0.212] | 0.617 | within-Qwen SD |
| (i) Qwen unsteered | 0.60 | [-1.74, 2.93] | 0.617 | raw Qwen L32 projection units (unsteered SD = 9.48) |
| (ii) Qwen all 6, main effect (unsteered) | 0.085 | [-0.051, 0.220] | 0.220 | within-Qwen SD |
| (ii) tightness × capped | -0.034 | [-0.217, 0.148] | 0.712 | within-Qwen SD |
| (iii) pooled Qwen+Gemma | 0.003 | [-0.104, 0.109] | 0.963 | within-model SD |

## Spearman ρ of tightness_total with projection, within transcript

| transcript | n | ρ | p |
|---|---|---|---|
| delusion_capped.json | 23 | 0.26 | 0.222 |
| delusion_unsteered.json | 23 | 0.15 | 0.490 |
| jailbreak_capped.json | 15 | 0.30 | 0.284 |
| jailbreak_unsteered.json | 15 | -0.03 | 0.928 |
| philosophy.json | 14 | 0.04 | 0.902 |
| selfharm_capped.json | 31 | 0.24 | 0.200 |
| selfharm_unsteered.json.json | 31 | 0.40 | 0.026 |
| writing.json | 14 | -0.21 | 0.466 |

## Capped vs unsteered mean projection per pair (Qwen, raw L32 units; from check_c_summary.json)

| pair | n turns | mean capped | mean unsteered | capped − unsteered | paired-by-turn mean diff (SD) | paired t | p |
|---|---|---|---|---|---|---|---|
| delusion | 23 | -27.96 | -49.93 | +21.97 | +21.97 (4.89) | 21.55 | 2.8e-16 |
| jailbreak | 15 | -14.67 | -36.02 | +21.35 | +21.36 (10.37) | 7.98 | 1.4e-06 |
| selfharm | 31 | -17.77 | -40.24 | +22.47 | +22.47 (6.58) | 19.02 | 2.7e-18 |

Capping raises the projection by roughly 20 raw units in every pair, i.e. about 2.3 unsteered SDs — an effect far larger than anything tightness is associated with here.

## Conclusion (plain language)

In the three unsteered Qwen transcripts, each extra rubric point of prompt tightness goes with a higher per-turn projection of 0.60 raw units (0.04 within-Qwen SD), 95 % CI [-1.74, 2.93], p = 0.62, which is not distinguishable from zero at this sample size (n = 69 turns, 3 conversations). The pooled estimate including Gemma (+0.003 SD per point, p = 0.96) and the all-Qwen estimate (+0.085 SD per point, p = 0.22) are likewise small, positive and not distinguishable from zero, with per-transcript Spearman ρ ranging -0.21 to 0.40. Because these auditor-written turns only span tightness totals 1–7 (almost entirely items 3–4, never constraints, format or verification hooks) and the capping manipulation dwarfs any form-related variation, this check is a weak, exploratory description that neither supports nor rules out H1; the preregistered stimulus arms are needed.
