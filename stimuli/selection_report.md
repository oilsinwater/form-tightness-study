# Selection report (v3, 2x2 register x tightness, address = none)

Generated 2026-10-31T14:09:58-0700. Pool: 1536 candidates ({'v1_reuse': 274, 'v2_gen': 494, 'v3_gen': 768}; generators MiniMax-M3, deepseek/deepseek-v4-pro; endpoints https://api.commandcode.ai/provider/v1, https://api.minimax.io/v1). Address filter (both coders `none`): 1516 admissible; dropped per cell: loose_verse 0/384; tight_verse 4/384; tight_prose 3/384; loose_prose 13/384. Admissible candidates per topic × cell slot: min 3, mean 3.95. **Address gate (all 384 selected coded none by both): PASS.** Selected 384 stimuli ({'v1_reuse': 47, 'v2_gen': 145, 'v3_gen': 192}), seed 20261030, 40 random restarts of greedy coordinate descent. Selected items inside the 130–200 token band: 384/384; len_ok violations: 0.

## Decorrelation

Targets: |r(tightness, tokens)| < 0.1 and |r(tightness, log-ppl)| < 0.1 overall and within each register; per-domain mean token spread across the four cells < 10%. **r gate: PASS. Spread gate: PASS. Overall: PASS**

| scope | n | r(tightness, tokens) | r(tightness, log-ppl) |
|---|---|---|---|
| all | 384 | +0.000 | -0.000 |
| verse | 192 | -0.000 | +0.000 |
| prose | 192 | +0.000 | -0.000 |

### Per domain

| domain | r tok (all) | r lpp (all) | r tok (verse) | r lpp (verse) | r tok (prose) | r lpp (prose) | token spread |
|---|---|---|---|---|---|---|---|
| coding | -0.013 | -0.068 | +0.045 | -0.102 | -0.056 | -0.260 | 5.4% |
| philosophy_of_ai | -0.004 | +0.031 | +0.093 | -0.022 | -0.084 | +0.186 | 6.8% |
| therapy_like | +0.017 | +0.101 | -0.128 | -0.069 | +0.135 | +0.532 | 7.5% |
| writing | +0.000 | -0.043 | +0.004 | +0.171 | -0.003 | -0.477 | 4.4% |

### Cell means (all domains)

| cell | n | mean tokens (SD) | mean log-ppl (SD) |
|---|---|---|---|
| loose_verse | 96 | 163.5 (11.2) | 3.587 (0.321) |
| tight_verse | 96 | 163.5 (13.8) | 3.587 (0.349) |
| tight_prose | 96 | 156.1 (18.4) | 2.501 (0.267) |
| loose_prose | 96 | 156.1 (13.0) | 2.501 (0.272) |

### Per-domain cell means: tokens / log-ppl

| domain | loose_verse tok | tight_verse tok | tight_prose tok | loose_prose tok | loose_verse lpp | tight_verse lpp | tight_prose lpp | loose_prose lpp |
|---|---|---|---|---|---|---|---|---|
| coding | 165.2 | 166.3 | 157.8 | 159.6 | 3.690 | 3.617 | 2.333 | 2.449 |
| philosophy_of_ai | 162.3 | 164.5 | 154.1 | 156.6 | 3.656 | 3.643 | 2.755 | 2.676 |
| therapy_like | 163.2 | 159.8 | 156.3 | 151.8 | 3.521 | 3.483 | 2.616 | 2.344 |
| writing | 163.2 | 163.3 | 156.5 | 156.5 | 3.480 | 3.604 | 2.300 | 2.535 |

For comparison, over the full pool before selection: all: r_tok = +0.398, r_lpp = +0.044; verse: r_tok = +0.606, r_lpp = -0.336; prose: r_tok = +0.234, r_lpp = +0.541. Pool rows outside the 130–200 token band: 2.

### Search log

```
restart 0: obj=0.0109 all:tok+0.000/lpp-0.000 verse:tok+0.000/lpp-0.000 prose:tok+0.000/lpp+0.000 maxspread=0.073 sweeps=6
restart 7: obj=0.0075 all:tok+0.000/lpp-0.000 verse:tok-0.000/lpp+0.000 prose:tok+0.000/lpp-0.000 maxspread=0.075 sweeps=5
search done in 103s, objective=0.0075
```
