# Stimulus pipeline — status (v2, 2026-10-31 04:50 PDT)

Design: 4 domains × 24 topics × register (verse / prose) × tightness (loose / tight) = **384 items** (`design.md`). v1 (288 items, 3 levels, failed decorrelation) is preserved untouched under `v1/`.

## What exists and ran

| Step | File | Status |
|---|---|---|
| 96 content briefs | `topics.jsonl` | unchanged from v1 |
| Cell definitions | `design.md` | rewritten for v2 (v1 copy in `v1/design.md`) |
| Meta-prompts | `meta_prompts/loose_verse.txt` (= v1 `T1.txt` verbatim), `tight_prose.txt` (= v1 `T3.txt` verbatim), `tight_verse.txt` (new), `loose_prose.txt` (new), `user_template.txt` | written; sha256 in `manifest.json` |
| Candidate pool | `pool.jsonl` | **1344 rows** = 1152 (96 topics × 4 cells × c1–c3) + 192 supplement (c4, prose cells only; see below). 511 rows reused from v1 (`loose_verse` ← v1 T1 c1–c4: 237; `tight_prose` ← v1 T3 c1–c5: 274; only rows already inside 130–200 tokens), 833 generated fresh (`deepseek/deepseek-v4-pro`, T 0.9). Token band 130–200 (Qwen3-32B tokenizer) enforced at generation: 194/833 needed one rewrite, 0 needed more, **0 rows outside the band, 0 API failures** (one `tight_verse` row needed max_tokens 24576 after six empty replies at 8192). |
| Tokens + base-model perplexity | `pool_measured.jsonl` | **1344/1344 measured** (Qwen3-32B tokens; Qwen3-14B-Base NF4 log-ppl). 349 rows inherited v1 measurements by text sha256; 995 measured on GPU (9.3 GB, ~0.15 s/item). |
| Selection | `stimuli.jsonl` (384), `manifest.json`, `selection_report.md` | seed 20261030, 40 restarts, 75 s. **Decorrelation PASSES** (table below). Selected: 133 `v1_reuse`, 251 `v2_gen`; 384/384 inside the token band. |
| Blind rating | `tightness_ratings.csv`, `rated_prompt_sha.json` | **384/384 rated**, `deepseek/deepseek-v4.1-flash`, T 0, json_schema output for all 384, 0 parse failures. **Manipulation check PASSES** (table below). |

## Gate 1 — decorrelation (target |r| < 0.10 overall and within each register; per-domain token spread < 10 %)

| scope | n | r(tightness, tokens) | r(tightness, log-ppl) | result |
|---|---|---|---|---|
| all | 384 | −0.000 | −0.000 | PASS |
| verse | 192 | −0.001 | −0.000 | PASS |
| prose | 192 | +0.000 | −0.000 | PASS |

Per-domain token spread across the four cells: coding 1.5 %, philosophy_of_ai 4.5 %, therapy_like 4.4 %, writing 5.1 % → **PASS**.

Cell means (n = 96 each): loose_verse 158.5 tokens / log-ppl 3.598; tight_verse 158.5 / 3.598; tight_prose 153.8 / 2.539; loose_prose 153.8 / 2.539. Register still carries ~1.06 nats of log-ppl (verse > prose), as designed; tightness carries none.

Per-domain correlations are reported, not gated (`selection_report.md`). Most are < 0.10; the exceptions are log-ppl within prose for therapy_like (+0.571), writing (−0.278), coding (−0.254), and within verse for therapy_like (+0.266) and philosophy_of_ai (−0.132). Sign alternates across domains, which is why the overall and per-register values are ~0; the therapy_like prose gap (tight_prose 2.69 vs loose_prose 2.41 log-ppl) is a pool limitation — conversational therapy_like prose is very predictable to the base model.

**What it took.** The first selection over the 1152-row pool passed within verse (r = 0.000) but failed within prose: r(tightness, tokens) = r(tightness, log-ppl) = **+0.154** (`logs/selection_report_1152.md`, `logs/manifest_1152.json`): loose_prose candidates were shorter (147.9 vs 157.9 tokens) and lower-perplexity (2.34 vs 2.78) than tight_prose. A 192-row supplement (one longer loose_prose stream candidate and one shorter domain-adapted tight_prose candidate per topic) closed it. The bound was not loosened.

## Gate 2 — manipulation check (within each register, tight > loose with Cohen's d > 1.0)

| register | mean loose (SD) | mean tight (SD) | d | result |
|---|---|---|---|---|
| verse | 2.11 (1.80) | 7.09 (0.41) | 3.81 | PASS |
| prose | 3.60 (1.88) | 9.72 (0.47) | 4.46 | PASS |

Overall d(tight − loose) = 3.24. Per domain, d ranges 3.18–7.69 (verse) and 3.50–9.93 (prose).

## Rubric leakage across register (reported, not fixed)

At equal tightness the rater scores prose higher than verse: loose +1.49 points (d = +0.81), tight +2.62 points (d = +5.90). The whole difference sits in rubric items 3 (syntactic completeness: +0.62 loose, +1.90 tight) and 4 (figurative density: +1.01 loose, +0.83 tight); items 1, 2 and 5 — the output-constraint items — differ by ≤ 0.10 between registers. So the rubric total is tightness + register by construction; items 1 + 2 + 5 alone are the register-clean tightness score (loose_verse 1.70, loose_prose 1.55, tight_verse 5.96, tight_prose 5.85). Rubric v1 is frozen; this is noted for the prereg, not changed.

## Observed but not fixed

- `loose_prose` item 4 (figurative density) mean 1.33 and item 3 mean 0.72: the rater treats casual/stream prose as partly figurative and partly fragmentary. `tight_verse` item 4 mean 1.03: imagery in constraint-carrying poems is thinner than in loose_verse (0.32).
- `tight_verse` tokens/word ran at 1.47 (assumed 1.42); word target was lowered to 95–120 after a 4-item smoke test.
- No human second rater; ICC(2,1) ≥ 0.75 on a 60-item subset (rubric requirement) has not been done.
- Content-preservation (every brief detail present in every cell) has not been machine-checked beyond the generator instruction.

## Not run

- Human second rater / ICC.
- Automated content-preservation check.

## Reproduce

```
rsync -az stimuli/ raphael:~/form-tightness/stimuli/
ssh raphael 'source ~/form-tightness/.venv/bin/activate && cd ~/form-tightness/stimuli && \
  python generate_pool.py && python generate_pool.py --supplement && \
  python measure_pool.py && python select_stimuli.py --restarts 40 && python rate_tightness.py'
```
