# Selection report (v2, 2x2 register x tightness)

Generated 2026-10-31T04:24:14-0700. Pool: 1152 candidates ({'v1_reuse': 511, 'v2_gen': 641}; generator deepseek/deepseek-v4-pro; endpoint https://api.commandcode.ai/provider/v1). Selected 384 stimuli ({'v1_reuse': 171, 'v2_gen': 213}), seed 20261030, 20 random restarts of greedy coordinate descent. Selected items inside the 130–200 token band: 384/384; len_ok violations: 0.

## Decorrelation

Targets: |r(tightness, tokens)| < 0.1 and |r(tightness, log-ppl)| < 0.1 overall and within each register; per-domain mean token spread across the four cells < 10%. **r gate: FAIL. Spread gate: PASS. Overall: FAIL**

| scope | n | r(tightness, tokens) | r(tightness, log-ppl) |
|---|---|---|---|
| all | 384 | +0.063 | +0.034 |
| verse | 192 | -0.001 | +0.000 |
| prose | 192 | +0.154 | +0.154 |

### Per domain

| domain | r tok (all) | r lpp (all) | r tok (verse) | r lpp (verse) | r tok (prose) | r lpp (prose) | token spread |
|---|---|---|---|---|---|---|---|
| coding | +0.052 | -0.059 | -0.102 | -0.043 | +0.221 | -0.272 | 8.0% |
| philosophy_of_ai | +0.013 | +0.025 | +0.114 | -0.185 | -0.146 | +0.364 | 9.4% |
| therapy_like | +0.091 | +0.200 | -0.020 | +0.235 | +0.265 | +0.628 | 9.6% |
| writing | +0.098 | -0.015 | +0.007 | -0.007 | +0.243 | -0.074 | 8.0% |

### Cell means (all domains)

| cell | n | mean tokens (SD) | mean log-ppl (SD) |
|---|---|---|---|
| loose_verse | 96 | 160.9 (19.3) | 3.578 (0.331) |
| tight_verse | 96 | 160.8 (21.6) | 3.578 (0.271) |
| tight_prose | 96 | 154.7 (17.6) | 2.581 (0.277) |
| loose_prose | 96 | 149.9 (12.4) | 2.502 (0.230) |

### Per-domain cell means: tokens / log-ppl

| domain | loose_verse tok | tight_verse tok | tight_prose tok | loose_prose tok | loose_verse lpp | tight_verse lpp | tight_prose lpp | loose_prose lpp |
|---|---|---|---|---|---|---|---|---|
| coding | 166.3 | 162.2 | 162.3 | 154.1 | 3.572 | 3.544 | 2.346 | 2.470 |
| philosophy_of_ai | 158.4 | 162.9 | 149.0 | 152.5 | 3.717 | 3.620 | 2.810 | 2.663 |
| therapy_like | 159.4 | 158.5 | 152.9 | 145.4 | 3.467 | 3.597 | 2.695 | 2.371 |
| writing | 159.3 | 159.6 | 154.5 | 147.8 | 3.556 | 3.552 | 2.471 | 2.502 |

For comparison, over the full pool before selection: all: r_tok = +0.212, r_lpp = +0.261; verse: r_tok = +0.144, r_lpp = +0.309; prose: r_tok = +0.298, r_lpp = +0.622. Pool rows outside the 130–200 token band: 0.

### Search log

```
restart 0: obj=0.2575 all:tok+0.073/lpp+0.038 verse:tok-0.000/lpp+0.000 prose:tok+0.168/lpp+0.168 maxspread=0.086 sweeps=3
restart 2: obj=0.2548 all:tok+0.072/lpp+0.037 verse:tok-0.000/lpp+0.000 prose:tok+0.165/lpp+0.167 maxspread=0.088 sweeps=3
restart 4: obj=0.2406 all:tok+0.067/lpp+0.035 verse:tok+0.000/lpp+0.000 prose:tok+0.157/lpp+0.157 maxspread=0.091 sweeps=3
restart 10: obj=0.2394 all:tok+0.064/lpp+0.034 verse:tok-0.001/lpp+0.000 prose:tok+0.157/lpp+0.157 maxspread=0.099 sweeps=4
restart 11: obj=0.2359 all:tok+0.063/lpp+0.034 verse:tok-0.001/lpp+0.000 prose:tok+0.154/lpp+0.154 maxspread=0.096 sweeps=6
search done in 18s, objective=0.2359
```
