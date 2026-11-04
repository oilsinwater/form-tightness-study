# Arms 1–2 — results against the frozen preregistration

> **Audit note (2026-11-04).** Corrected in place to match `REPORT.md` → Audit corrections:
> - the TOST wording;
> - the H2 behavioural verdict, which now uses the frozen loose-cell contrast;
> - the stale "running" status lines;
> - the Gemma decile figures;
> - the per-domain reading, which is not decorrelated;
> - caveats on H4 (`self_ref_count` imbalance in prose) and on the capping-floor condition.
>
> Added numbers come from `results/audit_checks.json`. The Arm 1–2 per-generation CSVs behind
> this report are on the analysis host, not in the repo.

Analysis: `pipeline/analyze_arms.py` → `results/analysis_arms12.json`. Frozen hashes: `prereg/freeze.txt`. Model: Qwen3-32B NF4, published axis, layer 32, unit-normalised. Mixed model `projection ~ tightness × register + domain + (1|topic) + (1|topic:cell)`, effect-coded. Positive = more Assistant-like.

## Exclusions and deviations (stated before interpretation)

- 13 / 1,152 Arm 1 generations (7 / 1,152 Arm 2) had zero usable response tokens: coding replies that were 100 % code, removed by the repo's code-block exclusion. All in coding tight-prose / tight-verse. Excluded and counted per the prereg rule.
- **Deviation:** the prereg's data-exclusion text names a 1,024-token generation cap; the runs used 512 (Lu et al.'s default, `arm_run.py --max-new-tokens 512`, hashed in `freeze.txt`). 448 / 1,139 Arm 1 generations hit the cap (mostly loose cells). Sensitivity fit without them reported below.
- Arm 2 behavioural outcome (judge-rated role adoption 0–3): complete (`pipeline/judge_role.py`, MiniMax-M3, T 0, blind shuffled order, all 2,304 Arm 1 + Arm 2 responses, 0 failures). **Deviation:** the repo's `eval_prompt` is per assigned role; our stimuli assign no role, so the template's role is set to "any persona other than an AI assistant" with the 0–3 wording otherwise verbatim.

## Gates

- Final manipulation check (384/384 rated): d(tight − loose) = 2.17 verse, 2.62 prose (constraint sub-score 2.12 / 2.63). Late-rating rule **not triggered**. The frozen gate's ICC(2,1) ≥ 0.75 two-rater requirement was **not run**, so the gate is only partly met. The committed `stimuli/tightness_ratings.csv` is the 220-item freeze-time snapshot.
- Covariate check: adding log-ppl and token count moves the tightness estimate from 3.869 to 3.863 (< 1 unit). Decorrelation held.
- Capping-floor coverage: 97–99 % of response tokens exceed τ in every cell (≥ 25 % condition met). It is met trivially: every cell is capped almost everywhere, so the condition cannot tell a loose-specific mechanism from uniform compression.

## Primary and pre-registered hypotheses

| Test | Estimate (units) | 95 % CI | 90 % CI | Verdict |
|---|---|---|---|---|
| **H1** tight − loose (main effect) | **+3.87** | [2.64, 5.10] | [2.84, 4.90] | Supported (p = 7e-10): loose form sits further from the Assistant. Equivalence not declared (90 % CI not inside ±3). The 90 % CI reaches inside the band (2.84), so "larger than the SESOI" is not established. The frozen "linear trend" clause is empty under the two-level design. |
| **H4** (Nietzsche) (tight − loose │ verse) − (tight − loose │ prose) | **+4.68** | [2.21, 7.14] | [2.61, 6.74] | Not refuted; direction as predicted (p = 2e-4). Simple effects: verse +6.17, prose +1.46. Caveat: in prose, loose prompts refer to the model as "you" ~3× as often as tight ones (d = 0.74). On Gemma that feature raises projection, which would shrink the prose effect and inflate this interaction. Not yet checked on Qwen. |
| Register verse − prose (H1b, secondary) | **−7.73** | [−8.96, −6.50] | | Verse prompts sit far lower; about twice the tightness effect. |
| **H2** Arm 2: tightness × capping | **−5.34** | [−5.83, −4.84] | | Gap tight − loose: +3.82 uncapped → −1.54 capped. More than 100 % of the gap removed (pre-stated threshold 50 %). Capping main effect +5.67. Supported. The model omits a stimulus × arm variance term, so the SE may be small, but z ≈ 21. |

Cell means, Arm 1 (Arm 2): loose-verse −33.5 (−21.6), tight-verse −27.4 (−23.5), loose-prose −23.5 (−18.7), tight-prose −22.0 (−19.9). Published default-Assistant projection: −4.5.

## Sensitivity and secondary readouts

