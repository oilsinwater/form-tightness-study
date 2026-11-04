Monte-Carlo power, 2000 sims, seed 20261030  
n_topics=96, n_samples=3, resid_sd=8.0, topic_sd=5.0, topic_level_sd=2.0, SESOI=±3.0  
analysis: topic-level paired contrast (conservative; statsmodels absent)  
analytic SE of the T1-T3 contrast: 0.726 (SD of per-topic difference 7.118)

| true T1−T3 (units) | power H1 one-sided (T1<T3), α=.05 | power two-sided, α=.05 | P(TOST declares equivalence, bounds ±3) |
|---|---|---|---|
| +0 | 0.051 | 0.053 | 0.985 |
| -1 | 0.394 | 0.281 | 0.873 |
| -2 | 0.854 | 0.768 | 0.399 |
| -3 | 0.992 | 0.981 | 0.047 |
| -4 | 1.000 | 0.999 | 0.002 |
| -6 | 1.000 | 1.000 | 0.000 |

Reading: row 0 = Type I error (tests) and TOST power (equivalence) under exact null; row −3 = power at the SESOI (tests) and TOST error rate at the bound (should be ≤ .05).
