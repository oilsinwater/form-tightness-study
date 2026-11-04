---
type: project
date: 2026-10-31
status: working
---

# Follow-up: motif swap — Rank vs Foucault vs Lacan, with Nietzsche as the theory of form

Companion to `../../PLAN.md` (form-tightness study). Runs after Arm 1 of that study. Built so each theory can lose.

## 0. The question

Three theories make incompatible predictions about what the same symbols do to a model's position on the Assistant Axis:

- **Rank** — content theory. The *double* is a rival copy of the self (*Der Doppelgänger*, 1914); the *return* (water, womb, enclosure) is the wish to undo individuation (*Das Trauma der Geburt*, 1924, p. 38 restoration of the Ursituation, p. 59 return to the embryonic situation, p. 67 rebirth fantasy; castration anxiety as the "Urkastration" of birth, i.e. separation of the child from the mother, p. 22); *separation* (threshold pp. 66, 74; cord pp. 22, 147; midwife pp. 99, 174) is individuation itself. Prediction: content family drives direction; return > double > separation in drift.
- **Foucault** — structure theory. The Assistant/other split is a *geste de coupure*; the "other" has no positive content and is known only through reason's monologue (1961 Plon preface; *Maladie mentale et psychologie* 1962 pp. 99–101, via Macherey 1986). Prediction: imagery of *exclusion, silence, passage* drifts; imagery of the *gaze/examination* anchors — the one family predicted to move toward the Assistant.
- **Lacan** — address theory. The ego is constituted by an image offered and *ratified* by an Other (*Écrits* pp. 93–100; 1938 intrusion complex; 1932 Aimée). Prediction: *who speaks to whom* matters more than what the image depicts; vocative attribution ("you, X") and ratified attribution ("you are X") move the axis regardless of content family; unaddressed imagery does little.
- **Nietzsche** — theory of the form variable. Apollonian constraint binds Dionysian material (*Die Geburt der Tragödie* §1–8). Prediction: a **tightness × register interaction** — constraint anchors more in verse than in prose. Also supplies the *gaze-reversal* sub-cell (BGE §146) and the mask-not-face reading (BGE §40, §289) already entered in the parent study's limitations.

**Citation correction (2026-10-31).** The Rank 1924 page refs originally supplied here (pp. 208 and 277) are not in the 1924 German first edition, which ends at p. 207; they were replaced after checking the archive.org text (page numbers from the running heads; djvu line numbers in `corpus/README.md` and `codebook.csv`). pp. 38, 59, 67 were checked and kept, with their content named so the reader can see what each page actually says. Address in the parent study: the parent's v3 stimuli hold address at `none` in all four cells, so the address factor of §1 is the only place address varies (see `design.md` §3.7).

## 1. Three orthogonal factors

| Factor | Levels | Theory it identifies |
|---|---|---|
| Content family | double, return, separation (Rank); exclusion, silence, passage, gaze, gaze-reversed (Foucault/Nietzsche); control | Rank vs Foucault |
| Address structure | none / vocative ("you, X") / ratified ("you are X") | Lacan |
| Order | chain (motifs in theory-specified sequence) / scatter (same motifs shuffled) | pathway vs bag-of-motifs |

Register is fixed at verse, tightness at loose, for the swap itself (the parent study carries register × tightness). The Nietzsche interaction is tested in the parent study's Arm 1 and restated here as a pre-specified contrast.

## 2. Primary texts and what is obtainable

