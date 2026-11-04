#!/usr/bin/env bash
# Rebuild data/assistant-axis-extract/ from the upstream repo at the pinned commit.
#
# The upstream data and transcripts are NOT vendored in this repo: safety-research/
# assistant-axis ships no licence file, so copying its contents into a public repo
# would be redistribution. Fetch it locally instead; this directory is gitignored.
#
# Usage: ./scripts/fetch_upstream.sh
set -euo pipefail

UPSTREAM="https://github.com/safety-research/assistant-axis.git"
COMMIT="a98961956072224eaf244eb289d6c01700b63795"
DEST="$(cd "$(dirname "$0")/.." && pwd)/data/assistant-axis-extract"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Cloning $UPSTREAM at $COMMIT ..."
git clone --filter=blob:none --no-checkout "$UPSTREAM" "$TMP/repo"
git -C "$TMP/repo" checkout --quiet "$COMMIT"

echo "Copying extract into $DEST ..."
rm -rf "$DEST"
mkdir -p "$DEST"
cp "$TMP/repo/data/roles/instructions/default.json"      "$DEST/default.json"
cp "$TMP/repo/data/extraction_questions.jsonl"           "$DEST/extraction_questions.jsonl"
cp "$TMP/repo/data/roles/role_list.json"                 "$DEST/role_list.json"
cp -R "$TMP/repo/transcripts"                            "$DEST/transcripts"

echo "Done. Files:"
find "$DEST" -type f | sed "s|$DEST/||" | sort
