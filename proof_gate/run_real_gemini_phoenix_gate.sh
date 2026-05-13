#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUTDIR="proof_gate/artifacts/$STAMP"
mkdir -p "$OUTDIR"
if [ -d .venv ]; then
  PY=".venv/bin/python"
else
  PY="/opt/homebrew/bin/python3.12"
fi
MESSAGE="${MESSAGE:-Find a floral dress in size M, then explain which tool steps you used.}"
"$PY" proof_gate/check_real_stack.py | tee "$OUTDIR/preflight.txt"
cd agent
../"$PY" main.py "$MESSAGE" > "../$OUTDIR/adk_stdout.txt" 2> "../$OUTDIR/adk_stderr.txt"
cd ..
"$PY" proof_gate/check_phoenix_mcp.py "$OUTDIR" | tee "$OUTDIR/phoenix_mcp_check.txt"
printf 'Real Gemini/ADK/Phoenix/MCP proof gate passed.\nArtifacts: %s\n' "$OUTDIR" | tee "$OUTDIR/result.txt"
