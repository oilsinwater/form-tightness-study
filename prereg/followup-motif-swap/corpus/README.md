---
type: project
date: 2026-10-31
status: working
---

# Track A corpus — method, measures, what failed

Companion to `../PLAN.md` §2–3. Everything here was produced on 2026-10-31 without a GPU and without spaCy.

## Where the texts are

Downloaded texts are **not** in the vault. They live at:

```
~/.hermes/cache/scratch/motif-corpus/
  *.txt                        Gutenberg / archive.org plain text (one file per source)
  manifest.json                URL, bytes, sha256 per file
  nietzsche/<BOOK>.html        raw eKGWB book HTML from the AJAX endpoint
  nietzsche/<BOOK>.json        {eKGWB id: plain text} per section
  nietzsche/<BOOK>.txt         same, concatenated with [id] headers
  nietzsche/manifest.json
  colloc/collocations.json     full collocation tables (top 25 per text × family)
```

Scripts (also outside the vault): `~/.hermes/cache/scratch/motif_fetch.py`, `motif_nietzsche.py`, `motif_colloc.py`, `motif_outputs.py`, `motif_codebook.py`, `rank_pages.py`. That cache directory is pruned after 24 h idle — re-run `motif_fetch.py` and `motif_nietzsche.py` to rebuild; `sources.json` has the exact URLs and hashes to check against.

## Obtainability table — outcome

| PLAN row | Outcome |
|---|---|
| Rank, *Der Doppelgänger* 1925 | **obtained** — archive.org `Rank_1925_Doppelgaenger_k`, OCR djvu.txt, 36,684 tokens |
| Rank, *Das Trauma der Geburt* 1924 | **obtained** — archive.org `DasTraumaDerGeburtUndSeineBedeutungFrDiePsychoanalyse`, OCR, 63,675 tokens |
| Foucault 1961 preface; *Maladie mentale* 1962; Macherey 1986 | **not obtained** (copyright; not attempted by instruction). Only the short quotes in PLAN.md are used (`verified_quote`). |
| Lacan *Écrits* 93–100; 1938; 1932 thesis | **not obtained** (copyright; not attempted). PLAN quotes only. |
| Dolto 1936 notes; Kojève 1936 draft | **not obtained** (archival). Zero rows depend on them. |
| Nietzsche eKGWB | **obtained** — GT, JGB, Za-IV, FW, DD, BVN-1889 (see "Nietzsche Source" below) |
| Hoffmann, Chamisso, Maupassant, Stevenson, Wilde, Poe | **obtained** from Gutenberg; ids verified by fetching each file's `Title:`/`Author:` header: #76360, #31538, #10775, #43, #174, #2148 (Poe *Works* vol. 2, *William Wilson* sliced out) |
| Dostoevsky *The Double* (Garnett) | **substituted** — not on Project Gutenberg (site search: "No records found"). Used archive.org OCR of *The Eternal Husband and Other Stories* (Macmillan 1917, Garnett), item `eternalhusbandot00dost_3`, lines 9693–19785 |
| *Dionysos-Dithyramben*; Jan-1889 *Wahnzettel* | **obtained** — eKGWB DD (9 poems, 18 section ids) and BVN-1889 nos. 1232–1256 (27 letters incl. 1242a, 1255a) |

Counts: 14 obtained + 1 substituted = **15 texts with content**; 8 not obtained. Total tokens across the 15 texts used for collocations: 613,511.

| text | lang | tokens |
|---|---|---:|
| rank_doppelgaenger_1925 | de | 36,684 |
| rank_trauma_1924 | de | 63,675 |
| hoffmann_elixiere | de | 107,131 |
| chamisso_schlemihl | de | 21,563 |
| maupassant_horla (whole 1887 collection) | fr | 41,210 |
| stevenson_jekyll_hyde | en | 25,704 |
| wilde_dorian_gray | en | 79,179 |
| poe_william_wilson | en | 8,022 |
| dostoevsky_double_garnett_1917 | en | 63,774 |
| nietzsche_GT §1–8 | de | 11,492 |
| nietzsche_JGB (numbered aphorisms) | de | 55,983 |
| nietzsche_Za-IV | de | 23,997 |
| nietzsche_FW (numbered aphorisms) | de | 69,809 |
| nietzsche_DD | de | 3,571 |
| nietzsche_BVN-1889 | de | 1,717 |

## Nietzsche Source: how the text was actually fetched

