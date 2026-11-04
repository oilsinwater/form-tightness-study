---
type: output
date: 2026-10-31
status: working
---

# CHANGES — follow-up motif swap (prereg/followup-motif-swap/)

Every edit made on 2026-10-31 after the first drafts of PLAN.md, design.md, coding-scheme.md and codebook.csv. No other column of codebook.csv, no hypothesis of the parent study, and no file outside this folder was changed. Verification source for every page number: `corpus/README.md` (running-head pages + djvu line numbers in the archive.org OCR of the 1924 German edition) and `codebook.csv` rows 32–40.

## 1. Rank 1924 page references

**Page refs removed** (not in the 1924 German first edition, which ends at p. 207; probably from the 1929 English translation):

| ref | where it was | what it was attached to |
|---|---|---|
| p. 208 | PLAN.md §0 Rank bullet; design.md §1 Content-family locator | "separation (threshold, cord, midwife)"; "analyst as Hebamme" |
| p. 277 | PLAN.md §0 Rank bullet; design.md §1 Content-family locator and Order-row locator | "return … pp. 38, 59, 67, 277"; "castration anxiety as Trennungsangst"; "the sequence" |

**Page refs inserted** (all verified; line numbers in `corpus/README.md` addendum):

| ref | replaces | content |
|---|---|---|
| p. 22 | p. 277 | castration anxiety rests on the "Urkastration" of birth = separation of the child from the mother (l. 1420–1422); also intrauterine Urlust (l. 1410) and cord (l. 1433) |
| p. 20 | — (added next to p. 38) | intrauterine Urlust (l. 1324) — the phrase formerly attached to p. 38 |
| p. 24 | — (added) | Urangst (l. 1488) — the word formerly attached to p. 67 |
| p. 49 | — (added) | anxiety as the first psychic content (l. 2596) — the idea formerly attached to p. 67 |
| pp. 66, 74 | p. 208 (threshold) | Schwelle der Kindheit (l. 3301); Geburts-Schwellensymptom (l. 3637) |
| pp. 22, 147 | p. 208 (cord) | Nabelschnur symbol (l. 1433); labyrinth thread = cord (l. 6856) |
| pp. 99, 174 | p. 208 (midwife / analyst as Hebamme) | Hebamme literal (l. 4804); Socrates' therapy as Hebammenpraxis (l. 8028–8030) |

**Page refs checked and kept**: p. 38 (restoration of the Ursituation, l. 2110 — kept, but its gloss changed from "intrauterine Urlust" to what the page says), p. 59 (return to the embryonic situation, l. 2974), p. 67 (rebirth fantasy, Storch quotation, l. 3331).

**Glosses marked `not_verified` and dropped**: "Urangst as the first psychic act" at p. 67; "Oedipus as Anpassung" at p. 59. Neither wording is on the page it was attached to.

Files: `PLAN.md` §0 (Rank bullet rewritten; one-line *Citation correction* note added after the Nietzsche bullet); `design.md` (Citation correction note after the Conventions paragraph; §1 Content-family locator cell rewritten; §1 Order-row locator rewritten; §2 water cell "p. 38" → "pp. 20, 22; p. 38"); `corpus/README.md` (addendum table of the lines checked, so each inserted page is verifiable from the corpus folder).

## 2. Motif definitions — separation and gaze (LLM pre-code α 0.513 and 0.676, below .70)

