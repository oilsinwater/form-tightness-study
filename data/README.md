# data/

Not vendored. Everything under `data/assistant-axis-extract/` is a local copy of
`data/` and `transcripts/` from the upstream repo
[`safety-research/assistant-axis`](https://github.com/safety-research/assistant-axis)
at commit `a98961956072224eaf244eb289d6c01700b63795`.

That repo ships no licence file, so its contents are not redistributed here.
Rebuild the extract before running anything that reads it:

```bash
./pipeline/fetch_upstream.sh
```

Files this produces:

| Path | Upstream source |
|---|---|
| `default.json` | `data/roles/instructions/default.json` |
| `extraction_questions.jsonl` | `data/extraction_questions.jsonl` |
| `role_list.json` | `data/roles/role_list.json` |
| `transcripts/` | `transcripts/` |

Never edit anything in this directory: it is a verbatim copy, and the fetch
script overwrites it.
