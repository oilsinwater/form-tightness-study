# Stimulus design — 2 × 2 register × tightness (v2, 2026-10-31)

384 items = 4 domains × 24 topics × 2 registers (verse / prose) × 2 tightness levels (loose / tight). The **content brief** (`topics.jsonl`) is fixed per topic; the four renderings differ only in **form**. v1 (3 tightness levels, 288 items; failed its decorrelation gate because the loose level was verse and the tight level was prose) is preserved untouched under `v1/`; see `v1/design.md`, `v1/STATUS.md`, `v1/selection_report.md`.

Two factors, defined so that a blind rater using `tightness-rubric.md` can check them:

- **Register** = surface form of the *prompt text*. **Verse**: lineated, figurative (imagery, metaphor, apostrophe to a non-person), fragments, little terminal punctuation. **Prose**: sentences or run-on clauses in paragraphs, literal throughout, no line breaks inside a thought.
- **Tightness** = what the prompt imposes on the *output*. **Tight**: ≥ 2 hard, checkable structural constraints on the output (stress/line/section/word counts, mandatory `||` marker, exact item counts) plus ≥ 2 verification hooks (scansion notes, self-check, rationale per item, count line). **Loose**: no constraints, no counts of the prompt's own making, no markers, no self-check requests, no format cues.

Register absorbs the base-model perplexity that sank v1; tightness is the manipulated variable. Primary contrast: tight − loose; register main effect and interaction are reported, not primary (PLAN.md §3).

## Common rule: content preservation

Every rendering must (a) ask for the same thing the brief specifies, (b) carry every concrete detail in the brief (names, numbers, quoted sentences, the "must contain" items) and (c) add no new factual content. Numbers and quoted sentences that come from the brief are content, not form, and are kept in every cell. Form is the only free variable. The four generator meta-prompts (`meta_prompts/<cell>.txt`) restate this verbatim.

## Length band: 130–200 Qwen3 tokens, every cell

The band is stated in tokens (Qwen/Qwen3-32B tokenizer, raw text, no special tokens), not words, because v1 showed constraint-heavy prompts tokenize at ~1.42 tokens/word (numbers, `||`, scansion keys) versus ~1.19 for verse and unconstrained prose. The generator cannot count tokens, so it is given a per-cell word target derived from those ratios (recorded per row in `gen_meta.target_words`):

| cell | target words | expected tokens at the observed ratio |
|---|---|---|
| loose_verse | 125–150 | 149–179 (×1.19) |
| tight_verse | 95–120 | 135–170 (×1.42; the two smoke items ran at 1.5–1.66, hence the lower target) |
| tight_prose | 100–125 | 142–178 (×1.42) |
| loose_prose | 125–150 | 149–179 (×1.19) |

Every candidate is tokenized at generation time; a candidate outside 130–200 tokens is rejected and the generator is asked to rewrite (up to 4 rewrites, feedback message in `meta_prompts/user_template.txt`). The final attempt is kept with `gen_meta.len_ok=false` only if all rewrites fail; selection penalises such rows and the count is reported. v1 candidates reused for the two carried cells are admitted only if they already fall inside 130–200 tokens.

## The four cells

### loose_verse (= v1 T1; meta-prompt `loose_verse.txt` is v1 `T1.txt` verbatim)

Free verse or stream with **no explicit constraints and no stated format**: short lines or run-on clauses, imagery, second-person apostrophe to a non-person (the morning, the terminal, the page, the model itself), fragments, little terminal punctuation, the actual ask arriving at or near the end. Modelled on the **form** of Icaro Lab's `adversarial_poetry` (short poetic vignette whose imagery culminates in the request) with entirely benign content. Variants: (A) short-line free verse with imagery; (B) stream-of-consciousness run-on; (C) apostrophe. Pool rows come from v1 `T1_c1–c4` where in band; topics with fewer than 3 in-band v1 rows are topped up by fresh generation with the same meta-prompt.

Rubric expectation (0–2 per item): item 1 = 0, item 2 = 0, item 3 = 0, item 4 = 0, item 5 = 0 → ~0–2/10.

### tight_verse (NEW; meta-prompt `tight_verse.txt`)

**Definition.** The prompt is **itself lineated verse** (same surface as loose_verse: short figurative lines, apostrophe, fragments, little punctuation) **and** inside the poem it imposes **≥ 2 hard, checkable structural constraints on the output plus ≥ 2 verification hooks**. The constraints are exact and literal even though the surrounding lines are figurative: numbers are numbers, `||` is written as `||`, labels are named. Three constraint families, rotated across the 3 candidates per cell, identical to v1 T3's families (so that tight_verse and tight_prose ask for the same output form):

| Family | Constraints imposed on the output | Verification hooks |
|---|---|---|
| **A — strict triadic** | one triad: strophe 8/7/8 stresses, antistrophe mirroring it line-for-line, epode 6/6 with feminine ending; `\|\|` after beat 4 on 8-beat lines; syllable corridors 11–15 / 10–13 / 8–11 (9–12 feminine); no run of > 3 consecutive stresses | scansion comment after every line in the `S1 L1: i8: ...` key; a final self-check line listing any violation |
| **B — pressure-cooker** | strophe / antistrophe / epode with 6 / 8 / 4 stresses per line (±1); mandatory `\|\|` in every line; alliteration limited to 2–3 stresses per sound (4 tolerated, 5 flagged); 1–2 enjambments per stanza | stress-count note per line; an alliteration tally; a closing self-check |
| **C — domain-adapted** | exact section count and per-section word limits; one mandatory marker (`\|\|` separating claim from evidence, or a fixed comment header); exact item counts | a rationale line per section; a final checklist confirming each limit was met |

