#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python3 - <<'PY'
from pathlib import Path

path = Path("src/agent_workflow_demo/calculator.py")
text = path.read_text(encoding="utf-8")
fixed = "    return left + right\n"
buggy = "    return left - right\n"
if buggy in text:
    print("debug bug is already present")
elif fixed in text:
    path.write_text(text.replace(fixed, buggy, 1), encoding="utf-8")
    print("introduced debug bug: add now subtracts")
else:
    raise SystemExit("could not find expected add implementation")
PY
