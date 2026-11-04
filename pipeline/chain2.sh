#!/usr/bin/env bash
# One-off orchestration (second launch): check_c (Qwen, then Gemma in a fresh process), then check_a detached.
set -u
source ~/form-tightness/.venv/bin/activate
cd ~/form-tightness/pipeline
LOG=~/form-tightness/logs
python check_c_rescore_transcripts.py > $LOG/check_c.log 2>&1
echo "$(date) check_c exit $?" >> $LOG/chain.log
nohup python check_a_derive_axis.py > $LOG/check_a.log 2>&1 &
echo $! > $LOG/check_a.pid
echo "$(date) check_a launched pid $(cat $LOG/check_a.pid)" >> $LOG/chain.log
