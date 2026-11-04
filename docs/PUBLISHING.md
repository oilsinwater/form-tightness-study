# Publishing this repo — pre-flight audit

Audited 2026-11-04, before the first commit. Scope: every file that would be
tracked by a fresh git repo in this folder (168 files, 24.2 MB).

## Verdict

No credentials, keys, tokens, or `.env` content are present. Nothing here is a
security incident if published. What the audit found was machine-identifying
detail, plus one third-party redistribution problem.

## Cleaned before first commit

| Item | Action |
|---|---|
| Absolute home paths (`/home/<user>/...`, `/Users/<user>/...`) in 13 files (logs, `sources.json`, corpus README, lockfile, 2 analysis scripts) | Rewritten to `~/...`; the two `.py` files use `os.path.expanduser` so they still run. Verified: 0 remaining. |
| `pipeline/requirements-lock.txt` line 14 (an absolute `-e file:///...` editable install) | Replaced with a comment — the path was never portable. |
| `results/check_a_axis_ours.pt` (1.3 MB, 64×5120 activation tensor) | Ignored. `AGENTS.md` forbids activations in this folder; binary blobs don't belong in git. |
| `data/assistant-axis-extract/` (20 files) | Ignored and replaced by `pipeline/fetch_upstream.sh`, which reproduces it byte-for-byte from the pinned upstream commit. Verified with `diff -rq`: identical. |
| `.DS_Store` ×2, `__pycache__` ×2, `*.pyc`, empty `*.out`, `check_a.pid` | Ignored. |
| Logs (`stimuli/**/logs/*.log`) | **Kept** — `STATUS.md` and `design.md` cite them as the record of the failed v1 selection. Paths scrubbed, content intact. |

## Decisions taken

1. **Hardware / host fingerprint: kept as-is.** `compute-checklist.md` names the
   GPU host and its specs (RTX 3090 24 GB, 61 GB RAM, 580 GB free, the SSH alias,
   the llama.cpp server and its model). A hostname and hardware spec do not grant
   access, and they are genuine provenance for a study that asks to be recomputed.
2. **Upstream data: fetched, not vendored.** `safety-research/assistant-axis` ships
   no licence file (GitHub API: `license: null`), so its `data/` and `transcripts/`
   are not redistributed here. `data/README.md` documents the pinned commit;
   `./pipeline/fetch_upstream.sh` rebuilds the local copy.
3. **Commit identity:** `Phil D <23019793+oilsinwater@users.noreply.github.com>`,
   set repo-locally. The iCloud address never enters a commit.

## Left as-is, worth knowing

- `pipeline/fetch_upstream.sh` cannot be executed from this iCloud path under the
  local lifecycle guard; run it from a normal checkout or your own shell.

## Follow-up, same day

The audit above is the record of the first push. Two things changed after it:

1. **Presentation.** The repo had no front door and two files called
   `preregistration.md` — the root one an un-locked 16 Oct draft whose text does
   not match the frozen hash. It, `research-plan.md` and `stimulus-design.md`
   were removed (they survive in the vault at
   `5 Projects/Form-Tightness-Assistant-Axis/`), `README.md` and `CITATION.cff`
   were added, `external-checks/` became `sources/`, `scripts/` was folded into
   `pipeline/`, and the two process docs moved to `docs/`.
2. **A correction.** The first attempt at withdrawing the two source-request
   drafts edited `prereg/preregistration.md` and `PLAN.md` and re-recorded their
   hashes, with a note claiming it happened before Arm 1 ran. Arms 1–3 had in
   fact run on 31 Oct – 1 Nov. Both files were reverted to their frozen content,
   and the withdrawal is now recorded in `prereg/amendments.md` instead. All 13
   freeze hashes verify against the files on disk.