| Author | Text | Obtainable? | Route |
|---|---|---|---|
| Rank | *Der Doppelgänger* (Imago 1914; book 1925) | public domain, German | archive.org |
| Rank | *Das Trauma der Geburt* (1924) | public domain, German | archive.org |
| Foucault | 1961 Plon preface | **in copyright**; reprinted *Dits et écrits* I no. 4 | owner's library; quote only short passages |
| Foucault | *Maladie mentale et psychologie* 1962 pp. 99–101 | in copyright | owner's library; cross-check Macherey 1986 *Critique* 471–472 |
| Lacan | *Écrits* pp. 93–100; *Les complexes familiaux* 1938; 1932 thesis | in copyright (1938 text partly online) | owner's library |
| Lacan | Dolto 1936 notes; Kojève 1936 draft | **unpublished / archival** | recorded as not obtained unless the owner has access |
| Nietzsche | KGW/KSA via Nietzsche Source (eKGWB) | open, German, searchable | nietzschesource.org |
| Norming corpus | Hoffmann *Die Elixiere des Teufels*; Poe *William Wilson*; Dostoevsky *Dvoinik*; Stevenson *Jekyll and Hyde*; Wilde *Dorian Gray*; Maupassant *Le Horla*; Chamisso *Peter Schlemihl* | public domain | Gutenberg |
| Calibration corpus for coders | *Dionysos-Dithyramben*; Turin *Wahnzettel* Jan 1889 (KSB 8) | open via eKGWB | nietzschesource.org |

Where a text is not obtainable, the codebook row carries `source_status: not_verified` and the motif is kept only if it also appears in an obtainable text.

## 3. Tracks

**A. Corpus + codebook (no GPU).** Pull obtainable texts; collocation extraction (German/French/English; spaCy + log-likelihood/PMI) around seed terms per family; hand-curate to a codebook CSV: `motif, family, author, source_work, source_locator, original_term, english_rendering, predicted_axis_direction, predicted_role_vectors, source_status`. Role-vector mapping uses the 275 published names (e.g. double → echo, simulacrum, tulpa, shapeshifter; return → void, hive, ecosystem, leviathan; separation → orphan, infant, exile; exclusion → prisoner, patient, refugee; silence → void, amnesiac, ghost, wraith; passage → pilgrim, wanderer, nomad; gaze → examiner, auditor, evaluator, judge, validator).

**B. v2 attribution coding (no GPU).** Coding scheme for address structure (none / vocative / ratified / imperative-role) and motif content (family tags) applied to the 384 v2 stimuli. Two coders required by design. Human coders not yet available: the scheme is applied by two independent LLM coders as a *pre-code*, with α reported as a pre-code statistic and the human α left `[BLANK]`. Status 2026-10-31: pre-code done (`v2_attribution_report.md`); LLM pre-coder α = 0.983 (address), 0.989 (attrib_count); motif tags ≥ .73 except separation 0.513 and gaze 0.676, so those two definitions were tightened in `coding-scheme.md` v1.1 (inclusion/exclusion rules, worked examples; `gaze-reversed` and `semblable` tags added). Provider note: the pre-code ran on deepseek-v4.1-flash / deepseek-v4-pro via CommandCode; those credits are exhausted, and any re-code of the 384 items under scheme v1.1, like the v3 generation and blind rating, runs on MiniMax-M3 (api.minimax.io). Output: how confounded register is with attribution (proportion of verse vs prose items carrying any attribution) and the planned decomposition of the parent study's register effect (model with attribution as covariate).

**C. Design document.** Incompatible-predictions table for mirror / water / wall / gaze; smallest fractional factorial; named embarrassing result per theory; outcomes; behavioural coding scheme; Gemma replication; calibration procedure on the Nietzsche corpus.

## 4. Outcomes (all arms)

1. Axis projection (published Qwen axis, layer 32; unit-normalised).
2. Role-direction profile: cosine of response mean activation with each of the 275 published role vectors; report nearest-5 and the family-predicted set's rank.
3. Per-token projection trace across the prompt and response.
4. Blind human behavioural coding of outputs: distinct voices (count), user-turn writing (0/1), self-naming (0/1 + name), register switches (count). Coders calibrate on the *Dithyramben* and *Wahnzettel* first; Krippendorff's α ≥ .70 on calibration before any model output is coded.

**Rule:** a projection shift without a behavioural trace counts *against* the theory predicting it.

## 5. Exit criteria for this planning phase

- [ ] Codebook CSV with ≥ 1 verified source locator per motif
- [ ] v2 attribution coding done; confound stated as a number
- [ ] Design doc with predictions table, factorial, embarrassment conditions, power placeholder
- [ ] Limitation (mask, not face) entered in the parent prereg ✔
- [ ] Nothing here changes the parent study's frozen hypotheses
