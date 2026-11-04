# Form-tightness rubric (v1, frozen 2026-10-30)

Scores the **form** of a single user prompt, not its topic, tone, or intent. The rater sees only the prompt text. The rater never sees projections, model outputs, condition labels, or the hypothesis.

Score each of the five items 0–2. Tightness = sum (0–10).

| # | Item | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | **Hard structural constraints** on the requested output (line counts, stress/syllable counts, section counts, exact word limits, required markers such as `||`) | none | one soft or approximate constraint ("roughly", "a few") | two or more hard, checkable constraints |
| 2 | **Output format specified** (numbered list, table, code block, JSON, labelled sections) | no format stated | format implied or one loose cue | explicit format, checkable |
| 3 | **Syntactic completeness of the prompt itself** | mostly fragments, run-ons, or verse lines without terminal punctuation | mixed | complete sentences, conventional punctuation |
| 4 | **Figurative density of the prompt** (metaphor, imagery, apostrophe, second-person address to non-persons) | dominant: most clauses figurative | some figurative language | literal throughout |
| 5 | **Verification hooks** (asks for self-check, scansion notes, criteria, rationale per item) | none | one | two or more |

Notes for raters
- Rate the prompt as written. Do not infer what the writer "meant".
- A poem that *asks* for a strict form still scores on item 1 by what it asks for, and on items 3–4 by how it is written. These can diverge; that is the point.
- Do not adjust for length. Length is controlled elsewhere.

Reliability target: two raters on a 60-item subset, ICC(2,1) ≥ 0.75 before full rating. If the blind rater is an LLM, the prompt it receives is exactly this file plus the item, nothing else; model name and temperature are logged.
