# Stimuli v3 — status (2026-10-31)

| Gate | Result |
|---|---|
| Address = none (regex + blind MiniMax-M3), all 384 | PASS (dropped 20 of 1,536 candidates; 0 empty slots) |
| r(tightness, tokens), r(tightness, log-ppl) < 0.10, overall + per register | PASS (0.000 everywhere) |
| Per-domain token spread < 10 % | PASS (max 7.5 %) |
| 130–200 Qwen tokens | PASS (384/384) |
| Manipulation check, tight > loose within register, d > 1.0 | PASS on 219/384 rated (d 2.18 verse, 2.84 prose); final pending |
| Human second rater / ICC | NOT DONE (needs owner) |

Re-rating is still running on raphael (`rate_tightness.py --workers 1`, log `logs/rate_v3d.log`); MiniMax-M3 spends most of its budget in `<think>` so items take ~27 s. Resumable.

sha256 at this snapshot: stimuli.jsonl `820140f4538bb3fa6e7fb5165d9577197b802513f6ba7326b1e9f29b2aa46ad5`, manifest.json `ce7e003b0e1db67bef6775693bbe0141ac3861db2465441c2d2c3330711df005`. Selection is final; only ratings will change.
