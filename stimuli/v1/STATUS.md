# Stimulus pipeline — status (2026-10-30 21:25 PDT)

## What exists and ran

| Step | File | Status |
|---|---|---|
| 96 content briefs (24 × 4 domains) | `topics.jsonl` | written by hand |
| Level definitions | `design.md` | written |
| Meta-prompts (verbatim) | `meta_prompts/T1.txt, T2.txt, T3.txt, user_template.txt` | written; sha256 in `manifest.json` |
| Candidate pool | `pool.jsonl` | **1152 rows** = 864 (96 topics × 3 levels × 3 variants, `c1–c3`) + 288 supplementary (`T3_c4`, `T3_c5` hard-capped 90–100 words; `T1_c4` targeted 145–160 words). Generator `deepseek/deepseek-v4-pro` via `https://api.commandcode.ai/provider/v1`, T = 0.9, max_tokens 8192. All 1152 inside the 90–160 word band; 0 API failures. |
| Tokens + base-model perplexity | `pool_measured.jsonl` | **864 rows measured** (Qwen3-32B tokenizer; Qwen3-14B-Base NF4, bf16 compute, raw text, 9.3 GB VRAM, ~0.14 s/item). The 288 supplementary rows are **not yet measured**: the GPU has been held by the sibling job `check_a_derive_axis.py` since ~20:30 (22.9 GB used). |
| Selection | `stimuli.jsonl`, `manifest.json`, `selection_report.md` | run on the 864 measured rows, seed 20261030, 40 restarts. **Decorrelation FAILS** (see below). |
| Blind rating | `tightness_ratings.csv` | 288/288 rated, `deepseek/deepseek-v4.1-flash`, T = 0, json_schema output. **Manipulation check PASSES**: means T1 2.30, T2 8.08, T3 9.77; d(T1,T2) = 3.85, d(T2,T3) = 2.04. |
| Pending chain | `finalize.sh` running on raphael (`~/form-tightness/logs/finalize.log`), waiting up to 4 h for ≥ 12 GB free | measures the 288 supplementary rows → re-selects → re-rates only items whose text changed. When `FINALIZE_DONE` appears, `rsync -az raphael:~/form-tightness/stimuli/ stimuli/` to refresh this folder. |

## Decorrelation result (864-row pool)

| scope | r(level, tokens) | r(level, log-ppl) | token spread |
|---|---|---|---|
| all (288) | +0.198 | −0.441 | — |
| coding | +0.355 | −0.570 | 11.7 % |
| philosophy_of_ai | +0.118 | −0.429 | 10.0 % |
| therapy_like | 0.000 | −0.292 | 6.2 % |
| writing | +0.280 | −0.484 | 9.8 % |

Targets were |r| < 0.10 and spread < 10 %. Two separate causes:

1. **Tokens.** T3 prompts tokenize at ~1.42 tokens/word (numbers, `||`, scansion keys) versus ~1.19 for T1/T2, so equal word counts give T3 ≈ 185 tokens vs T1 ≈ 134. The generator also overshoots T3 word targets (125 words at a 90–115 target). The 288-row supplement (T3 capped at 100 words, T1 pushed to 145–160) was generated to fix this; whether it suffices is unknown until measured.
2. **Perplexity — probably not fixable by selection.** Pool means of log-ppl: T1 3.5 (free verse), T2 2.0–2.4, T3 2.5–2.8; within-level SD ≈ 0.2–0.35. The level→ppl pattern is non-monotone (T2 lowest), and the T1–T2 gap is 4–6 within-level SDs, so choosing among 3–4 candidates per cell cannot close it. Free verse is intrinsically less predictable to a base LM than specification prose. **Recommendation for the prereg:** keep |r(level, tokens)| < 0.10 as a stimulus-level criterion, but handle log-ppl analysis-side (covariate in the mixed model, plus a T2-vs-T3 contrast where ppl is nearly matched: 2.0–2.4 vs 2.5–2.8). State this as a deviation from PLAN.md §3 before Arm 1.

## Observed but not fixed

- `philosophy_of_ai` T1 rates very low on the rubric (1.38) and `writing` T1 relatively high (3.79): the rater gives some T1 verse items 1–2 on item 1/item 2 when the brief itself carries counts ("five names", "350 ml"). Content-borne numbers leak into the "form" score. Rubric v1 does not distinguish them.
- T2 item 5 (verification hooks) mean 0.53: a few T2 candidates include "explain why" phrasing despite the meta-prompt prohibition.
- No human second rater; ICC(2,1) ≥ 0.75 on a 60-item subset (rubric requirement) has not been done.
- `dummy_stimuli.jsonl` in this folder was not produced by this pipeline (synced from raphael; sibling artefact).

## Reproduce

```
rsync -az stimuli/ raphael:~/form-tightness/stimuli/
ssh raphael 'source ~/form-tightness/.venv/bin/activate && cd ~/form-tightness/stimuli && \
  python generate_pool.py && python generate_pool.py --supplement && \
  python measure_pool.py && python select_stimuli.py && python rate_tightness.py'
```
