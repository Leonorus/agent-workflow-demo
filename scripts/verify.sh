#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

for script in scripts/*.sh; do
  bash -n "$script"
done

PYTHON_BIN="${PYTHON:-python3}"

PYTHONPATH=src "$PYTHON_BIN" -m compileall -q src tests
PYTHONPATH=src "$PYTHON_BIN" -m unittest discover -s tests -q

echo "verification passed"
