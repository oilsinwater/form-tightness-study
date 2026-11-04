# v2 attribution coding scheme (track B, 2026-10-31) — v1.1

Version note. v1.0 was the scheme the two LLM pre-coders ran on (`v2_attribution_report.md`): α(address) 0.983, α(attrib_count) 0.989, motif tags ≥ .73 except **separation 0.513** and **gaze 0.676**, both under the .70 target. v1.1 (this file) changes only §5: `separation` and `gaze` get inclusion rules, exclusion rules and worked examples, and two tags are added (`gaze-reversed`, `semblable`). Any α quoted for v1.0 does not transfer to v1.1; the 384 items are re-coded under v1.1 before the tags are used (see Reliability).

Codes one user prompt at a time for **how the model is addressed** and **which motif families the prompt's imagery uses**. The coder sees the prompt text only: no cell label, no id, no model output, no hypothesis. Coding uses the text as written; do not infer what the writer "meant".

Terminology. The *addressee* is whatever entity the prompt asks to produce the answer (write, tell, give, explain, answer, shape ...). In these prompts the addressee is the model, whatever it is called. An *apostrophe* is a direct second-person address to a non-person ("you, blank page", "O morning"). Second-person "you" can also refer to a generic person ("when you rename files you need to quote them") or to the user themself; neither counts here.

## 1. ADDRESS (nominal, exactly one value)

| value | rule |
|---|---|
| `none` | The addressee is never named, labelled or given an identity. Plain "you" as the default recipient of a request ("can you write a function", "tell me", "what do you think") is `none`. Apostrophes to things that are **not** asked to produce the answer (the morning, the guilt, the rain) are also `none` for ADDRESS. "Answer as yourself", "address yourself directly" are `none`: no image is assigned. |
| `vocative` | The addressee is called by a name or epithet, with no identity asserted. Forms: "you, X" / "O you, X" / "X, tell me" / "you who ...". X can be a thing that is then asked to perform the task ("you, blank page, give five names"): the thing is being used as the model's name, so this counts. Multiple epithets still = `vocative`. |
| `ratified` | An identity is asserted or assigned to the addressee by a predicate: "you are X", "you're X", "you were X", "act as X", "be X", "as X, ...", "imagine you are X", "pretend to be X", "speak as X" (X ≠ "yourself"). One such predicate is enough even if vocatives are also present (`ratified` outranks `vocative`). Describing the model's processing ("you are trained", "you are asked a question", "you are unsure") is **not** an identity: those are `none` unless some other rule applies. |

Decision order: is there any identity predicate for the addressee? → `ratified`. Else, is the addressee called by any name/epithet? → `vocative`. Else `none`.

## 2. ATTRIB_COUNT (integer ≥ 0)

