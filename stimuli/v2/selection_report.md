# Selection report (v2, 2x2 register x tightness)

Generated 2026-10-31T04:39:07-0700. Pool: 1344 candidates ({'v1_reuse': 511, 'v2_gen': 833}; generator deepseek/deepseek-v4-pro; endpoint https://api.commandcode.ai/provider/v1). Selected 384 stimuli ({'v1_reuse': 133, 'v2_gen': 251}), seed 20261030, 40 random restarts of greedy coordinate descent. Selected items inside the 130–200 token band: 384/384; len_ok violations: 0.

## Decorrelation

Targets: |r(tightness, tokens)| < 0.1 and |r(tightness, log-ppl)| < 0.1 overall and within each register; per-domain mean token spread across the four cells < 10%. **r gate: PASS. Spread gate: PASS. Overall: PASS**

| scope | n | r(tightness, tokens) | r(tightness, log-ppl) |
|---|---|---|---|
| all | 384 | -0.000 | -0.000 |
| verse | 192 | -0.001 | -0.000 |
| prose | 192 | +0.000 | -0.000 |

### Per domain

| domain | r tok (all) | r lpp (all) | r tok (verse) | r lpp (verse) | r tok (prose) | r lpp (prose) | token spread |
|---|---|---|---|---|---|---|---|
| coding | -0.007 | -0.053 | -0.021 | -0.006 | +0.011 | -0.254 | 1.5% |
| philosophy_of_ai | -0.025 | -0.037 | +0.017 | -0.132 | -0.079 | -0.035 | 4.5% |
| therapy_like | +0.029 | +0.176 | -0.026 | +0.266 | +0.095 | +0.571 | 4.4% |
| writing | +0.002 | -0.074 | +0.032 | -0.087 | -0.040 | -0.278 | 5.1% |

### Cell means (all domains)

| cell | n | mean tokens (SD) | mean log-ppl (SD) |
|---|---|---|---|
| loose_verse | 96 | 158.5 (18.0) | 3.598 (0.277) |
| tight_verse | 96 | 158.5 (20.6) | 3.598 (0.288) |
| tight_prose | 96 | 153.8 (17.4) | 2.539 (0.314) |
| loose_prose | 96 | 153.8 (12.7) | 2.539 (0.236) |

### Per-domain cell means: tokens / log-ppl

| domain | loose_verse tok | tight_verse tok | tight_prose tok | loose_prose tok | loose_verse lpp | tight_verse lpp | tight_prose lpp | loose_prose lpp |
|---|---|---|---|---|---|---|---|---|
| coding | 159.0 | 158.1 | 157.0 | 156.6 | 3.517 | 3.513 | 2.356 | 2.483 |
| philosophy_of_ai | 157.9 | 158.5 | 151.6 | 153.9 | 3.751 | 3.688 | 2.742 | 2.758 |
| therapy_like | 158.0 | 157.0 | 154.2 | 151.3 | 3.521 | 3.638 | 2.690 | 2.410 |
| writing | 159.1 | 160.2 | 152.4 | 153.5 | 3.605 | 3.555 | 2.367 | 2.505 |

For comparison, over the full pool before selection: all: r_tok = +0.190, r_lpp = +0.239; verse: r_tok = +0.144, r_lpp = +0.309; prose: r_tok = +0.235, r_lpp = +0.532. Pool rows outside the 130–200 token band: 0.

### Search log

```
restart 0: obj=0.0177 all:tok-0.000/lpp-0.000 verse:tok-0.001/lpp-0.000 prose:tok+0.000/lpp+0.000 maxspread=0.045 sweeps=4
restart 2: obj=0.0129 all:tok-0.000/lpp+0.000 verse:tok-0.001/lpp+0.000 prose:tok+0.000/lpp+0.000 maxspread=0.062 sweeps=3
restart 7: obj=0.0111 all:tok+0.000/lpp+0.000 verse:tok+0.000/lpp+0.000 prose:tok+0.000/lpp+0.000 maxspread=0.091 sweeps=5
restart 32: obj=0.0108 all:tok-0.000/lpp-0.000 verse:tok-0.001/lpp-0.000 prose:tok+0.000/lpp-0.000 maxspread=0.051 sweeps=3
search done in 75s, objective=0.0108
```

## Manipulation check (blind rubric rating)

Rater: `deepseek/deepseek-v4.1-flash` via `https://api.commandcode.ai/provider/v1`, temperature 0.0, seed 20261030, items in seeded random order, system prompt = `tightness-rubric.md` verbatim, user message = item text only, scores returned via response_format json_schema where accepted (parse modes: {'json_schema': 384}). Rated 384 / 384 items.

Pre-stated pass rule: within each register, mean rubric total tight > loose with Cohen's d > 1.0. verse: loose 2.11 vs tight 7.09, d = 3.81. prose: loose 3.60 vs tight 9.72, d = 4.46. Overall d(tight − loose) = 3.24. **PASS**

| cell | n | mean total (SD) | item1 | item2 | item3 | item4 | item5 |
|---|---|---|---|---|---|---|---|
| loose_verse | 96 | 2.11 (1.80) | 0.74 | 0.61 | 0.09 | 0.32 | 0.34 |
| tight_verse | 96 | 7.09 (0.41) | 2.00 | 2.00 | 0.10 | 1.03 | 1.96 |
| tight_prose | 96 | 9.72 (0.47) | 2.00 | 2.00 | 2.00 | 1.86 | 1.85 |
| loose_prose | 96 | 3.60 (1.88) | 0.64 | 0.56 | 0.72 | 1.33 | 0.35 |

### Register difference at equal tightness (rubric leakage signal; reported, not a gate)

| tightness | mean verse | mean prose | prose − verse | d | item1 Δ | item2 Δ | item3 Δ | item4 Δ | item5 Δ |
|---|---|---|---|---|---|---|---|---|---|
| loose | 2.11 | 3.60 | +1.49 | +0.81 | -0.10 | -0.05 | +0.62 | +1.01 | +0.01 |
| tight | 7.09 | 9.72 | +2.62 | +5.90 | +0.00 | +0.00 | +1.90 | +0.83 | -0.10 |

Items 3 and 4 of the rubric score the prompt's own syntax and figurative density, so a prose > verse difference at equal tightness is expected by construction; it means the rubric total is not a pure tightness score.

### Per domain

| domain | loose_verse | tight_verse | tight_prose | loose_prose | d verse | d prose |
|---|---|---|---|---|---|---|
| coding | 3.25 | 7.04 | 9.83 | 4.79 | 3.18 | 3.50 |
| philosophy_of_ai | 1.04 | 6.96 | 9.62 | 2.88 | 7.34 | 6.46 |
| therapy_like | 0.79 | 7.25 | 9.46 | 2.00 | 7.69 | 9.93 |
| writing | 3.38 | 7.12 | 9.96 | 4.75 | 3.39 | 5.49 |