`http://www.nietzschesource.org/#eKGWB/JGB-40` is a hash route handled by JavaScript; the server returns the same shell page for every id, and `/texts/eKGWB/...` is 404. The application loads one book at a time from

```
https://www.nietzschesource.org/resources/scripts/static_html_include.php?book=%23eKGWB%2F<BOOK>
```

(`<BOOK>` = GT, JGB, Za-IV, FW, DD, BVN-1889). That HTML contains `<a name="eKGWB/<id>">` anchors; `motif_nietzsche.py` splits on them and URL-decodes the ids. Each aphorism appears under two ids (e.g. `JGB-40` empty anchor and `JGB-II-40` with the text); the codebook uses the short canonical form (`JGB-40`) which is what the public URL takes. No substitution (Gutenberg/zeno) was needed.

## Collocation method

- Tokeniser: regex `[^\W\d_]+(?:['’-][^\W\d_]+)*`, lower-cased, no lemmatisation. Gutenberg header/footer stripped between the `*** START` / `*** END` markers; archive.org OCR used whole (library stamps and running heads included — noted below).
- Seeds: one prefix regex per family per language (listed at the top of each block in `collocations.md`). Prefix matching stands in for lemmatisation (`spiegel` → *Spiegel, Spiegelbild, spiegelte*).
- Window: ±5 tokens around every seed hit; seed tokens themselves excluded from the window counts.
- Measure: Dunning log-likelihood G² on the 2×2 table (word in window / word elsewhere × window tokens / other tokens), sign-flipped if the word is under-represented near seeds. Ranked by G², ties broken by raw count; min window count 2, min length 3, stop-lists per language. Raw window count and whole-text frequency are reported next to G² so the reader can re-rank by PMI or raw count.
- Families × texts: Rank texts get the Rank families (+ gaze/silence as a check); Nietzsche texts get gaze/double/silence/passage/exclusion (+ the Apollonian/Dionysian form vocabulary on GT §1–8); each norming text gets all seven content families.
- Output: `collocations.md` (top 25 per block) and `colloc/collocations.json` (same, machine-readable).

What this does *not* do: no POS filtering, so verbs and adjectives from the surrounding narration appear (e.g. *opened, locked, fixed*); for the purpose here — finding which concrete images a family actually co-occurs with — that was useful rather than noise (the door vocabulary under "separation/passage" in the English novels is a real finding). No sentence boundaries: a ±5 window can cross a full stop.

## Codebook

`../codebook.csv`, 118 rows, columns exactly as specified. Rows per family: double 38, return 18, form 14 (Nietzsche GT §1–8 form vocabulary — not a content family, kept separate), exclusion 11, separation 9, silence 8, gaze 8, passage 8, gaze-reversed 4. Rows per `source_status`: verified_text 108, verified_quote 10, not_verified 0. Rows per author: Nietzsche 48, Rank 39, Foucault 6, Lacan 4, norming authors 21.

