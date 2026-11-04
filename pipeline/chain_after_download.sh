#!/usr/bin/env bash
# One-off orchestration: wait for the Qwen3-32B download process to exit,
# prefetch Gemma in the background, run check_b then check_c, then launch
# check_a detached. Usage: ./chain_after_download.sh <qwen_download_pid>
set -u
source ~/form-tightness/.venv/bin/activate
cd ~/form-tightness/pipeline
LOG=~/form-tightness/logs
QPID=$1
while [ -d /proc/$QPID ]; do sleep 20; done
echo "$(date) qwen download process exited" >> $LOG/chain.log
nohup python -c 'from huggingface_hub import snapshot_download; print(snapshot_download("google/gemma-2-27b-it", allow_patterns=["*.json","*.safetensors","*.txt","*.jinja","*.py"]))' > $LOG/dl_gemma.log 2>&1 &
echo "$(date) gemma download pid $!" >> $LOG/chain.log
python check_b_refusal_cosine.py > $LOG/check_b.log 2>&1
echo "$(date) check_b exit $?" >> $LOG/chain.log
python check_c_rescore_transcripts.py > $LOG/check_c.log 2>&1
echo "$(date) check_c exit $?" >> $LOG/chain.log
nohup python check_a_derive_axis.py > $LOG/check_a.log 2>&1 &
echo $! > $LOG/check_a.pid
echo "$(date) check_a launched pid $(cat $LOG/check_a.pid)" >> $LOG/chain.log
