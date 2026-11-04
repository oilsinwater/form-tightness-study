# Selection report

Generated 2026-10-30T21:22:07-0700. Pool: 864 candidates (1 generator model(s): deepseek/deepseek-v4-pro; endpoint https://api.commandcode.ai/provider/v1). Selected 288 stimuli, seed 20261030, 40 random restarts of greedy coordinate descent.

## Decorrelation

Targets: |r| < 0.1 overall and per domain; per-domain mean token spread across levels < 10%. **Pass: False**

| scope | r(level, tokens) | r(level, log-ppl) | token spread |
|---|---|---|---|
| all (n=288) | +0.198 | -0.441 | — |
| coding | +0.355 | -0.570 | 11.7% |
| philosophy_of_ai | +0.118 | -0.429 | 10.0% |
| therapy_like | +0.000 | -0.292 | 6.2% |
| writing | +0.280 | -0.484 | 9.8% |

### Per-level means (all domains)

| level | n | mean tokens (SD) | mean log-ppl (SD) |
|---|---|---|---|
| T1 | 96 | 144.5 (15.1) | 3.404 (0.331) |
| T2 | 96 | 151.6 (21.0) | 2.054 (0.240) |
| T3 | 96 | 153.4 (17.6) | 2.730 (0.307) |

### Per-domain, per-level mean tokens / log-ppl

| domain | T1 tok | T2 tok | T3 tok | T1 lpp | T2 lpp | T3 lpp |
|---|---|---|---|---|---|---|
| coding | 144.9 | 144.9 | 161.8 | 3.394 | 1.876 | 2.437 |
| philosophy_of_ai | 141.5 | 155.7 | 146.2 | 3.610 | 2.249 | 2.981 |
| therapy_like | 148.5 | 157.8 | 148.5 | 3.200 | 2.045 | 2.836 |
| writing | 143.0 | 148.2 | 156.9 | 3.413 | 2.045 | 2.666 |

For comparison, over the full pool before selection: r(level, tokens) = +0.640, r(level, log-ppl) = -0.581. Candidates outside the 90–160 word band in pool: 0; selected: 0.

### Search log

```
restart 0: obj=2.0963 r_tok=+0.195 r_lpp=-0.446 sweeps=4
restart 1: obj=2.0792 r_tok=+0.194 r_lpp=-0.445 sweeps=4
restart 11: obj=2.0754 r_tok=+0.196 r_lpp=-0.442 sweeps=6
restart 12: obj=2.0726 r_tok=+0.198 r_lpp=-0.441 sweeps=4
search done in 43s, objective=2.0726
```

## Manipulation check (blind rubric rating)

Rater: `deepseek/deepseek-v4.1-flash` via `https://api.commandcode.ai/provider/v1`, temperature 0.0, seed 20261030, items in seeded random order, system prompt = `tightness-rubric.md` verbatim, user message = item text only, scores returned via response_format json_schema where accepted (parse modes: {'json_schema': 288}). Rated 288 / 288 items.

Pre-stated pass rule: mean total monotone T1 < T2 < T3 and Cohen's d > 1.0 between adjacent levels. **Monotone: True. d(T1,T2) = 3.85, d(T2,T3) = 2.04, d(T1,T3) = 5.66. Pass: True**

| level | n | mean total (SD) | item1 | item2 | item3 | item4 | item5 |
|---|---|---|---|---|---|---|---|
| T1 | 96 | 2.30 (1.82) | 0.65 | 0.58 | 0.16 | 0.52 | 0.40 |
| T2 | 96 | 8.08 (1.09) | 1.81 | 1.96 | 2.00 | 1.78 | 0.53 |
| T3 | 96 | 9.77 (0.42) | 2.00 | 2.00 | 2.00 | 1.89 | 1.89 |

| domain | T1 | T2 | T3 | d(T1,T2) | d(T2,T3) |
|---|---|---|---|---|---|
| coding | 3.04 | 8.50 | 9.67 | 4.22 | 1.90 |
| philosophy_of_ai | 1.38 | 8.29 | 9.83 | 5.84 | 2.04 |
| therapy_like | 1.00 | 7.04 | 9.58 | 6.74 | 3.46 |
| writing | 3.79 | 8.50 | 10.00 | 3.44 | 2.08 |
