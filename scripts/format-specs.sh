#!/bin/bash
set -e
cd "$(dirname "$0")/.."
echo "Formatting spec files..." >&2
uv run mdformat README.md AGENTS.md specs/
echo "Done." >&2
