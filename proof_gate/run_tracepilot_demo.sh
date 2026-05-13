#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -d .venv ]; then
  PY=".venv/bin/python"
else
  PY="/opt/homebrew/bin/python3.12"
fi
BASELINE_MESSAGE="${MESSAGE:-Find a floral dress in size M, then explain which tool steps you used.}"
if [ "${TRACEPILOT_SKIP_REAL_GATE:-0}" = "1" ]; then
  PROOF_DIR="${TRACEPILOT_PROOF_DIR:-}"
  if [ -z "$PROOF_DIR" ]; then
    PROOF_DIR="$(find proof_gate/artifacts -maxdepth 1 -type d -name '20*' | sort | tail -1)"
  fi
else
  MESSAGE="$BASELINE_MESSAGE" proof_gate/run_real_gemini_phoenix_gate.sh | tee /tmp/tracepilot_real_gate_latest.txt
  PROOF_DIR="$(awk -F'Artifacts: ' '/Artifacts:/ {print $2}' /tmp/tracepilot_real_gate_latest.txt | tail -1)"
fi
if [ -z "${PROOF_DIR:-}" ] || [ ! -d "$PROOF_DIR" ]; then
  echo "FAIL  TracePilot demo — proof directory not found" >&2
  exit 1
fi
"$PY" tracepilot_operator.py --proof-dir "$PROOF_DIR"
