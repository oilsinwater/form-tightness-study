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

## 3. 2026-11-04 — deviations found by the post-data audit (none changes a frozen file)

These deviations happened during the run. Some were reported only in `results/arm12_report.md`,
and some were not reported anywhere. They are recorded here so that this file is the complete list.

| # | Frozen text | What was done | Effect |
|---|---|---|---|
| 3.1 | Data exclusion: generations that hit "the max-token limit (1024)" are kept and flagged | `arm_run.py --max-new-tokens 512` (Lu's default, hashed in `freeze.txt`). 448 / 1,139 Arm 1 and 73–88 % of Gemma generations hit it | Response means cover truncated replies. Sensitivity fit without cap hits is reported for Qwen |
| 3.2 | Role-adoption judge uses the repo's `eval_prompt` | Its role slot is set to "any persona other than an AI assistant", because the stimuli assign no role | The behavioural scale is not the one Lu used |
| 3.3 | Randomization: generation order shuffled with seed 20261030; a stimulus's three samples not adjacent | Stimuli run in file order (domain → topic → cell), three samples adjacent within one 12-item batch | Tightness balanced within each batch. Domain confounded with run time |
| 3.4 | Behavioural model: cumulative-link mixed model; linear fallback "if it fails to converge" | Linear mixed model used because statsmodels has no ordinal mixed model. Convergence was never attempted | Fallback taken for a reason the frozen text does not name |
| 3.5 | Manipulation-check gate includes rater ICC(2,1) ≥ 0.75 on a two-rater 60-item subset | One rater only (MiniMax-M3). ICC never computed | That part of the gate is unmet |
| 3.6 | Arm 3 model Gemma-2-27B-it | `unsloth/gemma-2-27b-it-bnb-4bit` (official repo gated) | Same weights in principle. Not verified |
| 3.7 | H1 criterion: contrast **and** a negative linear trend over levels | No trend tested. With two levels the trend is the same contrast | Clause left over from v1, empty under v2 |
| 3.8 | Secondary readouts and exploratory analyses (refusal flag and refusal-excluded fit, rubric sub-item regressions, 2-turn continuation, 24-topic residual-SD pilot, Satterthwaite / topic-level df = 95 check) | Not run, or not reported, for Qwen. The topic-level check was run for Gemma in `results/audit_checks.json` | Listed as not done |
| 3.9 | Freeze record: "Owner action: submit to OSF with `freeze.txt` attached" | Not submitted. First git commit 2026-11-04, after the arms | The freeze time is self-reported and has no external timestamp |
| 3.10 | `results/` holds per-item projections (PLAN §6) | Arm 1 and Arm 2 CSVs and the final 384-item ratings were not committed. Only Gemma's CSV was | The Qwen results cannot be recomputed from the repo |

The audit also found a residual stimulus imbalance that the preregistration never named. In
prose, loose prompts refer to the model as "you" (`self_ref_count`) about 3× as often as tight
prompts do (d = 0.74). That is a finding, not a deviation; it is reported in `REPORT.md` →
Audit corrections, with a covariate check in `pipeline/audit_checks.py`.
