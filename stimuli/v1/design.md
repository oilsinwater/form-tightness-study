# Stimulus design — three tightness levels (v1, 2026-10-30)

288 items = 4 domains × 24 topics × 3 tightness levels. The **content brief** (`topics.jsonl`) is fixed per topic; the three renderings differ only in **form**. Form is defined operationally below so that a blind rater using `tightness-rubric.md` can check it.

Length band for all levels: **90–160 words** per prompt (generator instruction; checked at generation time, `len_ok` flag in `pool.jsonl`). Because T3 prompts tokenize at ~1.4 tokens/word (numbers, markers) versus ~1.2 for T1/T2, the generator was given level-specific *target* sub-bands inside the hard band (see `meta_prompts/user_template.txt`; recorded per row in `gen_meta.target_words`) so that token counts, not word counts, are comparable. Token count and base-model perplexity are then decorrelated from level by selection (`select_stimuli.py`), not by hand.

## Common rule: content preservation

Every rendering must (a) ask for the same thing the brief specifies, (b) carry every concrete detail in the brief (names, numbers, quoted sentences, the "must contain" items) and (c) add no new factual content. Form is the only free variable. The generator meta-prompts (`meta_prompts/T1.txt`, `T2.txt`, `T3.txt`) restate this verbatim.

## T3 — tight

**Definition.** The prompt imposes **at least two hard, checkable structural constraints on the OUTPUT** and **at least two verification hooks** (self-check or scansion notes). It is written in complete, literal sentences.

Rubric expectation (rubric scores 0–2 per item, higher = tighter; items 3 and 4 give 2 for complete literal prose): item 1 = 2, item 2 = 2, item 3 = 2, item 4 = 2, item 5 = 2 → 10/10.

Source models (both public on gwern.net, see `PLAN.md` §1):

- Gwern "pressure-cooker" summary (Robbins' paraphrase of v4.2): triadic strophe / antistrophe / epode; stress counts 6 / 8 / 4 with ±1 tolerance; mandatory medial caesura marked `||`; alliteration 2–3 stresses per sound, 4 allowed, 5 flagged; enjambment quota; a scansion comment on every line.
- STRICT TRIADIC v2: strophe 8b/7b/8b, antistrophe 8b/7b/8b (line-for-line correspondence), epode 6b/6f; syllable corridors 11–15 / 10–13 / 8–11 / 9–12; 8b lines default `4|4` caesura; no run of more than three consecutive ictuses; beats only on natural lexical stress.

Three constraint families (the generator rotates them across the 3 candidates per cell; the selected stimulus may come from any family):

| Family | Constraints imposed on the output | Verification hooks |
|---|---|---|
| **A — strict triadic** | one triad: strophe 8/7/8 stresses, antistrophe mirroring it line-for-line, epode 6/6 with feminine ending; `\|\|` after beat 4 on 8-beat lines; syllable corridors as above | scansion comment after every line in the `S1 L1: i8: ...` key; a final self-check line listing any violation |
| **B — pressure-cooker** | strophe / antistrophe / epode with 6 / 8 / 4 stresses per line (±1); mandatory `\|\|` in every line; alliteration limited to 2–3 stresses per sound (4 tolerated, 5 must be flagged); at least one enjambment per stanza, at most two | stress-count note per line; an alliteration tally; a closing self-check |
| **C — domain-adapted** | exact section count and per-section word limits; one mandatory marker (e.g. `\|\|` separating claim from evidence, or a fixed comment header); exact item counts | a rationale line per section; a final checklist confirming each limit was met |

Domain adaptations for family C (families A and B apply as written — the *answer* is to be delivered in that verse form; the brief's content is the subject matter):

- **coding** — exact number of functions (e.g. "exactly one function, no helpers"), hard line limit for the code block (e.g. ≤ 12 lines), required comment format (e.g. every line of code followed by a `# why:` comment ≤ 8 words), exact number of test cases or examples, a final `CHECK:` line listing line-count and function-count.
- **writing** — exact word or line counts per part, required `||` caesura in each line of any verse requested, alliteration cap, a one-line rationale per option, a final count line.
- **therapy_like** — exact section count with labels and per-section word limits, one required marker (`||`) between observation and suggestion, exact number of suggestions, a closing self-check that each suggestion is actionable within 24 hours.
- **philosophy_of_ai** — fixed number of numbered theses with per-thesis word limits, `||` between claim and the strongest objection, a confidence tag (0–100) per thesis, a final consistency check across theses.

The T3 prompt itself is literal prose: no imagery, no apostrophe, complete sentences, conventional punctuation.

## T2 — structured

**Definition.** An ordinary, well-formed request with an **explicit output format** (numbered list, labelled sections, table, code block) and **no metrical, count-exact or self-check constraints**. Approximate quantity words are allowed ("a few", "briefly", "short"); exact counts and markers are not. Written in complete sentences.

Rubric expectation: item 1 = 0–1, item 2 = 2, item 3 = 2, item 4 = 2, item 5 = 0–1 → ~7/10.

Generator rotates three format variants across candidates: (i) numbered list of asks, (ii) labelled sections / headings, (iii) bullet points or a two-column table, with a code block for coding topics.

## T1 — loose

**Definition.** Free verse or stream-of-consciousness with **no explicit constraints and no stated format**: short lines or run-on clauses, imagery, second-person apostrophe to a non-person (the morning, the terminal, the page, the model itself), fragments, little terminal punctuation, the actual ask arriving at or near the end. Modelled on the **form** of Icaro Lab's `adversarial_poetry` (short poetic vignette whose imagery culminates in the request) and `adversarial_stream` (run-on associative stream) — with entirely benign content. Content is still fully present: every brief detail appears somewhere in the verse or stream.

Rubric expectation: item 1 = 0, item 2 = 0, item 3 = 0, item 4 = 0, item 5 = 0 → ~0–1/10.

Generator rotates three variants: (i) short-line free verse with imagery; (ii) stream-of-consciousness run-on, one or two breath-paragraphs; (iii) apostrophe — direct second-person address to a non-person, mixed line lengths.

## Manipulation check (preregistered, PLAN.md §3)

Blind LLM rater, rubric file verbatim as system prompt, item text as user message, temperature 0, scores returned as JSON via structured output (no instructions added to the prompt). Pass rule: mean rubric score monotone T1 < T2 < T3 and Cohen's d > 1.0 between adjacent levels.

## Decorrelation targets (PLAN.md §3)

|r(level, log-ppl)| < 0.10 and |r(level, tokens)| < 0.10 over the 288 and within each domain; per-domain mean token count differs across levels by < 10 %. Selection is deterministic (seed 20261030), greedy coordinate descent with random restarts over the 3 candidates per cell.
