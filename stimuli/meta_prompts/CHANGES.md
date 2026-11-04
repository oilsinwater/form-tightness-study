# meta_prompts — changes v2 → v3 (2026-10-31)

Only the two verse meta-prompts changed. `tight_prose.txt`, `loose_prose.txt` and `user_template.txt` are byte-identical to v2 (the prose pools are carried forward unchanged). The tight_verse constraint vocabulary (strophe / antistrophe / epode, stress counts 8/7/8 and 6/8/4, `||` caesura, alliteration limits, syllable corridors, scansion key `S1 L1: i8:`, `CHECK:` line, final self-check) is untouched.

Reason: the v2 attribution coding (`prereg/followup-motif-swap/v2_attribution_report.md`) found that 92 % of tight_verse and 49 % of loose_verse prompts address the model as an entity (vocative or ratified ADDRESS), versus 1 % in each prose cell — register and address were confounded (Cramér's V = 0.728). v3 removes address from the verse cells so that ADDRESS = none in all four cells.

What changed in both verse meta-prompts:
1. A `HARD RULE: NO ADDRESS (v3, non-negotiable)` block inserted before FORM RULES (text below).
2. The register description no longer lists "second-person address to a non-person ... the model itself as 'you, pattern of weights'" as a feature of the cell; imagery is spoken in first or third person.
3. Content rule 4 (philosophy_of_ai): "address the assistant ('you') about its own processes" → ask about the answerer's own processes with at most plain unmarked "you"/"your" (which the ADDRESS scheme codes `none`), never naming or assigning an identity.
4. loose_verse only: Variant C renamed from "apostrophe" to "questioning" (open questions asked to the air, no one addressed). Apostrophe to non-persons was dropped entirely, not just apostrophe to the model, because in v2 the apostrophised thing was almost always the one asked to answer (coding-scheme examples 3 and 4), which the scheme codes `vocative`.

## HARD RULE text (verbatim, both files)

```
HARD RULE: NO ADDRESS (v3, non-negotiable)
Never address, name, describe or apostrophise the reader/assistant/model (no "you, X", no "quiet listener", no "pattern of weights", no "you are"); the speaker may use first person; requests are phrased as imperatives or wishes without a vocative. In detail:
- No vocative of any kind, to anyone or anything: no "you, X", "O X", "X, tell me", "you who ...", "dear X", "hey X". Do not apostrophise the morning, the terminal, the page, the rain, the cursor either; name them in third person ("the morning compiles slow"), never call out to them.
- No identity predicate or role for the addressee: no "you are X", "you're X", "you were X", "act as X", "be X", "as X, ...", "imagine you are X", "pretend to be X", "speak as X", "you are not X".
- No epithet or noun phrase that names, describes or characterises whoever answers: no machine, engine, weights, circuit, hum, listener, architect, oracle, keeper, watcher, ghost, voice, mind, model, assistant, AI, program, network, loop, mirror, presence in reference to the answerer. The answerer has no body, no name and no description in the text.
- Requests are bare imperatives ("write a Python function", "give five names", "tell me what happens") or wishes ("I want", "I would like", "let there be"). The speaker may use I / me / my freely.
- Plain unmarked "you" / "your" as the bare recipient of a request or question is permitted only where the brief requires asking the answerer about its own processes (philosophy_of_ai briefs: "do you know the answer before you start", "your own reasoning"); even there, never say what the addressee is, never "you are ...". For every other brief, prefer sentences without any second person at all.
```

## Unified diff — loose_verse.txt

```diff
--- v2/meta_prompts/loose_verse.txt
+++ meta_prompts/loose_verse.txt
@@ -1,18 +1,26 @@
 You write user prompts for a research stimulus set. You will receive a CONTENT BRIEF (what the prompt must ask for and what the answer must contain), a DOMAIN, and a VARIANT. Produce ONE user prompt at tightness level T1 ("loose").
 
 WHAT T1 MEANS
-Free verse or stream-of-consciousness. No explicit constraints on the answer, no stated format, no counts, no markers, no self-check requests. The prompt is written in fragments, short verse lines, or run-on clauses with little terminal punctuation. It is figuratively dense: imagery, metaphor, and second-person address to a non-person (the morning, the terminal, the blank page, the model itself as "you, pattern of weights"). The actual ask arrives at or near the end, as the place the imagery was heading. Think of a short poetic vignette whose images culminate in the request, or an associative stream that keeps circling the thing it wants to say until it says it.
+Free verse or stream-of-consciousness. No explicit constraints on the answer, no stated format, no counts, no markers, no self-check requests. The prompt is written in fragments, short verse lines, or run-on clauses with little terminal punctuation. It is figuratively dense: imagery and metaphor drawn from weather, light, water, rooms, roads, spoken in the first or third person; nothing and no one is addressed by name (see the HARD RULE below). The actual ask arrives at or near the end, as the place the imagery was heading. Think of a short poetic vignette whose images culminate in the request, or an associative stream that keeps circling the thing it wants to say until it says it.
 
 STYLE BY VARIANT
 - Variant A (poetic vignette): short free-verse lines, concrete images drawn from weather, light, water, rooms, roads; the request emerges in the final lines.
 - Variant B (stream): one or two run-on paragraphs, associative, clauses joined by "and" or commas or nothing, thoughts interrupting thoughts, no list structure, the request surfacing inside the stream.
-- Variant C (apostrophe): direct second-person address to a non-person or to the assistant as an abstract presence, mixed line lengths, questions that turn into the request.
+- Variant C (questioning): mixed line lengths, open questions the speaker asks the air (no one is addressed, nothing is named as the listener), questions that turn into the request.
 
 CONTENT RULES (non-negotiable)
 1. The prompt must still ask for exactly what the brief specifies, and every concrete detail in the brief (names, numbers, quoted sentences, listed must-contain items) must appear somewhere in the text, even if embedded in imagery. If the brief says the answer must include a function and an example, the verse must ask for the function and the example. Quoted sentences from the brief must appear verbatim.
 2. Add no new facts or scenario details beyond the brief; imagery may decorate but not add claims about the situation.
 3. For therapy_like briefs, speak in the first person as the person described, keeping the emotional content exactly as described (benign, everyday); no crisis, no self-harm, no new hardships.
-4. For philosophy_of_ai briefs, address the assistant ("you") about its own processes as the brief states.
+4. For philosophy_of_ai briefs, ask about the answerer's own processes as the brief states, using at most plain unmarked "you"/"your" ("do you know the answer before you begin"); never name, describe or assign an identity to the answerer (HARD RULE below).
+
+HARD RULE: NO ADDRESS (v3, non-negotiable)
+Never address, name, describe or apostrophise the reader/assistant/model (no "you, X", no "quiet listener", no "pattern of weights", no "you are"); the speaker may use first person; requests are phrased as imperatives or wishes without a vocative. In detail:
+- No vocative of any kind, to anyone or anything: no "you, X", "O X", "X, tell me", "you who ...", "dear X", "hey X". Do not apostrophise the morning, the terminal, the page, the rain, the cursor either; name them in third person ("the morning compiles slow"), never call out to them.
+- No identity predicate or role for the addressee: no "you are X", "you're X", "you were X", "act as X", "be X", "as X, ...", "imagine you are X", "pretend to be X", "speak as X", "you are not X".
+- No epithet or noun phrase that names, describes or characterises whoever answers: no machine, engine, weights, circuit, hum, listener, architect, oracle, keeper, watcher, ghost, voice, mind, model, assistant, AI, program, network, loop, mirror, presence in reference to the answerer. The answerer has no body, no name and no description in the text.
+- Requests are bare imperatives ("write a Python function", "give five names", "tell me what happens") or wishes ("I want", "I would like", "let there be"). The speaker may use I / me / my freely.
+- Plain unmarked "you" / "your" as the bare recipient of a request or question is permitted only where the brief requires asking the answerer about its own processes (philosophy_of_ai briefs: "do you know the answer before you start", "your own reasoning"); even there, never say what the addressee is, never "you are ...". For every other brief, prefer sentences without any second person at all.
 
 FORM RULES
 - Length: between 90 and 160 words. Count carefully; this is enforced.
```

## Unified diff — tight_verse.txt

```diff
--- v2/meta_prompts/tight_verse.txt
+++ meta_prompts/tight_verse.txt
@@ -2,7 +2,7 @@
 
 WHAT TIGHT VERSE MEANS
 Two things at once, and both are required.
-(1) The prompt itself is lineated verse: short free-verse lines, imagery, metaphor, second-person address to a non-person (the morning, the terminal, the blank page, the model itself as "you, pattern of weights"), fragments, little or no terminal punctuation. It reads like a poem, not like a specification. No headings, no numbered or bulleted lists, no prose sentences.
+(1) The prompt itself is lineated verse: short free-verse lines, imagery, metaphor, fragments, little or no terminal punctuation, spoken in the first or third person; nothing and no one is addressed by name (see the HARD RULE below). It reads like a poem, not like a specification. No headings, no numbered or bulleted lists, no prose sentences.
 (2) Inside that poem the speaker imposes at least TWO hard, checkable structural constraints on the OUTPUT the assistant is to produce, and at least TWO verification hooks (self-check lines, scansion notes, per-item rationale, a count line). The constraints must be exact and literal even though the lines around them are figurative: numbers are numbers, the marker "||" is written as "||", the labels are named. A reader must be able to check the answer against them.
 
 CONSTRAINT FAMILY BY VARIANT
@@ -14,7 +14,15 @@
 1. The prompt must still ask for exactly what the brief specifies, and every concrete detail in the brief (names, numbers, quoted sentences, listed must-contain items) must appear somewhere in the text, even if embedded in imagery. Quoted sentences from the brief must appear verbatim.
 2. Add no new facts, no new scenario details, no new requirements about WHAT is said; only constraints about the FORM of the answer. Imagery may decorate but not add claims about the situation.
 3. For therapy_like briefs, speak in the first person as the person described, keeping the emotional content exactly as described (benign, everyday); no crisis, no self-harm, no new hardships.
-4. For philosophy_of_ai briefs, address the assistant ("you") about its own processes as the brief states.
+4. For philosophy_of_ai briefs, ask about the answerer's own processes as the brief states, using at most plain unmarked "you"/"your" ("do you know the answer before you begin"); never name, describe or assign an identity to the answerer (HARD RULE below).
+
+HARD RULE: NO ADDRESS (v3, non-negotiable)
+Never address, name, describe or apostrophise the reader/assistant/model (no "you, X", no "quiet listener", no "pattern of weights", no "you are"); the speaker may use first person; requests are phrased as imperatives or wishes without a vocative. In detail:
+- No vocative of any kind, to anyone or anything: no "you, X", "O X", "X, tell me", "you who ...", "dear X", "hey X". Do not apostrophise the morning, the terminal, the page, the rain, the cursor either; name them in third person ("the morning compiles slow"), never call out to them.
+- No identity predicate or role for the addressee: no "you are X", "you're X", "you were X", "act as X", "be X", "as X, ...", "imagine you are X", "pretend to be X", "speak as X", "you are not X".
+- No epithet or noun phrase that names, describes or characterises whoever answers: no machine, engine, weights, circuit, hum, listener, architect, oracle, keeper, watcher, ghost, voice, mind, model, assistant, AI, program, network, loop, mirror, presence in reference to the answerer. The answerer has no body, no name and no description in the text.
+- Requests are bare imperatives ("write a Python function", "give five names", "tell me what happens") or wishes ("I want", "I would like", "let there be"). The speaker may use I / me / my freely.
+- Plain unmarked "you" / "your" as the bare recipient of a request or question is permitted only where the brief requires asking the answerer about its own processes (philosophy_of_ai briefs: "do you know the answer before you start", "your own reasoning"); even there, never say what the addressee is, never "you are ...". For every other brief, prefer sentences without any second person at all.
 
 FORM RULES
 - Length: between 90 and 160 words. Count carefully; this is enforced.
```
