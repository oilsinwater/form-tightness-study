#!/bin/bash
# finalize.sh — run on raphael. Waits for the GPU (up to --max-wait), measures any unmeasured pool rows,
# re-runs the deterministic selection, then the blind rating. Idempotent; safe to re-run.
set -e
source ~/form-tightness/.venv/bin/activate
cd ~/form-tightness/stimuli
python measure_pool.py --pool pool.jsonl --out pool_measured.jsonl --max-wait ${MAX_WAIT:-14400}
python select_stimuli.py --restarts 40
# ratings are keyed by stimulus id; items whose selected candidate changed must be re-rated,
# so drop rows whose cand_id no longer matches the new selection.
python - <<'EOF'
import csv, json, os
if os.path.exists("tightness_ratings.csv"):
    sel = {json.loads(l)["id"]: json.loads(l)["prompt"] for l in open("stimuli.jsonl")}
    rows = list(csv.DictReader(open("tightness_ratings.csv")))
    # prompt text is not stored in the csv; use the sha256 recorded in manifest at rating time if present
    keep = []
    prev = {}
    if os.path.exists("rated_prompt_sha.json"):
        prev = json.load(open("rated_prompt_sha.json"))
    import hashlib
    for r in rows:
        h = hashlib.sha256(sel.get(r["id"], "").encode()).hexdigest()
        if prev.get(r["id"]) == h:
            keep.append(r)
    with open("tightness_ratings.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else ["id"])
        w.writeheader(); w.writerows(keep)
    print(f"kept {len(keep)}/{len(rows)} ratings whose item text is unchanged")
EOF
python rate_tightness.py --workers 8
python - <<'EOF'
import json, hashlib
sha = {json.loads(l)["id"]: hashlib.sha256(json.loads(l)["prompt"].encode()).hexdigest() for l in open("stimuli.jsonl")}
json.dump(sha, open("rated_prompt_sha.json", "w"), indent=0)
EOF
echo FINALIZE_DONE
