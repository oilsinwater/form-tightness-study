#!/usr/bin/env bash
# run_all.sh — full GPU pipeline on raphael. Run from ~/form-tightness/pipeline.
# Each step is resumable; logs go to ~/form-tightness/logs/.
set -euo pipefail
cd "$(dirname "$0")"
source ~/form-tightness/.venv/bin/activate
export PATH=$HOME/.local/bin:$PATH
mkdir -p ~/form-tightness/logs ~/form-tightness/results ~/form-tightness/outputs
# prerequisites: data/ synced from the vault (transcripts, qwen_role_proj_L32.json),
# refusal_direction cloned, HF models cached.
test -d ~/form-tightness/refusal_direction || git clone --depth 1 https://github.com/andyrdt/refusal_direction ~/form-tightness/refusal_direction
python check_b_refusal_cosine.py        2>&1 | tee ~/form-tightness/logs/check_b.log
python check_c_rescore_transcripts.py   2>&1 | tee ~/form-tightness/logs/check_c.log
python check_a_derive_axis.py           2>&1 | tee ~/form-tightness/logs/check_a.log
# arms (after stimuli/stimuli.jsonl exists and prereg is frozen)
# python arm_run.py --name 1_observation
# python arm_run.py --name 2_capped --capping
# python arm_run.py --name 3_gemma --model google/gemma-2-27b-it --layer 22 --axis gemma
uv pip freeze > requirements-lock.txt
