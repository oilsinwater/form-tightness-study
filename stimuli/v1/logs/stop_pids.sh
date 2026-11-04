#!/usr/bin/env bash
# stop_pids.sh — terminate the given PIDs (explicit, owned by this user) politely.
for p in "$@"; do
  if [ -d /proc/$p ]; then
    /bin/kill -TERM "$p" && echo "sent TERM to $p"
  else
    echo "$p not running"
  fi
done