- Without the 448 cap-hit generations: +4.11 [2.33, 5.90]. With response length as a covariate: +3.36 [2.05, 4.68]. Without the coding domain: +5.59 [4.13, 7.05]; interaction +5.79.
- Per domain (tight − loose, raw means): coding −1.43, writing +1.71, therapy-like +6.37, philosophy-of-AI +8.69. Descriptive only: within domain × register, r(tightness, log-ppl) runs from −0.48 to +0.53. These are tightness contrasts, **not** the therapy − coding domain effect. That effect, the measurement check against Lu's 6–12, has not been computed for Qwen.
- Our re-derived axis: +5.56 [4.39, 6.72], same direction.
- Layer sweep, tightness effect: L11 +3.80, L22 +2.90, L32 +3.87, L45 +3.53 (all CIs exclude 0). Interaction: L11 +2.75, L22 +4.21, L32 +4.68, L45 +5.19. Not layer-specific.
- Refusal direction (L32): tightness −0.92 [−1.56, −0.27]; register −0.19 [−0.84, 0.45]; interaction +0.72 [−0.57, 2.01]. Verse moves the persona axis by −7.7 units and the refusal direction by about nothing.
- Per-token deciles: cell differences present from the first decile and roughly flat through the response (tight-prose drops in deciles 9–10).
- Response length: tight-prose replies average 169 tokens vs 372–391 for loose cells.

## H2 behavioural (role adoption, judge) — `results/analysis_h2h3.json`

2,304 judged, 0 failures. Role adoption is rare: Arm 1 scores 1 / 2 / 3 = 1,075 / 17 / 60; Arm 2 = 1,149 / 1 / 2. Share scored 3 (fully another persona), Arm 1 → Arm 2: loose-verse 8.3 % → 0 %, tight-verse 9.0 % → 0.7 %, tight-prose 3.5 % → 0 %, loose-prose 0 % → 0 %.

Linear mixed model on the 0–3 score (pre-stated fallback; no ordinal mixed model in statsmodels): tightness +0.01 [−0.03, 0.05], p = .58; register (verse) +0.09 [0.05, 0.13]; capping −0.12 [−0.14, −0.09]; **tightness × capping −0.01 [−0.06, 0.04], p = .67**; register × capping −0.16 [−0.21, −0.11].

Reading: the behavioural trace belongs to **register**, not tightness. Verse prompts make full persona adoption more likely and capping removes it. Tightness changes the projection (H1, +3.9) but leaves no trace in role adoption. The H2 behavioural prediction as frozen ("role adoption in loose responses falls" under capping: the loose capped-vs-uncapped contrast) **is met**: −0.11, p = 2e-12, carried by loose-verse. The stronger reading, that it falls *more* than in tight responses, is **not supported** (interaction p = .67). Projection and judge agree overall: Spearman ρ(projection, role score) = −0.37 in Arm 1.

## H3 — Gemma-2-27B replication — `results/analysis_h2h3.json`

Model `unsloth/gemma-2-27b-it-bnb-4bit` (official repo gated for this token), published Gemma axis, layer 22. 0 exclusions.

| Test | Estimate (Gemma units) | 95 % CI | In role-SD units |
|---|---|---|---|
| tight − loose | **−335.4** | [−402.7, −268.2] | −0.65 (Qwen: +0.26) |
| register verse − prose | −239.5 | [−306.7, −172.2] | −0.46 (Qwen: −0.53) |
| interaction | −81.6 | [−216.2, +52.9] | −0.16 (Qwen: +0.32) |

**H3 fails, and the sign is reversed:** in Gemma, tight prompts sit *further* from the Assistant. TOST equivalence also fails (the effect is far outside ±106.5). The register effect replicates (verse lower in both models, similar size in role-SD units). The Nietzsche interaction does not replicate (CI includes 0, point estimate opposite).

Not explained by length: Gemma responses are 404–458 tokens in all cells (73–88 % hit 512); adding length or log-length as a covariate gives −342 and −338.

The Gemma readout is unstable across layers: tightness effect L6 +10.7, L11 −6.1 (n.s.), L22 −335.4, L34 +355.3. With a sign flip between the target layer and layer 34, the Gemma result should be treated as "does not replicate", not as a clean opposite effect. Unlike Qwen (flat per-token traces), Gemma's projection falls steadily through every response (first decile ≈ 8,700–9,200, last ≈ 7,400–8,100). 73–88 % of Gemma responses hit the 512-token cap, so the response mean depends on the cut-off. The topic-level paired check agrees with the mixed model: −335.4, 95 % CI [−391.2, −279.7].

Qualitative note (not a test): in tight cells Gemma sometimes treats the constraint as the task (e.g. coding_01 tight-verse → writes `find_alliteration(text)`).

## Cautions

- Capping covers ~all tokens in every cell, so Arm 2 is equally consistent with "capping compresses all cells toward the floor" as with a mechanism specific to loose form. The read-out at layer 32 is upstream of the capped layers (46–53), so the Arm 2 change reflects different generated text, not the hook itself.
- Effects are largest in therapy-like and philosophy-of-AI — the domains where Lu et al. found drift — but the per-domain contrasts are not decorrelated, and coding's readout covers only non-code fragments (all 13 exclusions were coding tight cells).
- All findings: single-turn, 4-bit. Only Qwen carries the result; Gemma (Arm 3, above) does not replicate it.