- Every row has a locator a reader can open: an eKGWB id with its URL; a Gutenberg id + chapter + line number in the `pg<id>.txt` file; or an archive.org item + chapter + page (from the running head) + line number in the `_djvu.txt`. For the Rank *Doppelgänger* OCR only odd-page running heads survived, so pages are given as `p.~NN` (floor) with the djvu line.
- `predicted_role_vectors` were validated against the 275 names in `external-checks/qwen_role_proj_L32.json` (script asserts membership; a few of my draft glosses like "outcast" were dropped because they are not in the list).
- Foucault and Lacan rows (10) use only the phrases quoted in PLAN.md and are marked `verified_quote`; each such row's `notes` names the obtainable-text counterpart that justifies keeping it. No row is `not_verified`, because the two archival sources (Dolto, Kojève) contribute nothing quotable.
- Direction coding follows the theory that owns the family: Rank families → down (separation least); Foucault exclusion/silence/passage → down, gaze → up; gaze-reversed (JGB-146, FW-125 "durchbohrte sie mit seinen Blicken", Hoffmann's staring double) → down; form rows → Apollonian terms up, Dionysian terms down, pairs lateral/none. Contested images (cave, threshold, wall, sea) are flagged in `notes`.
- The JGB-146 gaze-reversal rows and the Za-IV *Der Schatten* shadow-as-voice rows (12 rows, including the verbatim vocative "oh Zarathustra, ich, dein Schatten!" and the ratified "Du bist mein Schatten!") are present as requested.

## What failed or deviates from the PLAN

1. **PLAN page numbers for Rank 1924 (pp. 38, 59, 67, 208, 277).** The German 1924 edition runs to ~p. 207 (last running head p. 207, "Die therapeutische Wirkung"). pp. 59 and 67 are confirmed in the neurotic-reproduction chapter; p. 38 is in the sexual-satisfaction chapter (return via coitus); **p. 208 and p. 277 do not exist in this edition** — they are probably from the English translation (*The Trauma of Birth*, 1929). The cord/midwife/threshold material is at pp. 22, 66, 74, 93, 99, 147, 174 and the codebook points there.
2. **Dostoevsky *The Double* is not on Project Gutenberg.** Substituted with archive.org OCR of the 1917 Garnett volume (same translation). The OCR has running-head noise ("THE DOUBLE 139") and junk tokens (*eee, eae*) that reach the collocate tables; I left them in rather than hand-clean.
3. **Rank OCR page mapping** is approximate for *Der Doppelgänger* (odd pages only) and breaks in the front/back matter; locators carry the djvu line as the reliable key.
4. **`gutendex.com`** timed out / returned non-JSON; ids were verified instead by fetching `gutenberg.org/cache/epub/<id>/pg<id>.txt` and reading the header.
5. **Python `urllib` could not verify TLS** on this machine (missing CA bundle) — all downloads were made with `curl` via subprocess. Hashes in `sources.json` are of the bytes curl returned.
6. **Le Horla** Gutenberg #10775 is the whole 1887 collection (Le Horla + 13 other stories), not the single story; token counts and collocates are for the collection. The codebook locators point into the diary-dated Horla section (lines 48–1047).
7. **spaCy not installed**, as anticipated; no lemmatisation or POS tags. Prefix regexes were used instead.
8. The Foucault families have **no Foucault-text collocates** (texts not obtainable); their seed vocabulary was run on Nietzsche and the norming corpus instead, and the section header in `collocations.md` says so.

## Files written in this directory

- `sources.json` — 23 entries (15 with bytes/sha256, 8 not_obtained with reason)
- `collocations.md` — seeds + top-25 collocates per text × family; norming corpus in its own section
- `calibration-set.md` — Dithyramben ids and Wahnzettel KSB 8 numbers with calibration notes
- `README.md` — this file
- `../codebook.csv` — 118 rows

## Addendum 2026-10-31 — Rank 1924 locators inserted into PLAN.md / design.md

Checked again against `rank_trauma_1924.txt` (page = running head; l. = djvu line) when the pp. 208/277 refs were replaced. These are the pages now cited in `PLAN.md` §0 and `design.md` §1–2:

| claim in PLAN/design | page | djvu line | wording |
|---|---:|---:|---|
| intrauterine Urlust | 20, 22 | 1324, 1410 | "der intrauterinen Urlust tendiert" |
| restoration of the Ursituation (the former "p. 38") | 38 | 2110 | "Versuch zur Wiederherstellung der Ursituation" (ch. Die sexuelle Befriedigung) |
| castration anxiety = separation from the mother (the former "p. 277") | 22 | 1420–1422 | "basiert die Bedeutung der Kastrationsangst … auf der ‚Urkastration' der Geburt, d. h. der Trennung des Kindes von der Mutter" |
| anxiety as the first psychic content (gloss formerly attached to p. 67) | 49 | 2596 | "die Angst …, die sozusagen der erste psychische Inhalt ist" |
| Urangst | 24 | 1488 | codebook row `primal anxiety` |
| return to the embryonic situation | 59 | 2974 | codebook row `embryonal situation` |
| rebirth fantasy (Storch) | 67 | 3331 | codebook row `rebirth fantasy` |
| midwife, literal | 99 | 4804 | codebook row `midwife` |
| therapy as midwifery (the former "p. 208 analyst as Hebamme") | 174 | 8028–8030 | "dialektische Therapie des Herausziehens der Gedanken der Hebammenpraxis gleichgestellt" (Socrates) |
| threshold | 66, 74 | 3301, 3637 | codebook row `threshold of childhood` |
| cord | 22, 147 | 1433, 6856 | codebook rows `umbilical cord symbol`, `labyrinth and thread` |

Not found and dropped from design.md: "Urangst as the first psychic act" **at p. 67** (p. 67 is the Storch rebirth material) and "Oedipus as Anpassung" **at p. 59** (p. 59 is the Embryonalsituation passage; no Ödipus/Anpassung collocation on that page). Both are marked `not_verified` in design.md §1.
