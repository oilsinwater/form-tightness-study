#!/bin/bash
# stop_gen.sh — stop the running generate_pool.py on this host by explicit PID
for p in $(pgrep -f "^python generate_pool.py"); do echo "kill $p"; kill "$p"; done
sleep 2
pgrep -af "^python generate_pool" | wc -l
