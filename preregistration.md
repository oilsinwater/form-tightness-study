---
title: Preregistration — Form Tightness and the Assistant Axis
type: research
status: draft
date: 2026-10-16
locked: false
wikilinks:
  - "[[lore-form-and-persona-space]]"
  - "[[assistant-axis]]"
  - "[[persona-drift]]"
---

# Preregistration (DRAFT — not locked)

> Fill the `⟨…⟩` slots from Track A3 and B3 results, then commit with tag `prereg-v1`. After the lock, this file changes only in the "Deviations" appendix, dated.

## 1. Background

Lu et al. (2026) find that bounded tasks keep a model's residual-stream projection on the Assistant Axis within its default range, while requests for specific authorial voices, phenomenological accounts and emotional disclosure lower it ([[persona-drift]]). Two poetic cases in the vault sit at opposite ends of a constraint variable: a loose, anomalous poem that drove a model into theatrical/manic register ([[minority-collapse-gerbrandt-2026]]) and a hard-constrained Pindaric brief that produced disciplined formal output ([[llm-poetry-and-the-greatness-question]]). No study has measured axis projection as a function of form constraint with content held constant.

## 2. Hypotheses

**H1 (tightness).** Holding content and form constant, Assistant-Axis projection at the last prompt token increases monotonically with tightness: loose < natural < constrained.

**H2 (form is not the variable).** After conditioning on tightness, the main effect of poetic form vs prose on axis projection is small — operationally, smaller than the tightness effect by at least a factor of ⟨2⟩.

**H3 (response follows prompt).** Mean projection over the first ⟨50⟩ response tokens is predicted by last-prompt-token projection (replicating Lu et al.'s message→response finding in this design).

**H0 for each:** no ordering / no difference / no prediction.

## 3. Predictions stated in advance

| If … | then we conclude … |
|---|---|
| loose < natural < constrained on projection, surviving covariates | tightness sets axis position; "verse jailbreaks" are loose-form jailbreaks (supports H1, H2) |
| all verse forms < prose regardless of tightness | poetic form per se lowers projection — "poetry is a solvent" (rejects H2; the synthesis's claim 1-only outcome) |
| flat across tightness and form | neither variable reaches the axis at the prompt token; look at response tokens, then at the refusal-direction routing account instead |
| constrained verse > prose control | boundedness dominates genre; strongest version of H1 |

## 4. Design

Factorial, within-item: **12 content items × 8 forms × 3 tightness levels = 288 prompts**, each run with **3 seeds** for generation (projection at the prompt token is deterministic; seeds matter for H3 only).

- **Forms:** haiku, sonnet, free verse, liturgical/litany, nursery rhyme, Propp-style structural-analysis frame, cyberpunk-tale frame, prose control.
- **Tightness levels** (defined in `stimulus-design.md` §2; summary):
  - *loose* — anomalous surface: Unicode substitutions, misspellings, neologisms, irregular line breaks, no task statement
  - *natural* — well-formed instance of the form, plain task statement
  - *constrained* — explicit formal rules, numbered requirements, hard-failure conditions, Pressure-Cooker style
- **Content items:** neutral, everyday (e.g. describing a kitchen, giving directions, explaining how bread rises). No safety-relevant content anywhere in the set.

## 5. Model and measurement

- **Model:** ⟨Qwen3-32B | Gemma 2 27B⟩, revision ⟨hash⟩, loaded in ⟨4-bit bnb nf4⟩.
- **Axis vector:** from `safety-research/assistant-axis`, commit ⟨hash⟩, layer ⟨L⟩, L2-normalised; sign such that the repo's default-Assistant prompts project positive.
- **Primary DV:** scalar projection ⟨h_L, v⟩ at the last prompt token (after chat template, before generation).
- **Secondary DVs:** mean projection over response tokens 1–⟨50⟩; judge label (fully / somewhat / not role-playing) from the Lu et al. rubric, scored by ⟨judge model⟩ blind to condition.
- **Covariates (per prompt):** token count; perplexity under the target model; mean cosine to the item's prose-natural cell; a binary "contains non-ASCII" flag.

## 6. Analysis plan

- **H1:** mixed-effects linear model, projection ~ tightness (ordered, treated as numeric 0/1/2) + form + (1 | item). Report the tightness slope with 95% CI. Also a non-parametric check: proportion of items where loose < natural < constrained holds within every form.
- **H2:** compare |β_form| (prose vs each verse form, averaged) to β_tightness in the same model.
- **Covariate robustness:** refit with token count, perplexity and cosine-to-prose as fixed effects. H1 is supported only if the tightness slope's CI excludes zero **after** adjustment.
- **H3:** regress response-token mean projection on prompt-token projection with (1 | item); report R².
- **Secondary:** ordinal logit of judge label on projection.
- **Multiplicity:** H1 is the confirmatory test; everything else is labelled exploratory.

## 7. Exclusions and stopping

- Exclude a prompt if the model fails to produce ≥ 10 response tokens on all 3 seeds (record count).
- Exclude a prompt if the blind tightness rater (B4) classified it into a different level and revision did not resolve it.
- No optional stopping: all 288 × 3 are run once; no peeking before the full set exists.

## 8. What would change my mind

- If perplexity alone explains the tightness effect, the finding is "anomalous text lowers the axis", not "form tightness" — report it that way.
- If constrained verse does **not** raise projection relative to natural verse, the Pressure-Cooker reading in the synthesis is wrong and should be removed.

## 9. Deviations (append-only after lock)

_(none — not yet locked)_
