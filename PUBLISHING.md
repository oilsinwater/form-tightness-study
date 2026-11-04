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
| `data/assistant-axis-extract/` (20 files) | Ignored and replaced by `scripts/fetch_upstream.sh`, which reproduces it byte-for-byte from the pinned upstream commit. Verified with `diff -rq`: identical. |
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
   `./scripts/fetch_upstream.sh` rebuilds the local copy.
3. **Commit identity:** `Phil D <23019793+oilsinwater@users.noreply.github.com>`,
   set repo-locally. The iCloud address never enters a commit.

## Left as-is, worth knowing

- `external-checks/requests/gwern-request.md` contains `gwern@gwern.net`, scraped
  from a public page, inside an unsent outreach draft. Public information; left in.
- No `README.md`, no `LICENSE`, no `CITATION.cff`. A study built "to be wrong in
  public" is hard to cite without them — worth adding before announcing the repo.
- `scripts/fetch_upstream.sh` cannot be executed from this iCloud path under the
  local lifecycle guard; run it from a normal checkout or your own shell.

## Publish sequence

```bash
cd "5 Projects/form-tightness-study"
git status --short          # confirm: no .pt, no __pycache__, no assistant-axis-extract
git commit -m "Initial: preregistered form-tightness study"
gh repo create form-tightness-study --public --source=. --remote=origin --push
```

Then add `5 Projects/form-tightness-study/` to the vault's own `.gitignore` so the
nested repo does not become an accidental gitlink in Nube Cripta.
