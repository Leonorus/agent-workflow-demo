#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python3 - <<'PY'
from pathlib import Path

path = Path("src/agent_workflow_demo/calculator.py")
text = path.read_text(encoding="utf-8")
fixed = "    return left + right\n"
buggy = "    return left - right\n"
if fixed in text:
    print("debug fix is already present")
elif buggy in text:
    path.write_text(text.replace(buggy, fixed, 1), encoding="utf-8")
    print("restored debug fix: add uses addition")
else:
    raise SystemExit("could not find expected add implementation")
PY
