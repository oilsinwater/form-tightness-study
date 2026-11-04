---
type: note
date: 2026-10-30
status: working
---

# OSF submission notes — owner to execute

The agent cannot log in to OSF. Everything below is for the owner. Do this **after** stimuli are frozen and **before** Arm 1 runs.

## 0. Prerequisites

- `prereg/preregistration.md` is final (no `[BLANK]` except the freeze-record hashes and Authors, which you fill in step 2).
- `stimuli/stimuli.jsonl` and `stimuli/manifest.json` exist and are final (decorrelation gate and manipulation check passed and logged).
- `pipeline/power.py` output matches the table in the preregistration (re-run: `/usr/local/bin/python3 pipeline/power.py --markdown`, seed 20261030; it is deterministic).

## 1. Freeze procedure (do this first, record the hashes)

From the project root:

```
shasum -a 256 prereg/preregistration.md stimuli/stimuli.jsonl stimuli/manifest.json
```

Note: the preregistration contains its own hash field. To avoid a circular hash, hash the file **with the freeze-record lines still reading `[BLANK]`**, then paste the three hashes into the OSF form (step 3, "Other"). Do not edit `preregistration.md` after hashing except for the Freeze record block; the OSF form holds the authoritative hashes. Optionally commit and tag the repo (`git tag prereg-frozen`) and put the commit hash in the form too.

## 2. Create the registration

1. Log in at osf.io. Create a project (or use the existing one): title as in the preregistration.
2. Upload to OSF Storage: `prereg/preregistration.md`, `prereg/null-result-writeup.md`, `stimuli/tightness-rubric.md`, `pipeline/power.py`, `prereg/power-table.md`, `stimuli/manifest.json`. (Upload `stimuli.jsonl` too unless it must stay private until the run; if private, the hash in the form is the commitment.)
3. Project → Registrations → New registration → choose **"OSF Preregistration"** (this is the template whose section headings `preregistration.md` follows; do not pick "Preregistration Challenge", "AsPredicted", or "Open-Ended").
4. Fill Authors in the form and in `preregistration.md` (Study Information → Authors) — the markdown says `[BLANK]`.

## 3. Field mapping — OSF form field → `preregistration.md` section

Copy the markdown text of each section into the matching form field. Tables paste as plain text; that is fine.

| OSF form field | preregistration.md |
|---|---|
| Study Information → Title | Study Information → Title |
| Study Information → Authors | Study Information → Authors (fill) |
| Study Information → Description | Study Information → Description |
| Study Information → Hypotheses | Study Information → Hypotheses (H1, H0, H2, H3) |
| Design Plan → Study type | Design Plan → Study type ("Experiment") |
| Design Plan → Blinding | Design Plan → Blinding (tick "no blinding" for participants — there are none — and paste the text) |
| Design Plan → Study design | Design Plan → Study design (include the arms table) |
| Design Plan → Randomization | Design Plan → Randomization |
| Sampling Plan → Existing data | choose "Registration prior to analysis of the data" |
| Sampling Plan → Explanation of existing data | Sampling Plan → Explanation of existing data |
| Sampling Plan → Data collection procedures | Sampling Plan → Data collection procedures |
| Sampling Plan → Sample size | Sampling Plan → Sample size |
| Sampling Plan → Sample size rationale | Sampling Plan → Sample size rationale (include the power table verbatim) |
| Sampling Plan → Stopping rule | Sampling Plan → Stopping rule |
| Variables → Manipulated variables | Variables → Manipulated variables |
| Variables → Measured variables | Variables → Measured variables |
| Variables → Indices | Variables → Indices |
| Analysis Plan → Statistical models | Analysis Plan → Statistical models |
| Analysis Plan → Transformations | Analysis Plan → Transformations |
| Analysis Plan → Inference criteria | Analysis Plan → Inference criteria |
| Analysis Plan → Data exclusion | Analysis Plan → Data exclusion |
| Analysis Plan → Missing data | Analysis Plan → Missing data |
| Analysis Plan → Exploratory analysis | Analysis Plan → Exploratory analysis |
| Other | Other: paste **all** of it — pre-stimulus gates (a)(b)(c), manipulation-check gate, decorrelation acceptance, Known deviations table, Limitations, and the three sha256 hashes from step 1 plus the repo commit hash |

Attach the uploaded files to the registration when the form asks ("Add files").

## 4. Submit

- Embargo: none (choose "Make registration public immediately") unless you want the stimuli private until the run; a public registration with a private stimuli file is still fine because the hash is public.
- Submit. OSF gives a 48-hour window to cancel; after that it is permanent and gets a DOI.
- Paste the registration DOI/URL into: `prereg/preregistration.md` (Freeze record), `prereg/null-result-writeup.md` (header), both request drafts in `external-checks/requests/` (the `[BLANK — OSF link]` fields), `PLAN.md` §6.

## 5. After registration

- Fill the Freeze record block in `preregistration.md` with the hashes and date; commit. Note that this edit changes the file hash; the hash of record is the one in the OSF form.
- Only then start gate (a) on the GPU. Gate (a) is itself registered: if cos < 0.9, the study is abandoned and that is published as an OSF registration outcome ("registration report: aborted at gate (a)").
- Any deviation during the run goes into a `prereg/deviations.md` with date and reason, and is listed in the write-up.
