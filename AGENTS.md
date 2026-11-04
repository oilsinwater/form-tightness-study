# form-tightness-study — agent entry point

Preregistered study: does prompt-form tightness predict Assistant-Axis projection (Lu et al. 2026)? Built to be falsifiable in public.

Read in this order: `PLAN.md` → `external-checks/artefact-inventory.md` → `prereg/preregistration.md`.

## Layout

- `PLAN.md` — design, gates, effect sizes, sequencing (commitment document)
- `external-checks/` — what the primary artefacts said; subset-ceiling and capping-sign checks
- `prereg/` — OSF-format preregistration, pre-drafted null write-up, OSF submission notes
- `stimuli/` — rubric, design, topics, generator, pool, decorrelation selection, 288 stimuli + manifest
- `pipeline/` — all runnable code (runs on raphael, `~/form-tightness/`)
- `results/` — small CSV/JSON results only; large outputs stay on raphael `~/form-tightness/outputs/`
- `data/assistant-axis-extract/` — verbatim copies of the repo transcripts and default prompts (immutable)

## Rules

- Never edit `data/`. Never put weights or activations in this folder (iCloud-synced).
- Every number in a report must come from a file in `results/` or `external-checks/`.
- Preregistration freezes before Arm 1 runs; record sha256 in `prereg/freeze.txt`.
- Deviations from Lu et al. go in `prereg/preregistration.md` → Known deviations, not in chat.
- GPU host: `ssh -o BatchMode=yes raphael`; venv `~/form-tightness/.venv`.