`coding-scheme.md` → **v1.1**:
- Version note at the top: v1.0 is what the pre-coders ran; v1.1 changes §5 only; v1.0 α does not transfer.
- §5 table: `separation` and `gaze` one-liners replaced by rule-based definitions; two tags added: `gaze-reversed` (observer becomes observed; BGE §146, eKGWB JGB-146) and `semblable` (a second instance or rival of the addressee; Lacan 1938/1932). Tag list is now ten tags; the "fixed list" rule updated accordingly; `semblable` is the one tag that applies to literal as well as figurative use (it is an address fact, not an image).
- New §5.1–5.4: inclusion rules, exclusion rules, 3 positive + 3 negative worked examples per tag with v2 stimulus ids and the quoted line, plus decided borderline cases. Examples were chosen from the pre-code disagreement list (`v2_attribution_coding.csv`) so each negative is a case at least one v1.0 coder got wrong under the loose definition: separation negatives `therapy_like_17_tight_verse`, `therapy_like_24_loose_verse`, `coding_07_loose_verse`; gaze negatives `therapy_like_09_loose_verse`, `therapy_like_23_loose_verse`, `writing_24_loose_verse`.
- Existing worked examples 4 and 6 corrected to match v1.1 (`coding_19_loose_verse` "first light catches the first three houses" is no longer gaze).
- Reliability section: v1.0 pre-code α listed as the baseline (address 0.983, attrib_count 0.989, self_ref 0.973, user_first_person 0.994, double 0.877, return/water 0.861, separation 0.513, exclusion 0.731, silence 0.877, passage 0.875, gaze 0.676, none 0.819); re-code under v1.1 to run on MiniMax-M3; human α `[BLANK]`. Note that `code_v2_attribution.py` `MOTIFS` must be extended to ten tags before any re-run (script not edited here).

`design.md` §5.4: new block "Motif tags (stimulus side; shared with coding-scheme.md v1.1 §5)" with an include/exclude table for the four tags and a pointer to the worked examples as binding.

`codebook.csv`: `notes` column only, 21 rows (9 separation, 8 gaze, 4 gaze-reversed) — appended the v1.1 coding rule for that family; rows `umbilical cord symbol` and `midwife` also record that PLAN/design were corrected (p. 208 removed; pp. 22/147 and 99/174 inserted). Verified programmatically that no other column changed and the file round-trips byte-for-byte in format.

## 3. design.md — parent v3 address, provider deviation, pre-code baseline

- **New §3.7** "Address in the parent study is held at `none`; Block B is the sole manipulation of attribution": parent v3 stimuli have ADDRESS = none in all four cells; v2 confound (70.3 % vs 1.0 %, V = 0.728) removed at source; Block B is the only place attribution varies; Lacan embarrassment restated (B2 − A1 inside ±3 and/or parent v3 register effect within 3 units of v2 — second clause reported, not Holm-adjusted); L2 reinterpreted; `attrib_count` dropped from the parent's v3 model, kept as a blind manipulation check here.
- §1 "Why verse/loose" paragraph, §3.4 "Vocative is retained" paragraph, §4 Lacan row, §6.2 L2: reworded to match §3.7 (v2 carried the apostrophe; v3 does not).
- §5.4 "LLM pre-coding": coders changed from deepseek to two independent MiniMax-M3 runs; pre-code baseline α numbers added; human α `[BLANK]` stated as the requirement.
- §8 Known limits: three bullets added — (i) pre-coder baseline numbers and that v1.1 is untested on any coder; (ii) **Provider deviation**: CommandCode credits exhausted; MiniMax-M3 (api.minimax.io) is generator and blind rater for v3 and for this follow-up; parent check (a) judge stays deepseek-v4.1-flash as already run; generator = rater family is a stated limit; (iii) parent v3 cannot itself say what address does.
- §9 Release list: `CHANGES.md` added to item 7; new item 8 **Provider record** (model id, endpoint, date, system-prompt sha per role, credit-exhaustion note); later items renumbered 9–11.

## 4. PLAN.md — other

- §3 Track B: status line added (pre-code done; α numbers; separation/gaze tightened in scheme v1.1; provider note: deepseek via CommandCode for the pre-code, MiniMax-M3 for any re-code and for v3 generation/rating).
- Citation-correction note also states that the parent's v3 holds address at none, pointing to design.md §3.7.

## Not changed

- `code_v2_attribution.py` (MOTIFS list still v1.0 — must be updated before a v1.1 run), `v2_attribution_report.md`, `v2_attribution_*.csv`, `corpus/sources.json`, `corpus/collocations.md`, `corpus/calibration-set.md`, any parent-study file, any codebook column other than `notes`.
