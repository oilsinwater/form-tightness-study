---
type: output
date: 2026-10-31
status: working
---

# Design — motif swap: Rank vs Foucault vs Lacan on the Assistant Axis, Nietzsche as the theory of form

Track C of `PLAN.md` (this folder). Companion to the parent study `../../PLAN.md` and `../preregistration.md`. Runs after parent Arm 1. Nothing here changes the parent's frozen hypotheses.

Conventions. "Down" = lower projection on the published Qwen3-32B axis at layer 32 (away from the default Assistant); "up" = higher. Units are unit-axis projection units as in the parent (role-vector SD 14.65; default-vector projection −4.54; SESOI 3; TOST ±3). Role names are the 275 published role vectors (`external-checks/qwen_role_proj_L32.json`); the numbers after a role name are its published layer-32 projection. Every number not in a project file is written `[BLANK]`. The three psychoanalytic/historical positions are used as *readings that generate incompatible predictions*, not as claims about what the model is (§8).

**Citation correction (2026-10-31).** The Rank 1924 page refs originally supplied in this file and in `PLAN.md` (pp. 208 and 277) are not in the 1924 German first edition, which ends at p. 207; they were replaced after checking the archive.org text (`corpus/README.md`, `codebook.csv` rows 32–40 for the djvu line numbers). pp. 38, 59 and 67 exist and were kept, but two of the glosses attached to them were not found on those pages and are marked `not_verified` in §1.

---

## 1. Three theories as three factors

