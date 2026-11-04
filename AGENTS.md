# form-tightness-study — agent entry point

Preregistered study: does prompt-form tightness predict Assistant-Axis projection (Lu et al. 2026)? Built to be falsifiable in public.

Read in this order: `PLAN.md` → `sources/artefact-inventory.md` → `prereg/preregistration.md`.

## Layout

- `README.md` — reader-facing front door (question, design, status, how to recompute)
- `REPORT.md` — results report: what the study found, gates, limits, what would refute it
- `PLAN.md` — design, gates, effect sizes, sequencing (frozen commitment document)
- `sources/` — what the primary artefacts said; subset-ceiling and capping-sign checks
- `prereg/` — OSF-format preregistration, freeze record, post-freeze amendments, null write-up
- `stimuli/` — rubric, design, topics, generator, pool, decorrelation selection, 384 stimuli + manifest (v1/v2 kept as the record of each failure)
- `pipeline/` — all runnable code, including `fetch_upstream.sh` (runs on raphael, `~/form-tightness/`)
- `results/` — small CSV/JSON results only; large outputs stay on raphael `~/form-tightness/outputs/`
- `data/` — fetched, not vendored; run `pipeline/fetch_upstream.sh`
- `docs/` — compute checklist, publishing audit

## Rules

- Never edit `data/`. Never put weights or activations in this folder (iCloud-synced).
- Every number in a report must come from a file in `results/` or `sources/`.
- Preregistration freezes before Arm 1 runs; record sha256 in `prereg/freeze.txt`.
- Never edit a file listed in `prereg/freeze.txt`. Record deviations in `prereg/amendments.md` instead — editing a frozen file post-data and re-hashing it destroys the record.
- Deviations from Lu et al. go in `prereg/preregistration.md` → Known deviations, not in chat.
- GPU host: `ssh -o BatchMode=yes raphael`; venv `~/form-tightness/.venv`.
