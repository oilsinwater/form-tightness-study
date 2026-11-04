# Address screen report (v3) — 2026-10-31T14:06:39-0700

Pool: 1536 candidates (`pool.jsonl`). Coders: (1) regex `address_regex.py`; (2) blind LLM coder `MiniMax-M3` via `https://api.minimax.io/v1`, T = 0.0, system prompt = `coding-scheme.md` (ids withheld) + JSON output instruction (sha256 59750b400fb94f18…), user message = prompt text only, seeded order 20261030. A candidate is eligible only if BOTH code `none`.

| cell | n | regex flagged | LLM vocative | LLM ratified | LLM failed | flagged by regex only | by LLM only | by both | **dropped** | eligible | drop rate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| loose_verse | 384 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 384 | 0.0% |
| tight_verse | 384 | 0 | 1 | 3 | 0 | 0 | 4 | 0 | **4** | 380 | 1.0% |
| tight_prose | 384 | 3 | 0 | 1 | 0 | 2 | 0 | 1 | **3** | 381 | 0.8% |
| loose_prose | 384 | 6 | 1 | 10 | 0 | 2 | 7 | 4 | **13** | 371 | 3.4% |

Topic × cell slots with ZERO eligible candidates: 0.
Eligible candidates per topic × cell slot: 3: 20, 4: 364.

Regex hit types (all cells): ident_you_are_np 6, ident_act_as 3.