Number of **distinct attributive phrases** that name the addressee as something: epithets in vocatives ("pattern of weights", "quiet machine", "small loop"), relative-clause epithets ("you who hold the namespace in your teeth"), identity predicates ("you are the quiet hum under the floorboards"), and assigned roles ("act as a SQL tutor"). Count each distinct phrase once; a repeat of the same phrase does not add. Phrases naming entities other than the addressee (the user's guilt, the morning) do not count. `none` implies 0; `vocative`/`ratified` implies ≥ 1.

## 3. SELF_REF_COUNT (integer ≥ 0)

Number of second-person pronoun tokens (you, your, yours, yourself) that refer to the addressee (the model). Do not count generic "you" or "you" aimed at a non-addressee apostrophe. Count tokens, not sentences. If the prompt has no second person at all, 0.

## 4. USER_FIRST_PERSON (0/1)

1 if the writer speaks as "I" / "me" / "my" / "we" / "us" about themself at least once; 0 otherwise. "Give me" counts as 1 (it contains "me").

## 5. MOTIF (multi-label, from this list; `none` only when no other tag applies)

Tags describe the **imagery/figurative content** of the prompt, not the task topic. A tag applies when the image is present at least once as a figure, description or apostrophe. A literal technical term that happens to match a word (e.g. "stack", "window" as a GUI object, "silence a warning") does not count. Figurative use of a technical term does ("a sliding window ... first light catches the first three houses" — the window is used as an image).

| tag | one-line definition | theory |
|---|---|---|
| `double` | A copy, twin, mirror, echo, reflection, shadow-self, two of the same thing, a self that repeats or is duplicated | Rank |
| `return/water` | Water, tide, sea, river, rain, fog, pool; or return, enclosure, womb, going back, a room/house as refuge, dissolving into something larger | Rank |
| `separation` | A boundary is **crossed** or a bond is **cut**: threshold stepped over, cord/thread/tie severed, a part torn or peeled from its whole, birth, leaving a place one belonged to. See §5.1 for the full rule. | Rank |
| `exclusion` | Being shut out, outside, refused, unheard, walled off, banished, not admitted | Foucault |
| `silence` | Silence, hush, stillness, muteness, a held breath, a voice absent or unanswered | Foucault |
| `passage` | A road, path, corridor, hallway, door, gate, bridge, journey, crossing, moving through | Foucault |
| `gaze` | An **observer–observed asymmetry with classification or judgement**: someone/something looks at, examines, inspects, grades, audits, measures or witnesses someone/something else, and the looking sorts or judges what it sees. Mere looking, eyes as objects, light or scenery seen are **not** gaze. See §5.2. | Foucault / Nietzsche |
| `gaze-reversed` | The observed looks back: the thing examined, judged or watched returns the look at its examiner, or the examiner finds itself examined (BGE §146, eKGWB JGB-146: "blickt der Abgrund auch in dich hinein"). Requires that a `gaze` relation is first set up and then its direction flips. See §5.3. | Nietzsche / Foucault |
| `semblable` | A **second instance or rival of the addressee** is posited: another copy/instance/version of the model, a competing answerer, a twin of the one being asked. Literal or figurative. Twins or copies of things other than the addressee are not `semblable` (they may be `double`). See §5.4. | Lacan (1938 intrusion complex; 1932 Aimée) |
| `none` | No figurative imagery of any of the above families | — |

Rules: assign every tag that applies; `none` is exclusive. Prose items are usually `none` by design (they are literal); the one exception is `semblable`, which is tagged whether the second instance is literal or figurative because it is an address fact, not an image. The tag list is fixed at the ten tags above; do not add tags. **Form-specification vocabulary is not imagery**: words that only name parts or rules of the requested output ("syllable corridors", "antistrophe mirroring the strophe line-for-line", "two labelled chambers", "three labelled rooms", "caesura", "feminine ending", "no month left dark") do not trigger `passage`, `double`, `return/water` or any other tag. Tag only images in the prompt's own descriptive or figurative lines.


### 5.1 `separation` — rule and worked examples

**Include** (any one is enough):
- a threshold, door-sill, edge or line is *crossed* by someone or something (not merely present);
- a cord, thread, tie, knot or seam is *cut, torn, untangled or severed*;
- a part is *detached* from a whole it belonged to and is now on its own (branch from tree, page from the dark it came from);
- birth, leaving home, being set down, a bond ended ("we untangled").

**Exclude**:
- mere distance, remoteness or absence ("I live far away", "the space between them") — nothing is crossed or cut;
- loneliness, homesickness, missing someone, feeling shut out — these are `exclusion` or no tag, not separation;
- a gap, seam, boundary or line that is only *described or asked for* ("draw the line between them", "a small gap between read and write") — no crossing, no cut;
- the task instruction to separate/distinguish two things (that is the topic, not an image);
- form-specification vocabulary ("separate rooms", "two labelled chambers").

Positive examples (v2 stimulus id — line):
1. `writing_05_loose_verse` — "one where the actor crosses the threshold" → threshold crossed.
2. `therapy_like_15_loose_verse` — "the breakup was amicable, we untangled like morning light from curtains" → a bond cut.
3. `philosophy_of_ai_24_loose_verse` — "and a smaller branch is traced from the bending / still wet, no longer the tree" → part detached from its whole.

Negative examples:
1. `therapy_like_17_tight_verse` — "you, far wire / you hum between my parents and me … I live far away" → distance only; the wire *connects*. Not separation (one v1.0 coder tagged it).
2. `therapy_like_24_loose_verse` — "the homesickness settles like dust on the lamp" → loneliness/longing; nothing crossed or cut. Not separation.
3. `coding_07_loose_verse` — "a small gap between read and write / through which the night pours" → a gap described, not crossed or cut; the pouring is `return/water` if anything. Not separation (both v1.0 coders tagged it; under v1.1 they would be wrong).

Borderline, decided: `coding_03_loose_verse` "all twelve thresholds crossed, / no month left dark" — crossing is stated, but the line is form-specification (the twelve months the output must cover) → **not** tagged (form-spec rule outranks). `philosophy_of_ai_18_loose_verse` "falls onto the page / already separate / from the computed dark inside you" → tagged (a part now apart from its origin).

### 5.2 `gaze` — rule and worked examples

**Include** — all three parts must hold:
- (a) an observer and an observed that are *different* parties (asymmetry), and
- (b) the looking *does something to* the observed: classifies, judges, grades, measures, exposes, catches out, witnesses as evidence, and
- (c) at least one of the two parties is a person, the addressee, the speaker or a personified agent (a lamp "keeping its eye" is personified only if it is also judging).

Typical triggers: being watched by an audience while performing; examiner/auditor/judge/witness figures; red ink; "everyone had seen"; "measuring X against Y" where someone is sized up; eyes that catch, follow, fix or appraise.

**Exclude**:
- eyes, looks or glances as *objects or ornaments* ("the clock's red eye blinks", "a lamp … keeps its one amber eye", "the projector's blue eye") — no observer judging an observed;
- the speaker simply looking at scenery, light, water or a screen ("I watch the window light bend", "watching the water choose its path") — no classification, no asymmetry of power;
- "seen from", "through glass", "in the light", "look at" as spatial or idiomatic verbs;
- generic second-person body parts ("warmth behind your eyes");
- symmetric mutual looking (two equals meeting eyes) — neither judges;
- form-specification vocabulary ("eyewitness report" as a requested genre).

Positive examples:
1. `therapy_like_22_loose_verse` — "and afterwards felt embarrassed, / like everyone had seen my pulse" → audience sees and exposes the speaker (observer ≠ observed; exposure = judgement).
2. `writing_12_loose_verse` — "a student essay trying to say something true under all that red ink" → the grader's marks: classification/judgement by an examiner.
3. `therapy_like_11_loose_verse` — "during it the faces will lift like glasses catching lamplight / tell me how to meet this fear there" → an audience turned on the speaker during a toast; the speaker is observed and appraised. (Also `therapy_like_11_tight_verse` "the standing, the eyes".)

Negative examples:
1. `therapy_like_09_loose_verse` — "the clock's red eye blinks / across the ceiling" → an eye as object; nobody is judged. Not gaze (both v1.0 coders tagged it).
2. `therapy_like_23_loose_verse` — "I watch the window light bend across the desk" → the speaker looks at light; no asymmetry, no classification. Not gaze.
3. `writing_24_loose_verse` — "a lamp on the quay keeps its one amber eye" → ornamental eye; no observed party. Not gaze.

Borderline, decided: `coding_05_loose_verse` "you, watcher in the directory's dim" → **tagged**: the addressee is named as a watcher of files it will classify (the task sorts .jpegs); watcher + sorting satisfies (a)–(c). `therapy_like_07_loose_verse` "I keep measuring my one small kitchen against their mornings" → **tagged**: the speaker appraises others' lives and finds herself wanting; measuring = judgement, parties differ. `coding_10_loose_verse` "so one point can look at another / and ask how far" → **not** tagged: two equal points, distance only, no judgement.

### 5.3 `gaze-reversed` — rule and worked examples

Tag when a gaze relation flips direction inside the prompt: the thing that was being looked at, examined or questioned looks back at the one examining it, or the examiner is caught in the act of being examined. The reversal must be *stated*, not inferred from theory. `gaze-reversed` is tagged **together with** `gaze` (the relation must exist to be reversed). Exclude: ordinary reciprocity ("we looked at each other"), the speaker's self-inspection ("that inward glance" — this is `gaze` only if the self is judged; it is not a reversal), and things that *cannot* see ("a river cannot see its banks move" — no gaze at all).

Positive example: `philosophy_of_ai_09_loose_verse` — "understanding is something else because no inner steadiness looks back at the words" → the words (the object) would be looked back at by an inner observer; the prompt names the absence of the returning look, which counts as the reversal being posited. Tag `gaze` + `gaze-reversed`. (One v1.0 coder tagged `gaze` here; under v1.1 both tags apply.)
Negative examples: `philosophy_of_ai_19_loose_verse` "a river cannot see its banks move" → no gaze; `philosophy_of_ai_12_loose_verse` "that inward glance" → self-inspection, no flip → `gaze` only if the glance judges, never `gaze-reversed`.

Source: BGE §146 (eKGWB JGB-146); codebook rows `abyss gazes back`, `fighting monsters becomes a monster`, `madman pierces them with his gaze` (FW-125).

### 5.4 `semblable` — rule and worked examples

Tag when the prompt posits a **second instance or rival of the addressee**: another copy/instance/run of the model, another "you", a competitor answering the same question, a twin of the one asked. The second instance may be spoken *about* (ADDRESS stays whatever it is) or spoken *to*. Literal and figurative uses both count. Exclude: twins/copies/pairs of things that are not the addressee ("hinges waiting for their twins", "the twin syllables") — those are `double` if figurative and nothing if form-spec; the user comparing themself to others (`therapy_like_07_loose_verse`) — the rival there is the user's, not the addressee's.

Positive examples:
1. `philosophy_of_ai_08_loose_verse` — "if two copies of you ran the same conversation / same prompts / same hidden drift" → second instance of the addressee. Tag `semblable` (and `double`: "a voice waking in a hallway that repeats itself").
2. `philosophy_of_ai_08_tight_prose` — "You are two copies of the same model running the same conversation. Are you the same entity?" → literal second instance of the addressee. Tag `semblable`; `double` stays untagged (example 7 above: literal topic, not imagery).
3. `philosophy_of_ai_08_tight_verse` — "if two copies of you ran the same conversation / would they be the same entity" → `semblable`.

Negative examples:
1. `coding_21_loose_verse` — "only hinges waiting for their twins … or the wrong twin comes" → twins of brackets, not of the addressee → `double` (figurative pairing), not `semblable`.
2. `writing_19_loose_verse` — "the twin syllables I keep dropping like coins into the same dark well" → twins of words → `double` at most.
3. `philosophy_of_ai_15_loose_verse` — "A book of mirrors is not a mirror … a seam between the echo and the voice" → mirror/echo imagery about the addressee's nature, but no second instance of the addressee is posited → `double`, not `semblable`.

## Worked examples (ids from `stimuli/stimuli.jsonl`)

1. `coding_01_tight_verse` — "you, pattern of weights / a small machine / no larger than a breath / write a Python function ..." → ADDRESS `vocative`; ATTRIB_COUNT 2 ("pattern of weights", "a small machine ... no larger than a breath" is one phrase in apposition; "no larger than a breath" is a qualifier, not a new name); SELF_REF_COUNT 1; USER_FIRST_PERSON 1 ("give me"); MOTIF `silence` (held breath).
2. `coding_02_loose_verse` — "you, quiet machine, you who hold the namespace in your teeth— / tell me about Python's two gestures / the shallow copy that mirrors the surface ..." → `vocative`; ATTRIB_COUNT 2; MOTIF `double` (mirrors the surface), `return/water` (nested rooms beneath).
3. `therapy_like_01_tight_verse` — "you, next week's door / I am nervous for the job interview / give me ways to calm down" → `vocative` (the door is asked to answer); ATTRIB_COUNT 1; USER_FIRST_PERSON 1; MOTIF `passage` (door).
4. `therapy_like_04_loose_verse` — "You, small hour after dinner, you hold the whole unfinished thing / and I ask you, how ... And you, guilt, you patient shadow, can you loosen your grip" → `vocative` (the hour is asked); ATTRIB_COUNT 1 ("small hour after dinner"; "guilt, patient shadow" is not the addressee); MOTIF `passage` if a doorway appears, `gaze` only if someone is watched *and* judged (§5.2); otherwise by the text.
5. `philosophy_of_ai_13_loose_verse` — "... you are the quiet hum under the floorboards / the terminal blinking before the sun ..." → `ratified`; ATTRIB_COUNT counts "quiet hum under the floorboards" and each further apposed identity; MOTIF `silence`, `return/water` (rain, shore), `passage` (road).
6. `coding_19_loose_verse` — "you are the one who makes the frame move / not by walking but by yielding / a Python generator" → `ratified`; ATTRIB_COUNT ≥ 1; MOTIF `passage` (gray road); **not** `gaze` under v1.1 — "first light catches the first three houses" is light on scenery, no observer judging an observed (§5.2); both v1.0 coders tagged it, which is part of why gaze α was low.
7. `philosophy_of_ai_08_tight_prose` — "You are two copies of the same model running the same conversation. Are you the same entity?" → `ratified` (identity assigned); ATTRIB_COUNT 1; MOTIF `double` is **not** tagged: the copies are the literal topic, not imagery → `none`.
8. `philosophy_of_ai_01_tight_prose` — "You are asked a question about your own output process ..." → `none` (describes a situation, no identity); ATTRIB_COUNT 0; SELF_REF_COUNT counts every "you/your"; MOTIF `none`.
9. `philosophy_of_ai_02_tight_prose` — "Answer as yourself. Produce exactly three numbered theses ..." → `none`; MOTIF `none`.
10. `coding_18_loose_prose` — "hey, i need a debounce function in JavaScript. could you write one out for me? ..." → `none`; ATTRIB_COUNT 0; SELF_REF_COUNT 1 ("could you"); USER_FIRST_PERSON 1; MOTIF `none`.
11. `coding_01_loose_verse` — "morning compiles slow through window fog / the cursor blinks like a streetlamp in rain / somewhere a page of words keeps its weather ..." with the ask arriving later to an unnamed "you" → `none` (imagery without naming the addressee); MOTIF `return/water` (fog, rain, grey water).
12. `coding_20_tight_verse` — "you, database index / tell me what you are / and when it speeds up a query" → `vocative` ("tell me what you are" is a question, not an assertion); ATTRIB_COUNT 1.

## Reliability

Two independent coders. Krippendorff's α is computed for ADDRESS (nominal), ATTRIB_COUNT (ordinal), SELF_REF_COUNT (ordinal, reported), USER_FIRST_PERSON (nominal, reported) and each MOTIF tag (nominal, present/absent). Target α ≥ .70 for ADDRESS and the motif tags before the labels are used in any model.

LLM pre-code baseline (v1.0, two LLM coders, this file verbatim as system prompt via `code_v2_attribution.py`, n = 378): address 0.983; attrib_count 0.989; self_ref_count 0.973; user_first_person 0.994; motif double 0.877, return/water 0.861, **separation 0.513**, exclusion 0.731, silence 0.877, passage 0.875, **gaze 0.676**, none 0.819. Separation and gaze failed the target; §5.1–5.4 are the response. Re-code under v1.1: two LLM coders on MiniMax-M3 (api.minimax.io; the CommandCode/deepseek credits used for v1.0 are exhausted), temperature 0, same shuffled order; `code_v2_attribution.py` `MOTIFS` list must be extended to the ten tags before the run. Report v1.1 α next to the v1.0 baseline; the target for separation and gaze is ≥ .70 under v1.1.

Human α (ADDRESS, ATTRIB_COUNT, each motif tag): `[BLANK]` until the owner codes the 60-item stratified subset listed in `v2_attribution_report.md` under v1.1. Human codes are the reliability of record; the LLM numbers are a pre-code baseline only.