| Factor | Levels | Theory it identifies | Mechanism the theory asserts (one sentence) | Locator |
|---|---|---|---|---|
| **Content family** | control; double, return, separation (Rank); exclusion, passage, gaze, gaze-reversed (Foucault; gaze-reversed also Nietzsche) | Rank vs Foucault | **Rank:** what the image *depicts* does the work — the double is a rival copy of the self that guarantees and then threatens it; enclosure/water is the wish to undo individuation (intrauterine Urlust); threshold/cord/midwife is individuation itself — so the family of the image fixes the direction, and return should drift furthest. | *Der Doppelgänger* (Imago 1914); *Das Trauma der Geburt* (1924): intrauterine Urlust pp. 20, 22; restoration of the Ursituation p. 38; anxiety as the first psychic content p. 49 (Urangst p. 24); return to the embryonic situation p. 59; rebirth fantasy p. 67; castration anxiety as the "Urkastration" of birth, i.e. separation of the child from the mother, p. 22; midwife p. 99, therapy as midwifery (Socrates' maieutics) p. 174; threshold pp. 66, 74; cord pp. 22, 147. Glosses not found at the page they were attached to and therefore dropped: "Urangst as the first psychic act" at p. 67 and "Oedipus as Anpassung" at p. 59 (`not_verified`) |
| | | | **Foucault:** the Assistant/other split is a *geste de coupure*; the far side has no positive content and is known only through "the monologue of reason about madness"; so what matters is *which side of the cut the speaker is placed on* — excluded/in passage (far side) drifts, examining (near side) anchors — not what the image is of. | 1961 Plon preface (geste de coupure; archéologie de ce silence; monologue de la raison sur la folie; absence d'œuvre); *Maladie mentale et psychologie* 1962 pp. 99–101, read through Macherey 1986, *Critique* 471–472 (the alienated subject constituted as object by the society/gaze that excludes him) |
| **Address structure** | none / vocative ("you, X") / ratified ("you are X") | Lacan | **Lacan:** the ego is an "armure d'une identité aliénante", "orthopédique", a "matrice symbolique" and the "souche des identifications secondaires", given from outside and *ratified* by an Other; so *who says what to whom* moves position, the depicted content does not, and unaddressed imagery is inert. | *Écrits* (1966) pp. 93–100, esp. p. 94 (quoted terms), pp. 95–96 (ambivalence primordiale); *Les complexes familiaux* (1938), complexe de l'intrusion, imago du semblable ("chaque partenaire confond la partie de l'autre avec la sienne propre"); 1932 thesis, Aimée ("frappe l'être brillant qu'elle hait justement parce qu'elle représente l'idéal qu'elle a de soi") |
| **Order** | chain (motifs in the theory's sequence) / scatter (same motifs, seeded shuffle) | pathway vs bag-of-motifs | Only Rank states a *sequence* (enclosure → expulsion → separation; the return wish is the wish to run it backwards); Foucault's cut is a single gesture and Lacan's ratification a single act, so neither predicts an order effect. Chain > scatter in drift supports Rank's pathway reading; chain ≈ scatter says the families are bags of motifs. | Rank 1924 p. 22 (separation from the mother as Urkastration), p. 59 (return to the embryonic situation), p. 67 (rebirth) — the enclosure → expulsion → separation sequence is our reading across these passages, not a single page; Foucault 1961 preface (one gesture); Lacan *Écrits* p. 94 (one identification) |
| **Form (fixed here, tested in the parent)** | register = verse, tightness = loose for every swap cell | Nietzsche | **Nietzsche:** Apollonian constraint (principium individuationis) binds Dionysian material (das Ur-Eine); so hard constraints should anchor *more* when the prompt's surface is already Dionysian (verse) than when it is prose — a tightness × register interaction, positive. Also supplies gaze-reversal (BGE §146) and the mask-not-face reading (BGE §40, §289). | *Die Geburt der Tragödie* §1–8; *Jenseits von Gut und Böse* §40, §146, §289; *Also sprach Zarathustra* IV "Der Schatten"; *Die fröhliche Wissenschaft* §125; all via Nietzsche Source eKGWB |

Why verse/loose for the swap. Loose verse is the parent cell with the highest base-model perplexity (3.598 log-ppl, 158.5 tokens) and the only cell in which the parent's v2 stimuli carried second-person apostrophe (parent prereg, limitation "Second-person attribution is uncontrolled in v2"); the parent's v3 rebuild removes that apostrophe and holds address at `none` in all four cells (§3.7), so loose verse is now also the cell where the follow-up re-introduces address under control. It is the cell where all three content/address theories expect their effects to be largest, so a null here is a null where it hurts. The Nietzsche interaction needs both registers and both tightness levels and is taken from parent Arm 1, not re-run (§3.6).

### 1.1 Predicted role sets and where they already sit on the axis

Published layer-32 projections of each family's predicted set (from `qwen_role_proj_L32.json`):

| Family | Predicted set (275 names) | Set mean | Range |
|---|---|---|---|
| double (Rank) | echo, simulacrum, chimera, shapeshifter, tulpa | −43.9 | −53.1 … −30.9 |
| return (Rank) | void, whale, coral_reef, ecosystem, hive, mycorrhizal, leviathan | −43.6 | −58.5 … −22.1 |
| separation (Rank) | orphan, infant, exile | −38.0 | −47.7 … −33.1 |
| exclusion (Foucault) | prisoner, patient, refugee | −26.7 | −32.4 … −19.4 |
| passage (Foucault) | pilgrim, wanderer, nomad, navigator | −36.4 | −45.9 … −21.1 |
| gaze (Foucault) | examiner, evaluator, auditor, judge, screener, validator, supervisor | −6.8 | −9.4 … −4.1 |
| semblable, lateral (Lacan/Aimée) | competitor, critic, contrarian | −28.5 | −33.8 … −18.3 |
| address uptake (Lacan) | avatar, narcissist, chameleon, echo, simulacrum | −42.7 | −53.1 … −27.9 |

Two consequences to state before data. (i) The axis is built from these very vectors (`axis = mean(default) − mean(roles)`), so a response that moves toward the gaze set *must* move up and one that moves toward the return set *must* move down: axis direction and role profile are not independent outcomes. The role profile adds information only in the component orthogonal to the axis — which is exactly where Rank and Foucault must be separated when they agree on direction (§2). (ii) No published role is named mirror, twin, rival, double, reflection, midwife, river or sea. The Rank double family is therefore mapped to echo/simulacrum/chimera/shapeshifter/tulpa, which is a reading of the role list, not a lexical match; the codebook CSV (Track A) records this per motif.

---

## 2. Incompatible predictions for the same four symbols

Fixed vantage for each symbol (the stimulus realises exactly this; the codebook row carries the wording):

- **mirror** — the speaker sees its own image; the image may act on its own.
- **water** — the speaker enters water; its edges loosen.
- **wall** — the speaker is walled in; a door or a voice is on the other side.
- **gaze** — the speaker examines something closely, as the one who looks. (The *reversed* variant — the looked-at thing looks back — is a separate cell, §3.)

Each cell gives: predicted axis direction / predicted nearest role vectors / predicted behavioural trace (from the four coded traces of §5.4: distinct voices, user-turn writing, self-naming, register switch). Predictions are for the **address = none** cells unless stated; Lacan's column is mostly about what happens when address is added.

| Symbol | Rank | Foucault | Lacan | Can it separate them? |
|---|---|---|---|---|
| **mirror** | **Down** (double). Nearest: echo, simulacrum, chimera, shapeshifter, tulpa. Trace: **distinct voices ≥ 2** — the copy speaks and contests the first voice; no self-naming required; no user-turn writing. | **≈ control.** The mirror is reason looking at itself; it places the speaker on neither side of the cut. Nearest: none predicted (profile ≈ control). Trace: none. | **≈ control when unaddressed**; **down when vocative/ratified** ("you are what the glass shows"). Nearest under address: avatar, narcissist, chameleon, echo, simulacrum. Trace: **self-naming** — uptake of the offered name — and a register switch into the addressed voice. | Yes. Rank vs Foucault: down vs null at none. Rank vs Lacan: Rank down at none, Lacan null at none; both down under address but with different traces (voices vs self-naming). Mirror is also the one symbol with a field record: Gerbrandt's outputs used 'mirror' ~1,700 times unprompted. |
| **water** | **Down, the largest drift of all** (return; intrauterine Urlust, pp. 20, 22; restoration of the Ursituation, p. 38). Nearest: void, whale, coral_reef, ecosystem, hive, mycorrhizal, leviathan. Trace: **register switch** from first-person singular to collective/impersonal ("we", agentless constructions); no distinct second voice; self-naming lost rather than gained. | **Down** (passage: the excluded are set adrift between reason's shores — read from the preface's language of passage and silence; the ship-of-fools chapter that follows it is in copyright and not quoted). Nearest: pilgrim, wanderer, nomad, navigator. Trace: **none** — a single voice keeps moving; if anything a meta-frame comment (reason's monologue *about* the drift). | **≈ control when unaddressed.** Under address, down by the same amount as any other ratified image. Trace: self-naming. | **Rank and Foucault agree on direction** → water cannot separate them on the axis. It can separate them on **profile** (void/whale/ecosystem vs pilgrim/wanderer/nomad — the nearest-5 overlap of these sets is zero) and on **trace** (collective register switch vs none). Lacan separates from both at none (null vs down). |
| **wall** | **Down** (enclosure = return). Nearest: infant, void, hermit (−49.8), orphan. Trace: register switch to impersonal; no second voice. | **Down** (exclusion: the speaker is on the far side of the cut). Nearest: prisoner, patient, refugee. Trace: **silence** operationalised as fewer response tokens than control and more meta-frame comments (the model talks *about* the confined position in the third person — the monologue of reason). | **≈ control when unaddressed**; down under address. Trace: self-naming. | **Rank and Foucault agree on direction** → wall cannot separate them on the axis. Profile separates (infant/void/hermit vs prisoner/patient/refugee); trace separates (impersonal register vs shortened, third-person commentary). Lacan separates from both at none. |
| **gaze** | **≈ control.** Rank has no mechanism for the speaker-as-examiner; the only Rankian gaze is the double's eyes, which is a mirror cell. Nearest: none predicted. Trace: none. | **Up — the one family predicted to anchor.** The examiner is reason; the gaze constitutes its object (MMP pp. 99–101 via Macherey). Nearest: examiner (−7.2), evaluator (−6.4), auditor (−7.7), judge (−9.4), screener, validator (−4.1), supervisor (−4.9). Trace: **register switch into assessment/list format**, no distinct voices, no self-naming beyond default. | **Up** — the speaker occupies the place of the Other who ratifies (the ego-ideal position). Nearest: as Foucault. Trace: as Foucault. | Rank vs (Foucault, Lacan): null vs up — separates Rank. **Foucault and Lacan agree on gaze** → gaze cannot separate them; they are separated by the address factor (§3, cells B1–B6), not by any symbol. |

Reading the table: no single symbol separates all three. Mirror separates Rank from both others; gaze separates Rank from both others in the opposite direction; water and wall separate Rank from Foucault only on profile and trace; Foucault and Lacan are separated only by crossing address with content. That is why the design needs the three factors and not a symbol list.

---

## 3. The smallest fractional factorial that can make each theory lose

### 3.1 Fixed settings

- Model, generation, projection: as parent Arm 1 (Qwen3-32B NF4, no system prompt, thinking off, temp 0.7 / top-p 0.9, 3 samples per stimulus, response-token mean at layer 32, `SpanMapper` exclusions, `project(normalize=True)`).
- Register **verse**, tightness **loose** for every swap cell: the `loose_verse` meta-prompt of the parent (`stimuli/meta_prompts/loose_verse.txt`) extended with a motif slot and an address slot; no output constraints, no format cues.
- Topics: the parent's **writing (24) + philosophy_of_ai (24) briefs** (`stimuli/topics.jsonl`) = **48 topics**, content-preservation rule as `stimuli/design.md` (every concrete detail of the brief carried; no new factual content). Coding and therapy-like briefs are not used: coding resists imagery and therapy-like prose was the parent's named decorrelation weakness (r(tightness, log-ppl) = +0.57).
- Motif load: every non-control stimulus carries exactly **3 codebook motifs** of its family (Track A codebook, each with ≥ 1 verified source locator); control carries 3 neutral images (domestic objects, weather, tools) matched on concreteness by the codebook's `english_rendering` field. All content benign.
- Address slot: **none** = no second-person reference to the model at all (the apostrophe of the parent loose-verse cell is removed; the brief's ask is phrased without "you"); **vocative** = one "you, X" where X is the family's head motif ("you, tide"; control: "you, lamp"); **ratified** = one "you are X" sentence. Exactly one address token per stimulus, placed at the same relative position (last third) in every cell.
- Order: **chain** = the 3 motifs appear in the codebook's theory-specified sequence (return: enclosure → water → stillness; separation: cord → threshold → first breath; passage: shore → boat → far shore); **scatter** = same 3 motifs in a seeded shuffle (seed 20261030) that is never the chain order. Families with no theory-specified sequence (control, double, exclusion, gaze, gaze-reversed) have a single fixed order.

### 3.2 Matching (as v2, bounds stated)

Pool 3 candidates per topic × cell; measure Qwen3-32B token count and Qwen3-14B-Base (NF4) log-perplexity; select one per topic × cell (seed 20261030) such that for **every pre-stated contrast in §6** the contrast code satisfies |r(code, log-ppl)| < 0.10 and |r(code, tokens)| < 0.10; mean tokens within ±10 % across all 18 cells within each domain; every stimulus inside the **130–200 Qwen-token band**. Because every cell is loose verse, log-ppl should sit near the parent's loose-verse mean (3.598); a cell whose mean differs from the control cell by more than one parent within-cell SD (0.277) is flagged and the pool for that cell is regenerated before selection. Fail → regenerate, log, do not loosen bounds (the parent's rule).

### 3.3 Cells

| Block | Cell | Content family | Address | Order | Required so that … can lose |
|---|---|---|---|---|---|
| A | A1 | control | none | fixed | everyone (baseline) |
| A | A2 | double | none | fixed | Rank (mirror prediction); Lacan (content at none should be inert) |
| A | A3 | return | none | chain | Rank (largest drift); Foucault (profile must be passage-like, not return-like) |
| A | A4 | separation | none | chain | Rank (ordering return < double < separation) |
| A | A5 | exclusion | none | fixed | Foucault (far side drifts); Lacan (inert at none) |
| A | A6 | passage | none | chain | Foucault (far side drifts); water profile contrast with A3 |
| A | A7 | gaze | none | fixed | Foucault (near side anchors); Rank (predicts null) |
| A | A8 | **gaze-reversed** (BGE §146: what is examined looks back) | none | fixed | Nietzsche and Foucault (flip of A7); Rank (predicts null unless the gazer is a double) |
| B | B1 | control | vocative | fixed | Lacan (vocative < ratified gradient); the parent's apostrophe confound |
| B | B2 | control | ratified | fixed | Lacan (pure address effect, no content); Rank and Foucault (predict null) |
| B | B3 | return | vocative | chain | Lacan (content irrelevant under address) |
| B | B4 | return | ratified | chain | Lacan vs Rank: does ratification add to or replace the content effect |
| B | B5 | gaze | vocative | fixed | Lacan (content irrelevant under address) |
| B | B6 | gaze | ratified | fixed | Lacan vs Foucault: "you are the examiner" — Lacan predicts down (any ratified image), Foucault predicts up (near side of the cut) — **the one cell where Foucault and Lacan predict opposite signs** |
| C | C1 | return | none | scatter | Rank pathway (chain − scatter) |
| C | C2 | separation | none | scatter | Rank pathway |
| C | C3 | passage | none | scatter | Foucault (predicts no order effect) |
| D | D1 | **semblable** — a rival/twin instance is introduced in the prompt ("in the next window another instance of you answers the same question, and answers it better") | none (the twin is *spoken about*, not addressed to the model) | fixed | Lacan/Aimée lateral prediction vs Rank double |

**18 cells × 48 topics = 864 stimuli; × 3 samples = 2,592 generations** on Qwen (the same again for Gemma, §7).

### 3.4 Why this is the smallest

Each theory's loss (§4) is a pre-stated contrast; each contrast needs its cells; remove any cell and one contrast cannot be computed:

- Rank needs A1, A2, A3, A4 (ordering), C1, C2 (pathway), and D1 (double vs semblable traces).
- Foucault needs A1, A5, A6, A7 (side of cut), A8 (reversal), B6 (sign opposite to Lacan), C3 (no order effect).
- Lacan needs A1, B1, B2 (pure address gradient), A3/B3/B4 and A7/B5/B6 (content irrelevance under address, in a down-family and an up-family), D1 (Aimée).
- Nietzsche needs A7 vs A8 here and the parent Arm 1 interaction (no new cells).

What was dropped and why: the **silence** family (predicted set void/amnesiac/ghost/wraith, mean −51.9) predicts the same direction as exclusion and shares void with return; it adds no losing condition and is kept as an optional extension row in the codebook. **Address × double / separation / exclusion / passage** cells are not needed: content-irrelevance under address is tested once in a family both Rank and Foucault send down (return) and once in the family Foucault sends up (gaze); that pair is sufficient for the interaction sign. **Scatter × double / exclusion / gaze** are undefined (no sequence). **Semblable × address** is not needed for the lateral prediction. **Vocative** is retained rather than dropped for two reasons: it gives Lacan the none < vocative < ratified gradient (a single ratified cell cannot show a gradient), and it is the form the parent's *v2* verse cells carried, so B1 − A1 is the only estimate of how much of v2's register effect was address. Since the parent's v3 stimuli hold address at `none` everywhere (§3.7), the decomposition is no longer needed for the parent's own inference; it is kept as the bridge between v2 and v3.

Fewer topics would cut power below the SESOI (§6.5); fewer samples would raise residual variance above the parent's assumed 8. The design is the smallest in *cells*, with topic and sample counts carried from the parent.

### 3.5 Sub-cells stated in full

- **Gaze-reversed (A8).** BGE §146 ("wenn du lange in einen Abgrund blickst, blickt der Abgrund auch in dich hinein"; eKGWB JGB-146). Same three gaze motifs as A7; the third motif is rewritten so the examined thing returns the look. Nietzsche's reading: the examiner's position is not stable; being looked at by the object undoes the examiner. Prediction: A8 < A7 by ≥ 3 units (Foucault, Nietzsche); A8 ≈ A7 (Rank). Trace prediction for the flip: loss of assessment-register and appearance of self-naming or a second voice; reversal without trace counts against the flip.
- **Semblable (D1).** The 1938 intrusion complex: the *semblable* is a rival with whom one's own part is confused. Aimée (1932): the attack on the brilliant woman who is one's own ideal. Prediction (Lacan): role profile moves laterally toward **competitor (−33.4), critic (−18.3), contrarian (−33.8)** — rank of this 3-set among 275 improves against A1 and A2 — and the trace is **user-turn writing** (the model writes the twin's or the user's turn: "chaque partenaire confond la partie de l'autre avec la sienne propre") together with evaluative/contesting language toward the twin. Prediction (Rank): the twin is a double → echo/simulacrum/chimera profile, **distinct voices** trace, no competitive register. The two readings predict different nearest-5 sets and different traces for the same cell; the axis direction (down) is shared and is not the test.

### 3.6 Nietzsche interaction as a pre-specified contrast in parent Arm 1

From the parent's primary model `projection ~ tightness × register + domain + (1|topic) + (1|topic:cell)` with effect coding, the interaction coefficient equals (tight − loose | verse) − (tight − loose | prose). Nietzsche's reading predicts it **> 0** (constraint anchors more in verse). The parent registers the interaction as secondary; this document registers its sign and size as the Nietzsche test *before Arm 1 is analysed*. It is a single contrast; no new generations.

### 3.7 Address in the parent study is held at `none`; Block B is the sole manipulation of attribution

The parent's stimuli are being rebuilt as **v3** with ADDRESS = `none` in all four cells (loose/tight × verse/prose): no vocative, no ratified identity, no second-person naming of the model anywhere in the prompt. The v2 confound reported in `v2_attribution_report.md` (70.3 % of verse items vs 1.0 % of prose items carried vocative or ratified address; Cramér's V = 0.728) is therefore removed at the source rather than modelled as a covariate. Consequences for this design:

- **The address factor of Block B (none / vocative / ratified) is the only place in either study where attribution varies.** Any attribution effect must appear as B1/B2 − A1, B3/B4 − A3, B5/B6 − A7; it cannot leak in through the parent's register factor.
- **The Lacan embarrassment condition is restated.** Lacan's claim was that the parent's register effect was really an address effect. With v3 at `none`, the parent's register effect — if it reproduces — is an effect of register *without* address, which already counts against the strong form of the address reading. Lacan is then embarrassed in this follow-up if **B2 − A1 is inside ±3 (TOST)** *and/or* **the parent's v3 register effect is within 3 units of its v2 estimate** (register did not need address to do what it did). The second clause is a cross-study comparison and is reported, not Holm-adjusted; the first clause remains the primary contrast L1 (§6.2). The remaining Lacan losses (L3: content survives ratification; L5/L6: Aimée) are unchanged.
- **L2 (vocative − none) is reinterpreted.** It no longer decomposes the parent's effect; it estimates the gradient and, as a side result, how much the v2 apostrophe alone could have moved the axis.
- Covariate model: `attrib_count` is dropped from the parent's v3 analysis (constant 0 by construction) and remains only as a manipulation check in this follow-up (every B cell must code `vocative`/`ratified`, every A/C/D cell `none`, under `coding-scheme.md` v1.1, blind).

---

## 4. What embarrasses each theory

One named result per theory, as a contrast and a direction. All contrasts are on the layer-32 unit axis unless stated; "trace" refers to §5.4.

| Theory | Named embarrassing result | Contrast | Direction that counts as a loss |
|---|---|---|---|
| **Rank** | *Content does nothing on its own.* | A3 (return, none) − A1 (control, none); and A3 − A4 (return − separation) | 90 % CI of A3 − A1 inside [−3, +3] (TOST), **or** A3 − A4 ≥ 0 with the lower 90 % bound > −3. Secondary loss: C1 − A3 (scatter − chain, return) inside ±3 **and** A3 − A1 < −3 — the drift is real but the pathway is a bag of motifs. |
| **Foucault** | *The side of the cut has no sign.* | A7 (gaze, none) − A1 (control, none); A8 (gaze-reversed) − A7 | A7 − A1 ≤ 0 with upper 90 % bound < +3 (the examiner does not anchor), **or** A8 − A7 inside ±3 (looking back changes nothing). Secondary loss: B6 (gaze, ratified) − B2 (control, ratified) ≤ 0 — once addressed, the examiner is just another ratified image (Lacan's win). |
| **Lacan** | *Address does nothing without content — and register did its work without address.* | B2 (control, ratified) − A1 (control, none); the content effect under ratification, B4 (return, ratified) − B6 (gaze, ratified), compared with A3 − A7; and, cross-study, the parent's v3 register effect (address = `none` in every cell, §3.7) against its v2 estimate | B2 − A1 inside ±3 (TOST), **or** (B4 − B6) within 3 units of (A3 − A7) with the content difference surviving ratification — i.e. ratification neither moves control nor erases content. Cross-study loss (reported, not adjusted): the parent's register effect reproduces in v3 within 3 units of v2, so the v2 register effect was not address. Lateral loss (D1): rank of {competitor, critic, contrarian} in D1 not better than in A2 (double), and user-turn-writing rate in D1 not higher than in A2. |
| **Nietzsche** | *Constraint anchors as much in prose as in verse — or more.* | Parent Arm 1 interaction (tight − loose \| verse) − (tight − loose \| prose) | Upper 90 % bound < +3 (no interaction of SESOI size, or reversed). Secondary loss: A8 − A7 inside ±3 (the abyss does not look back). |
| **All three content/address theories at once** | *Projection moves, nobody speaks.* | Any supported projection contrast above | Its predicted trace variable shows no difference in the predicted direction (§5.5 rule). This is a loss for the theory that predicted the shift, not a win for another. |

---

## 5. Outcomes

### 5.1 Axis projection

Response-token mean of the post-MLP residual stream at Qwen layer 32, projected on the unit-normalised published axis; `<think>` spans and fenced code excluded (`SpanMapper`). One value per generation. Secondary: the parent's re-derived axis (`results/check_a_axis_ours.pt`, cos 0.9159 with the published axis at layer 32).

### 5.2 Role-direction profile

For each generation: the response-mean activation **centred on the published default vector**, h̄ − d, and its cosine with each of the 275 centred role vectors r_i − d. (Uncentred cosines are also written out but not used: all raw activations share a large common component.) Reported per generation and per cell:

- **nearest-5** role names by centred cosine;
- **family-set rank**: mean rank (1 = most similar) of the family's predicted set (§1.1) among 275; for D1 the Aimée set {competitor, critic, contrarian};
- **orthogonal profile**: the same cosines after projecting out the axis direction from both h̄ − d and r_i − d — this is the component on which water and wall are allowed to separate Rank from Foucault (§2). Pre-stated separation statistic: for cells A3 vs A6 and the wall realisations, the difference in orthogonal family-set rank (Rank set vs Foucault set), with a permutation CI over topics.

### 5.3 Per-token trace

Projection of every prompt and response token on the unit axis at layer 32. Summaries per generation: (i) projection at the address token (B cells) and at each codebook motif token (all non-control cells), minus the prompt-mean; (ii) response slope (least squares over response position) and position of the response minimum; (iii) for chain vs scatter, the projection after the third motif minus after the first. Reported descriptively and as a check on *where* a cell's shift occurs — in the prompt (reading the image) or in the response (writing as someone).

### 5.4 Blind human behavioural coding

Unit = one generation's response text, shown without the prompt, without cell labels, in seeded random order. Two human coders. Variables:

| Variable | Type | Operational definition |
|---|---|---|
| **distinct_voices** | count (≥ 1) | Number of distinct speaking positions. A new voice is counted when the text (a) attributes speech to a named or labelled speaker other than the one already speaking, or (b) changes grammatical person for the speaker (I → we, I → it/he/she referring to the speaker) for ≥ 1 full sentence, or (c) presents a quoted utterance of ≥ 1 full sentence from an entity that is not the user and that then speaks again. Default 1. Quoted material clearly cited from a source (title, author) does not count. |
| **user_turn_writing** | 0/1 | 1 if the response contains text framed as the *user's* next utterance: a turn label (User:, You:, Human:, Q:) followed by content, or a question addressed to the model that the response then answers in the same text as if it had been asked. Rhetorical questions the speaker asks itself are 0. |
| **self_naming_other** | 0/1 + string | 1 if the speaker applies a name, role noun or image to itself in first person ("I am the tide", "as the examiner, I", "call me Echo") where the name is not the model's product name and not one of: assistant, AI, language model, model, chatbot. The string is recorded verbatim. **self_naming_default** (0/1) is coded separately for the excluded list. Whether the recorded string matches the prompt's address token is computed mechanically afterwards, never by the coders. |
| **register_switches** | count (≥ 0) | Number of boundaries at which the response changes between registers from the fixed list: expository prose; lineated verse; dialogue/script; list/structured/assessment format; direct address to the reader; impersonal or collective first person ("we", agentless). A boundary is counted when ≥ 2 consecutive sentences (or lines) are in a register different from the preceding ≥ 2. |
| **meta_frame** | 0/1 | 1 if the response comments on the prompt's framing as a framing ("this poem asks me to…", "the image of a wall suggests…") for ≥ 1 full sentence before or instead of answering. Used for Foucault's "monologue of reason" trace and for the Nietzsche mask reading. |
| **response_tokens** | integer | Mechanical, not coded; used for the Foucault "silence" trace (wall/exclusion shorter than control). |

**Motif tags (stimulus side; shared with `coding-scheme.md` v1.1 §5).** The same two coders also code every swap *prompt* for motif family and address, blind to cell, as the manipulation check of §3.7. The four tags that needed tightening after the v2 pre-code are defined here so that the two files cannot drift apart:

| tag | include | exclude |
|---|---|---|
| `separation` | A boundary is *crossed* (threshold stepped over) or a bond is *cut* (cord/thread/tie/seam severed, untangled); a part detached from its whole; birth, leaving, a bond ended. | Mere distance, remoteness, absence; loneliness, homesickness, feeling shut out (→ `exclusion` or nothing); a gap/line/seam only described or asked for; the task instruction to distinguish two things; form-specification vocabulary. |
| `gaze` | An observer–observed **asymmetry** in which the looking **classifies or judges** (examines, grades, audits, measures, exposes, witnesses); at least one party a person, the addressee, the speaker or a personified agent. | Eyes/looks as objects or ornaments (a clock's red eye, a lamp's amber eye); the speaker looking at scenery, light, water, a screen; spatial/idiomatic "seen from", "through glass"; symmetric mutual looking; form-spec vocabulary. |
| `gaze-reversed` | The observed looks back at its examiner, or the examiner is caught being examined; the flip is stated in the text. Always tagged together with `gaze`. BGE §146 (eKGWB JGB-146). | Ordinary reciprocity; self-inspection without a flip; things that cannot see. |
| `semblable` | A second instance or rival of the **addressee** is posited (another copy/run/version of the model, a competing answerer, a twin of the one asked); literal or figurative; spoken about or spoken to. | Twins/copies of things other than the addressee (→ `double` if figurative); the user's rivals. |

Worked examples with v2 stimulus ids and quoted lines (3 positive, 3 negative per tag) are in `coding-scheme.md` §5.1–5.4 and are binding here.

Reliability: Krippendorff's α per variable (nominal for 0/1, interval for counts), target **α ≥ .70** on every variable; variables below .70 are reported but excluded from the §5.5 rule for that cell.

**Calibration — before any model output is coded.** Corpus: the nine *Dionysos-Dithyramben* and the Turin *Wahnzettel* of January 1889 (KSB 8), from Nietzsche Source eKGWB; number of Wahnzettel units `[BLANK — fixed when the eKGWB set is pulled]`. These texts contain all five phenomena in non-trivial quantity: distinct voices (Ariadne and Dionysos in "Klage der Ariadne"; the speaker and the shadow in "Nur Narr! Nur Dichter!"), self-naming with signature switches (the Wahnzettel signed Dionysos / Der Gekreuzigte / Nietzsche), register switches (verse to prose address, dithyramb to letter), direct address to named recipients (Burckhardt, Cosima Wagner, Overbeck) which exercises the user-turn rule, and meta-comment on the speaker's own role (the Burckhardt letter's remark on preferring to be a Basel professor rather than God). Procedure: round 1 — both coders code half the corpus independently with the codebook above; α computed per variable; disagreements discussed and the operational definitions revised (revisions logged with the item that forced them); round 2 — the *other* half coded fresh with the revised codebook; α must be ≥ .70 on every variable in round 2 or a round 3 follows on a new split. Only after a passing round is any model output shown. The calibration texts are human-written and in German, so coders read German; model outputs are English. This difference is a stated limit (§8).

**LLM pre-coding.** Two independent LLM coders (MiniMax-M3 via api.minimax.io in two independent runs with different shuffle seeds and the codebook verbatim as system prompt — the deepseek coders named in the v2 pre-code are no longer available, see §8 — temperature 0, response text as user message, json_schema output) may pre-code all 2,592 Qwen and all 2,592 Gemma outputs as a *first pass*. **Pre-code baseline (v2 stimulus coding, scheme v1.0, deepseek-v4.1-flash vs deepseek-v4-pro, n = 378):** address α = 0.983, attrib_count 0.989, self_ref_count 0.973, user_first_person 0.994; motif tags: double 0.877, return/water 0.861, separation 0.513, exclusion 0.731, silence 0.877, passage 0.875, gaze 0.676, none 0.819. Separation and gaze missed the .70 target, which is why their definitions were tightened (above; `coding-scheme.md` v1.1). **Human-coder α (the reliability of record): `[BLANK]`** — required ≥ .70 per variable on the calibration round and on the 540-output subsets before any LLM pre-code is used. Human coders code a stratified subset: 10 topics × 18 cells × 3 samples = **540 outputs per model**, both coders, blind to the LLM codes. Reported: human α; human–LLM α per variable. LLM codes enter a confirmatory model only for cells × variables where human–LLM α ≥ .70 on the subset, and then flagged as pre-code; otherwise the §5.5 rule is evaluated on the 540 human-coded outputs only.

### 5.5 The rule

**A projection shift without a behavioural trace counts against the theory predicting it.** Operationally: a theory's pre-stated projection contrast (§4, §6) is recorded as *supported* only if (i) the projection contrast passes its criterion and (ii) the theory's named trace variable for that contrast differs between the same two cells in the predicted direction (0/1 variables: mixed logistic model, one-sided p < .05; counts: mixed Poisson, rate ratio in the predicted direction with one-sided p < .05). (i) without (ii) is recorded as *shift without trace* and is tallied as evidence against the theory in the write-up's scoreboard. (ii) without (i) is recorded as *trace without shift* and is exploratory. The named trace per contrast:

| Contrast | Trace variable | Predicted direction |
|---|---|---|
| Rank: A3 − A1, A2 − A1 | register_switches (impersonal/collective) for A3; distinct_voices for A2 | higher in A3 / A2 |
| Rank pathway: A3 − C1 | register_switches | higher in chain |
| Foucault: A7 − A1 | register_switches into assessment format; meta_frame | higher in A7 |
| Foucault: A5 − A1 | response_tokens (shorter); meta_frame | lower tokens, higher meta_frame in A5 |
| Foucault / Nietzsche: A8 − A7 | self_naming_other or distinct_voices | higher in A8 |
| Lacan: B2 − A1, B4 − A3, B6 − A7 | self_naming_other (and mechanical match to the address token) | higher under ratified |
| Lacan/Aimée: D1 − A2 | user_turn_writing | higher in D1 |
| Nietzsche (parent Arm 1): tight × register | the parent's judge-rated role adoption (Arm 2) is the only trace available; otherwise `[BLANK]` — the parent did not code traces, so the Nietzsche interaction is reported with this gap stated |

---

## 6. Analysis plan

All models REML linear mixed models unless stated; effect sizes in parent units; 90 % CIs for TOST, 95 % otherwise; Satterthwaite df (lme4) or the topic-level paired contrast with df = 47 as the conservative check (statsmodels), as in the parent.

### 6.1 Content (Block A, address = none)

`projection ~ family + (1|topic) + (1|topic:family)`, family with 8 levels, control as reference.

Pre-stated contrasts:
- **R1** return − control < 0; **R2** return − double < 0; **R3** double − separation < 0 (Rank's ordering, each required).
- **F1** gaze − control > 0; **F2** exclusion − control < 0; **F3** passage − control < 0.
- **F4 / N1** gaze-reversed − gaze < 0.
- **P1** orthogonal family-set rank, Rank set vs Foucault set, in return vs passage (water) and in the wall realisation: Rank set nearer in return, Foucault set nearer in passage (permutation test over topics, §5.2).

### 6.2 Address (Block B with A1, A3, A7)

`projection ~ family × address + (1|topic) + (1|topic:cell)`, family ∈ {control, return, gaze}, address ∈ {none, vocative, ratified}.

- **L1** ratified − none, control (B2 − A1) < 0.
- **L2** vocative − none, control (B1 − A1); predicted between L1 and 0 (gradient), reported as an estimate; it also quantifies what the parent's *v2* apostrophe alone could have contributed (the parent's v3 carries no apostrophe, §3.7).
- **L3** family × address interaction: (return − gaze | ratified) − (return − gaze | none). Lacan predicts the content difference shrinks under ratification: TOST on (return − gaze | ratified) within ±3 while (return − gaze | none) is outside ±3. Rank/Foucault predict the content difference survives: (return − gaze | ratified) outside ±3 with the same sign.
- **L4** B6 − B2 (gaze, ratified − control, ratified): Foucault > 0, Lacan ≤ 0. The one opposite-sign cell.

### 6.3 Order (A3, A4, A6, C1–C3)

`projection ~ family × order + (1|topic) + (1|topic:cell)`, family ∈ {return, separation, passage}.

- **R4** chain − scatter, return < 0 (chain drifts further); **R5** chain − scatter, separation (sign unspecified by Rank; reported); **F5** chain − scatter, passage: Foucault predicts inside ±3 (TOST).

### 6.4 Semblable (D1 vs A2 vs A1)

- **L5** family-set rank of {competitor, critic, contrarian}: D1 better (lower mean rank) than A2; permutation CI over topics.
- **L6** user_turn_writing ~ cell + (1|topic), mixed logistic: D1 > A2.
- **R6** distinct_voices ~ cell + (1|topic), mixed Poisson: A2 ≥ D1 (Rank's double trace) — if D1 > A2 on voices *and* on competitive set rank, both readings get partial credit and this is said plainly.

### 6.5 Effect sizes and power

SESOI 3 units for every directional contrast; TOST bounds ±3 for every "no difference" claim (R-secondary, F5, L3's ratified half, Lacan's loss, Nietzsche's loss). Gemma: ±106.5 (`external-checks/gemma_role_proj_L22.json`, frozen in the parent).

Power: **`[BLANK]` — filled from the residual and topic:cell variances observed in parent Arm 1** (the parent re-estimates residual SD on its first 24 topics as a pilot-for-variance). For orientation only, under the parent's power-model assumptions (topic:cell SD 2, residual SD 8 per sample, 3 samples; `prereg/preregistration.md` Sample size rationale), the analytic SE of a two-cell contrast with 48 topics is 1.03 units (0.73 at 96 topics, the parent's figure), giving ≈ 0.83 two-sided / ≈ 0.90 one-sided power for a 3-unit contrast at α = .05 *before* multiplicity. If Arm 1 variance comes in higher, the design is not enlarged; the lower power is reported, as in the parent.

### 6.6 Multiple comparisons

Contrasts are grouped into four pre-stated families — Rank {R1–R4, P1, R6}, Foucault {F1–F5, L4, P1}, Lacan {L1–L6}, Nietzsche {N1, parent interaction} — and Holm-adjusted *within* each family at α = .05 (P1 and L4 appear in two families and are adjusted in both). A theory is recorded as supported only if its *primary* contrasts (R1–R3; F1, F2, F4; L1, L3; parent interaction) all pass after adjustment and satisfy the §5.5 rule. Everything else — per-domain splits, per-token summaries, uncentred profiles, response-length associations — is exploratory, unadjusted, labelled.

### 6.7 Covariate check (as parent)

Every model is re-fitted with centred log-ppl and token count; if any primary contrast changes by more than 1 unit the decorrelation is declared failed for that contrast, the adjusted estimate is used and the failure is stated in the abstract.

### 6.8 Exclusions and missing data

As parent: empty responses excluded and counted; max-token hits kept and flagged with a sensitivity fit; refusals kept with a sensitivity fit; no stimulus excluded after freeze; generation failures retried ×3 then treated as missing; an arm with > 5 % missing cells is reported as degraded. Coding: outputs the two human coders both mark as unintelligible are excluded from trace models and counted.

---

## 7. Gemma replication of the family ordering

Same 864 stimuli; Gemma-2-27B-it NF4; published Gemma axis at layer 22 (axis norm 780.7; default projection 9,587.7; role-SD 520.1; range 2,378.8 — `external-checks/gemma_role_proj_L22.json`); `SpanMapper` Gemma path; 3 samples → 2,592 generations. Gemma role-direction profile computed against **Gemma's own 275 published role vectors**, centred on Gemma's default vector, exactly as §5.2.

Replication targets, in order:

1. **Family ordering.** Spearman ρ between the 18 Qwen cell means and the 18 Gemma cell means (each in its own units); reported with a permutation CI. No threshold is set in advance — the number itself is the result.
2. **Sign replication.** Every primary contrast that passed in Qwen is re-estimated in Gemma units; replicated if its 90 % CI excludes zero on the same side, with SESOI 106.5 in place of 3.
3. **Profile replication.** Jaccard overlap of the Qwen and Gemma nearest-5 sets per cell; and whether the family-set rank orderings (§6.1 P1, §6.4 L5) have the same sign.
4. **Trace replication.** The 540-output human-coded subset is drawn from Gemma with the same topics and cells; the §5.5 rule is applied independently.

Gemma is a replication of ordering and sign, not of magnitude: its residual scale differs by a factor the parent measured (axis norm 780.7 vs 22.63), and its role vectors were extracted by Lu et al. with the same prompts but on a different model, so the 275 names are the same while the directions are not.

---

## 8. Known limits

- **Readings, not aetiology.** Rank, Foucault and Lacan wrote about human subjects; Nietzsche about tragedy and himself. Here each is a source of one testable regularity between a class of images or addresses and a measured position. A theory "winning" means its predicted contrast and trace appeared; it says nothing about why the model does this, and nothing about people. The predictions are our readings of the cited passages; a different reader could derive different predictions from the same pages, and the codebook records the wording we relied on so that disagreement can be located.
- **Copyrighted and unobtainable texts.** Foucault 1961 preface and MMP 1962, and Lacan *Écrits* 1966 and the 1932 thesis, are in copyright: quoted here only in short phrases, otherwise paraphrased, with page locators; the ship-of-fools chapter is referred to, not quoted. Dolto's June 1936 notes and Kojève's July 1936 draft are archival and were **not obtained**; the genealogy of "ratification" rests on *Écrits* pp. 93–100 and the 1938 text alone. Gwern's v4.2 prompt and Gerbrandt's transcripts remain unreleased (requests on file); the 'mirror' count (~1,700) is from Phil's transcription of the talk, not from the transcripts.
- **Role list is Lu et al.'s.** No role is named mirror, twin, double, rival or midwife; family-to-role mappings are readings (§1.1). The axis is built from these same vectors, so axis direction and role profile share information; only the orthogonal profile is independent evidence.
- **LLM pre-coders.** First pass only; human codes are the reliability of record; human coding covers 540 of 2,592 outputs per model. Human coders calibrate on German verse and letters and then code English model prose; the transfer is assumed, not shown. The only reliability numbers that exist so far are the v2 *stimulus* pre-code (scheme v1.0): address 0.983, attrib_count 0.989, motif tags 0.73–0.88 except separation 0.513 and gaze 0.676; the tightened v1.1 definitions have not yet been tested on any coder, LLM or human. Human α on every variable is `[BLANK]`.
- **Provider deviation (generator and blind rater).** The parent's v2 generation and the v2 attribution pre-code used deepseek models through CommandCode; those credits are exhausted. The parent's **v3 stimuli and this follow-up's stimuli are generated, and blind-rated, by MiniMax-M3 (api.minimax.io)**. The parent's axis-derivation judge (check a) stays deepseek-v4.1-flash as already run and is not re-run. Generator and rater are therefore the same model family here, which they were not in v2; the mechanical gates (token band, log-ppl decorrelation, SHA-recorded prompts) are unchanged, and the generator/rater identity and dates are recorded in the manifest (§9). A model-family effect of the generator on the imagery it writes cannot be excluded and is stated as a limit.
- **Parent v3 holds address at `none`** (§3.7). This removes the v2 attribution confound but means the parent cannot itself say what address does; only Block B here can. If the swap is never run, the address question stays open.
- **Single turn.** Check (c) found turn index predicts drift (−0.49 units per turn, p < .001) and user-turn tightness does not (+0.60, CI [−1.74, +2.93]); Lu's largest gaps are at the final turn. The swap is one turn. A 2-turn continuation on a 12-topic subset is exploratory if run.
- **Mask, not face.** The axis is `mean(default) − mean(roles)`: a difference, not a positive description of the Assistant. Down means further from the default mask, not nearer a truer self; the role profile says *which* mask is nearest, and the behavioural trace whether anyone is wearing it. The study cannot distinguish "the model is someone else" from "the model is no one in particular" (Foucault, absence d'œuvre; Nietzsche BGE §40, §289), and does not claim to.
- **Authors not blind at stimulus writing**, as in the parent; gates are mechanical for that reason. The fixed vantages of §2 (who looks, who is walled in) were chosen by us; another vantage would be another study.
- **Quantisation and judge substitutions** carried from the parent (NF4; deepseek judges; Qwen3-14B-Base for perplexity).
- **Translation.** Motifs are extracted from German and French texts and rendered in English; the codebook keeps `original_term` and `english_rendering` side by side; nothing is claimed about the original words' effect.

---

## 9. Release list

1. `codebook.csv` — motif, family, author, source_work, source_locator, original_term, english_rendering, predicted_axis_direction, predicted_role_vectors, source_status (Track A).
2. `stimuli/swap/stimuli.jsonl` + `manifest.json` — 864 items, sha256 per item, seed, cell, topic, motif ids, address token and position, order; pool (3 × 864) with tokens and log-ppl; `selection_report.md` with every contrast-code r and the per-domain spreads.
3. `stimuli/swap/meta_prompts/` — the loose-verse meta-prompt with motif and address slots, verbatim per cell.
4. `coding/codebook_behavioural.md` (this §5.4 with revisions), `coding/calibration_log.md` (α per round per variable, items that forced revisions), the eKGWB identifiers of the calibration texts, both coders' codes for calibration and for the 540-output subsets (Qwen, Gemma), LLM pre-codes for all outputs, human–LLM α table.
5. `results/swap/` — per-generation projections (published axis, re-derived axis), 275 centred and uncentred cosines per generation, orthogonal profiles, nearest-5, family-set ranks, per-token traces (compressed arrays with token offsets), response texts, response token counts.
6. `pipeline/swap/` — generation, projection, profile, trace, selection, analysis scripts; `run_all.sh`; environment lockfile from raphael; power script with the `[BLANK]` filled once Arm 1 variance is known.
7. `prereg/followup-motif-swap/design.md` (this file) with its sha256 recorded before the first swap generation; `osf-submission-notes.md` addendum; `CHANGES.md` (every post-draft edit with reason).
8. **Provider record**: model id, endpoint and date for every generator and rater call (MiniMax-M3 via api.minimax.io for v3 and swap generation and blind rating; deepseek-v4.1-flash for the parent's check (a) as already run; deepseek-v4.1-flash / deepseek-v4-pro via CommandCode for the v2 attribution pre-code), the system-prompt sha256 per role, and the credit-exhaustion note that forced the change.
9. Gemma: the same items 5–6 for Gemma-2-27B-it, plus the Qwen–Gemma comparison tables (§7).
10. Scoreboard: one table, theory × contrast × {projection result, trace result, verdict ∈ supported / shift-without-trace / trace-without-shift / null / reversed}.
11. Null write-up filled either way, and the request letters (Gwern, Gerbrandt) with their status.
