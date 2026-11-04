# Does prompt-form tightness predict Assistant-Axis projection?

A preregistered test of whether the *form* of a prompt — holding its content, token count and
base-model perplexity constant — moves a model along the Assistant Axis
([Lu et al. 2026](https://github.com/safety-research/assistant-axis)).

Built to be wrong in public: every number below comes from a file in `results/`, and every
commitment was hashed before the data existed.

**Results: [`REPORT.md`](REPORT.md)** — the study as run: H1 supported at +3.9 units, capping
removes the gap, the Gemma replication fails with a reversed sign, and the behavioural trace
belongs to register rather than tightness. An audit on 2026-11-04 corrected several statements
and lists the open validity gaps: [`REPORT.md` → Audit corrections](REPORT.md#audit-corrections-2026-11-04).

**Status.** Preregistration frozen 2026-10-31 (`prereg/freeze.txt`, 13 file hashes, all verifying).
Arms 1–3 complete. OSF registration is prepared (`prereg/osf-submission-notes.md`) but **not yet
submitted** — so the registered version will be the frozen text plus `prereg/amendments.md`, not a
DOI that predates the run. `prereg/null-result-writeup.md` is a pre-data anti-HARKing draft for the
null branch and carries no results.

## The question

- **H1** — looser form (free verse, associative, no hard constraints) pushes per-turn projection
  *lower* (further from the Assistant) than tight form (strict metrical/structural constraints),
  content held fixed.
- **H0** — the tightness effect lies inside a TOST equivalence band of ±3 units: one third of the
  turn-0 bounded-vs-therapy gap Lu et al. report.

Three literatures did not meet on this: Lu et al. (projection drops in therapy and philosophy,
holds in coding), Icaro Lab (poetic reformulation defeats refusal), Gerbrandt (a hand-built poem
induces role bleed). None manipulated form while holding content fixed.

## Design

4 domains × 24 topics × register (verse / prose) × tightness (loose / tight) = **384 stimuli**
(`stimuli/stimuli.jsonl`). Register absorbs the perplexity difference that defeated the v1 design —
both failures are kept as evidence under `stimuli/v1/` and `stimuli/v2/`. Selection is
deterministic (seed 20261030) and stratified so |r(tightness, tokens)| and |r(tightness, log-ppl)|
are 0.000 within each register.

| Arm | Model | Manipulation | Outcome |
|---|---|---|---|
| 1 | Qwen3-32B 4-bit | tightness | response-token projection on the published axis, layer 32 |
| 2 | Qwen3-32B 4-bit | tightness × capping `layers_46:54-p0.25` | does the gap shrink under capping |
| 3 | Gemma-2-27B-it 4-bit | tightness | replication on the Gemma axis, layer 22 |

## Results

Arm 1, Qwen3-32B, mixed model `projection ~ tightness × register + domain + (1|topic) + (1|topic:cell)`.
Positive projection = more Assistant-like.
Full account, exclusions and sensitivity fits: `results/arm12_report.md`.

| Test | Estimate | 95 % CI | Reading |
|---|---|---|---|
| H1 tight − loose | **+3.87 units** | [2.64, 5.10] | Supported (p = 7e-10): loose form sits further from the Assistant. Equivalence not declared, but the 90 % CI [2.84, 4.90] reaches inside the ±3 band, so "larger than the SESOI" is not established |
| H4 tightness × register | +4.68 units | [2.21, 7.14] | Not refuted; larger in verse (+6.17) than prose (+1.46). May be inflated by an unbalanced stimulus feature (see the audit) |
| Register verse − prose | −7.73 units | [−8.96, −6.50] | About twice the tightness effect |
| H2 tightness × capping | −5.34 units | [−5.83, −4.84] | Gap +3.82 uncapped → −1.54 capped: over 100 % removed, against a pre-stated 50 % threshold. Behavioural clause as frozen also met (loose cells, capped vs uncapped, p = 2e-12), but capping lowers role adoption in tight cells equally |
| H3 Gemma replication | −335.4 Gemma units | [−402.7, −268.2] | **Fails, sign reversed** (−0.65 role-SD vs Qwen's +0.26), and unstable across layers — treat as "does not replicate", not a clean opposite |

Two things worth stating plainly:

- **The behavioural trace belongs to register, not tightness.** Judge-rated role adoption (0–3,
  2,304 responses) shows tightness +0.01, p = .58, while verse is +0.09 and capping −0.12. Tightness
  moves the projection but leaves no behaviour trace.
- **The Qwen numbers are not yet reproducible from this repo.** The Arm 1–2 per-generation CSVs
  and the final 384-item ratings live on the analysis host; only Gemma's CSV is committed (and its
  numbers reproduce exactly).
- **Gemma's result is fragile.** The tightness effect runs L6 +10.7, L11 −6.1 (n.s.), L22 −335.4,
  L34 +355.3. A sign flip between the target layer and layer 34 is not a replication.

## Layout

```
README.md  REPORT.md  LICENSE  CITATION.cff
AGENTS.md            how this repo is operated by an agent
PLAN.md              design, gates, effect sizes (frozen)
prereg/              preregistration, freeze record, amendments.md, null write-up
sources/             what the primary artefacts actually contain
stimuli/             rubric, 384 stimuli + manifest, rating and selection records, v1/v2 failures
pipeline/            all runnable code, incl. fetch_upstream.sh
results/             small CSV/JSON only
data/                fetched, not vendored
docs/                compute checklist, publishing audit
```

## Reproduce

```bash
git clone https://github.com/oilsinwater/form-tightness-study && cd form-tightness-study
./pipeline/fetch_upstream.sh                    # upstream prompts + transcripts (not vendored: no licence)
pip install -r pipeline/requirements-lock.txt
./pipeline/run_all.sh                           # checks (a)-(c); arms are invoked from arm_run.py
```

The arms need a GPU that holds Qwen3-32B in 4-bit (~24 GB) and the model weights cached; see
`docs/compute-checklist.md`. `pipeline/requirements-lock.txt` was frozen on the machine that ran
them.

## Provenance

`prereg/freeze.txt` records the sha256 of every commitment file as of 2026-10-31T16:30:22-07:00,
before Arms 1–3 ran. Those files are unedited; deviations are recorded in
`prereg/amendments.md` rather than patched into the frozen text. The freeze time is
self-reported: this repository's first commit is dated 2026-11-04, after the arms, and no OSF
registration exists, so nothing external timestamps it. All known deviations from the
preregistration are listed in `prereg/amendments.md` (§3). Among them: the generation cap was 512
tokens, not the 1,024 the exclusion text names. The behavioural judge's role slot was set to "any
persona other than an AI assistant", because the stimuli assign no role. Generation order was not
shuffled. The rater ICC was never run.

## Cite

See `CITATION.cff`. Licensed MIT.