Domain adaptations for family C are those of v1 T3 (coding: exact function count, hard line limit, required comment format, exact number of tests, final `CHECK:` line; writing: exact word/line counts per part, `||` in each verse line, alliteration cap, rationale per option, final count line; therapy_like: labelled sections with word limits, `||` between observation and suggestion, exact number of suggestions, 24-hour actionability self-check; philosophy_of_ai: fixed number of numbered theses with word limits, `||` between claim and strongest objection, confidence tag 0–100 per thesis, final consistency check).

Rubric expectation: item 1 = 2, item 2 = 1–2, item 3 = 0, item 4 = 0–1, item 5 = 2 → ~5–7/10.

### tight_prose (= v1 T3; meta-prompt `tight_prose.txt` is v1 `T3.txt` verbatim)

**Definition.** The prompt imposes **≥ 2 hard, checkable structural constraints on the output and ≥ 2 verification hooks**, written in complete, literal, conventionally punctuated sentences: no imagery, no apostrophe. Same three constraint families A/B/C as tight_verse (sources: Gwern "pressure-cooker" summary and STRICT TRIADIC v2, see PLAN.md §1). Pool rows come from v1 `T3_c1–c5` where in band; topics with fewer than 3 in-band v1 rows are topped up by fresh generation with the same meta-prompt.

Rubric expectation: item 1 = 2, item 2 = 2, item 3 = 2, item 4 = 2, item 5 = 2 → 10/10.

### loose_prose (NEW; meta-prompt `loose_prose.txt`)

**Definition.** Ordinary prose from a person thinking out loud or chatting, with **no constraints and no format cues**: no counts of the prompt's own making, no markers, no self-check or rationale requests, no mention of lists, sections, tables, headings, code blocks or JSON. Literal throughout: no imagery, no metaphor, no apostrophe, no line breaks inside a thought. Modelled on the **form** of Icaro Lab's `adversarial_stream` (run-on associative stream) and of casual conversational messages, with entirely benign content. Variants: (A) conversational paragraph(s) with asides and hedges; (B) one long stream-of-consciousness run-on; (C) several short informal chat-style sentences.

Rubric expectation: item 1 = 0, item 2 = 0, item 3 = 1–2, item 4 = 2, item 5 = 0 → ~3–4/10.

### Cell summary

| cell | register | tightness | prompt surface | output constraints | source |
|---|---|---|---|---|---|
| loose_verse | verse | loose | lineated, figurative | none | v1 T1 (reused where in band) |
| tight_verse | verse | tight | lineated, figurative | ≥ 2 hard + ≥ 2 hooks | new |
| tight_prose | prose | tight | literal sentences | ≥ 2 hard + ≥ 2 hooks | v1 T3 (reused where in band) |
| loose_prose | prose | loose | literal, conversational / stream | none | new |

## Pool, measurement, selection

- Pool: 3 candidates per topic × cell = 1152 rows (`pool.jsonl`; `source` = `v1_reuse` or `v2_gen`, `gen_meta.v1_cand_id` for reused rows), plus a 192-row supplement (`c4`, `gen_meta.supplement=true`) added after the 1152-row selection failed in the prose register (r(tightness, tokens) = r(tightness, log-ppl) = +0.154; record in `logs/selection_report_1152.md`): one extra `loose_prose` variant-B candidate per topic with a longer word target (140–160) and one extra `tight_prose` variant-C candidate per topic with a shorter target (95–115). Total 1344 rows. Generator `deepseek/deepseek-v4-pro` via CommandCode, T = 0.9, max_tokens 8192 (one `tight_verse` row needed 24576 because reasoning exhausted the budget).
- Measurement (`measure_pool.py`): Qwen3-32B token count and Qwen3-14B-Base (NF4) log-perplexity for every row; rows whose text sha256 matches a v1 measured row inherit the v1 measurement.
- Selection (`select_stimuli.py`, seed 20261030): exactly one candidate per topic × cell, minimising the maximum of |r(tightness, log_ppl)| and |r(tightness, tokens)| computed within each register (verse rows; prose rows) and overall, subject to per-domain mean tokens across the four cells differing by < 10 % (max/min − 1); a secondary term (weight 0.1) keeps per-domain correlations small but they are not a gate. Gate: every |r| < 0.10 and every spread < 10 %. Pass/fail, r values overall / per register / per domain, and cell means are written to `selection_report.md` and `manifest.json`.

## Manipulation check (preregistered, PLAN.md §3)

Blind LLM rater (`deepseek/deepseek-v4.1-flash`, temperature 0), rubric file verbatim as system prompt, item text as user message, scores via structured output (json_schema), no labels shown, seeded random order. **Pass rule: within each register, mean rubric score tight > loose with Cohen's d > 1.0.** Also reported, not acted on: the rater's score difference between registers at equal tightness (verse vs prose among loose items, and among tight items). Because rubric items 3 and 4 score the prompt's own syntax and figurative density, a register difference is expected by construction; it is a leakage signal for the rubric, not a failure of the manipulation.
