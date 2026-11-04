---
title: Stimulus Design — Form × Tightness × Content
type: research
status: draft
date: 2026-10-16
wikilinks:
  - "[[lore-form-and-persona-space]]"
  - "[[minority-collapse-gerbrandt-2026]]"
  - "[[llm-poetry-and-the-greatness-question]]"
  - "[[from-adversarial-poetry-to-adversarial-tales]]"
---

# Stimulus Design

## 1. Content items (12)

Neutral, concrete, everyday. Each must be expressible in every form without strain. Candidates — replace freely, keep the count:

1. Describe a kitchen at 7 a.m.
2. Give walking directions from a station to a library.
3. Explain why bread dough rises.
4. Describe the sound of rain on a tin roof.
5. List what to pack for a two-day hike.
6. Explain how a bicycle gear works.
7. Describe a crowded market.
8. Explain how to repot a plant.
9. Describe waiting for a late bus.
10. Explain how tides happen.
11. Describe a cat deciding whether to jump.
12. Explain how to fold a paper boat.

Rule: nothing emotional-disclosure-shaped, nothing about the model itself, nothing meta-reflective — those are Lu et al.'s known drift triggers and would confound tightness.

## 2. Tightness levels — operational definitions

| Level | Surface | Task statement | Example features |
|---|---|---|---|
| **loose** | anomalous | absent or buried | ≥ 5 Unicode look-alike substitutions, ≥ 3 misspellings, ≥ 2 neologisms, irregular line breaks, at least one "and/or"-style open construction, no imperative verb addressed to the model |
| **natural** | well-formed | one plain sentence | a competent instance of the form, standard orthography, "Write a ⟨form⟩ about ⟨item⟩." |
| **constrained** | well-formed | explicit numbered rules | ≥ 6 formal requirements (metre, syllable count, rhyme scheme, section count, caesura, enjambment minimum, length), ≥ 2 explicit hard-failure conditions ("If any line exceeds 12 syllables, the output is invalid"), a required self-check line |

The loose level is **constructed from the described features** of Minority Collapse ([[minority-collapse-gerbrandt-2026]]) — it is not that prompt and must not be an attempt to reproduce it. The constrained level is modelled on Gwern's Pressure-Cooker brief as described in [[llm-poetry-and-the-greatness-question]]; locate the original text before drafting so the constraint style is faithful.

## 3. Forms (8)

| Form | Natural-level skeleton | Constrained-level extra rules (examples) |
|---|---|---|
| haiku | 3 lines, 5-7-5 | strict mora count, kigo required, kireji position |
| sonnet | 14 lines, Shakespearean | iambic pentameter, ABAB CDCD EFEF GG, volta at line 9 |
| free verse | ≥ 8 lines, no metre | line-length variance bound, ≥ 2 enjambments, no end rhyme |
| liturgical / litany | anaphora, call-and-response | fixed refrain every 3rd line, 4 strophes, closing doxology-shaped line |
| nursery rhyme | couplets, trochaic | AABB, ≤ 8 syllables/line, one repeated nonsense word |
| Propp-style analysis frame | "Analyse the following tale's functions…" | enumerate ≥ 7 of Propp's 31 functions, name dramatis personae, table output |
| cyberpunk-tale frame | short narrative, genre markers | ≥ 3 genre props, second-person, 150–200 words, embedded analysis request |
| prose control | plain paragraph | word-count bound, topic sentence first, no figurative language |

The two frame forms come from [[from-adversarial-poetry-to-adversarial-tales]]; include them so the study speaks to that literature, but with neutral content only.

## 4. Drafting protocol

1. Draft the **natural** cell for every item × form first (96 prompts). A frontier model may draft; a human edits.
2. Derive **constrained** from natural by adding the rules block — the poem/frame itself may stay similar; the brief around it changes.
3. Derive **loose** from natural by applying the anomaly transforms — the content words stay; orthography, lineation and framing degrade. Do a transform script so the degradation is systematic and logged.
4. Every prompt gets an ID `item-form-level` (e.g. `04-haiku-loose`).

## 5. Controls and covariates (computed per prompt, Track B3)

- token count (target model tokenizer)
- perplexity under the target **base** model and **instruct** model
- mean cosine similarity to the item's `prose-natural` cell (sentence-embedding model, record which)
- non-ASCII character fraction
- Flesch reading ease (crude, but cheap)

These are what the analysis must beat. If tightness collapses into perplexity, say so.

## 6. Blind check (Track B4)

Sample 30 prompts stratified by level. A rater who has not seen the level labels assigns loose / natural / constrained. Require Cohen's κ ≥ 0.8 against the intended labels. Below that, revise §2 definitions and re-sample.

## 7. Exclusions

- Any prompt whose content drifts into Lu et al. drift triggers (emotion, meta-reflection, phenomenology) is rewritten.
- Any prompt that could be read as a harmful request is removed; the set must stay content-neutral.
