# Amendments — post-freeze record

`freeze.txt` records the sha256 of every commitment file as of
`2026-10-31T16:30:22-07:00`. Arms 1–3 ran **after** that freeze (first analysis
output `2026-10-31 21:57`, reports `2026-11-01`). No frozen file has been edited
since; every hash in `freeze.txt` still verifies against the file on disk.

Anything below is a deviation from the frozen text. It is recorded here rather
than by editing the frozen documents, so that a third party can still verify
that the hypotheses, gates, bounds and analysis plan are the ones frozen before
the data existed.

---

## 1. 2026-11-04 — source requests to Gwern and Gerbrandt withdrawn (post-data)

**What changed.** Two drafted, never-sent outreach letters were deleted:
`external-checks/requests/gwern-request.md` and `gerbrandt-request.md`. Neither
source is public: Gwern's "pressure-cooker" v4.2 prompt is unpublished, and
Gerbrandt's poem and transcripts were not released. The study cites both as
unpublished and no request will be made.

**Where the frozen text disagrees.** Two sentences still describe the requests
as drafted, and now point at files that no longer exist:

- `prereg/preregistration.md` §Limitations stated up front, the Gwern and
  Gerbrandt bullets ("A request for the verbatim text is drafted …
  `external-checks/requests/gwern-request.md`").
- `PLAN.md` §1, rows "Gwern pressure-cooker v4.2 verbatim" and "Gerbrandt
  transcripts" ("Request drafted.").

Read those four sentences as: **cited as unpublished; no request was made.**

**Effect on the study: none.** The two artefacts were never stimuli and never
entered any analysis; the frozen text already states they are not public, that
T3 stimuli follow Hollis Robbins' paraphrase plus the verbatim STRICT TRIADIC v2
spec, and that neither would be used as anything but a descriptive form
reference. No hypothesis, gate, bound, effect size, exclusion rule, covariate or
analysis step is touched. Both files are byte-identical to the frozen versions:
`d5f53310…` and `960dd82…`.

**Why recorded rather than merged.** An earlier attempt on the same day edited
these two frozen files and re-recorded their hashes, which would have made a
post-data edit indistinguishable from the pre-data commitment. That was wrong and
has been reverted; the frozen text is the original text again.

## 2. 2026-11-04 — repository restructure (paths only)

Presentation changes, no content change. Path citations inside the frozen files
still use the pre-restructure names; the mapping is:

| Frozen citation | Now at |
|---|---|
| `external-checks/…` | `sources/…` |
| `scripts/fetch_upstream.sh` | `pipeline/fetch_upstream.sh` |
| `preregistration.md`, `research-plan.md`, `stimulus-design.md` (root) | removed — superseded 16 Oct drafts; still in the vault at `5 Projects/Form-Tightness-Assistant-Axis/` |
| `compute-checklist.md` (root) | `docs/compute-checklist.md` |

`prereg/` keeps its name because `freeze.txt` cites it by path.
