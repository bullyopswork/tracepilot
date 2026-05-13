# TracePilot Real Proof Gate

This is the **continue / do-not-waste-time gate** before a full TracePilot build.

Goal: prove the real Arize track stack works:

1. Google ADK/Gemini can run one agent turn.
2. OpenInference/Phoenix instrumentation emits spans.
3. Phoenix Cloud receives those spans in the expected project.
4. Phoenix MCP can inspect the traces/evals.

## Safe credential rule

Do **not** paste API keys in chat or save them in memory. Put them in this repo's local `.env` file or shell environment. `.env` is gitignored by the starter repo.

Required path A — simplest local Gemini API:

```bash
GOOGLE_API_KEY=...
PHOENIX_API_KEY=...
PHOENIX_COLLECTOR_ENDPOINT=https://app.phoenix.arize.com/s/<your-space>
PHOENIX_PROJECT_NAME=tracepilot-proof
```

Required path B — Vertex:

```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=...
GOOGLE_CLOUD_LOCATION=us-central1
PHOENIX_API_KEY=...
PHOENIX_COLLECTOR_ENDPOINT=https://app.phoenix.arize.com/s/<your-space>
PHOENIX_PROJECT_NAME=tracepilot-proof
```

## Commands

```bash
cd projects/agent-money-loop-pilot/tracepilot_proof_slice/arize-gemini-hackathon
. .venv/bin/activate
python proof_gate/check_real_stack.py
MESSAGE='Find a floral dress in size M, then explain which tool steps you used.' proof_gate/run_real_gemini_phoenix_gate.sh

# Full internal TracePilot package: real proof gate + MCP trace diagnosis + safe report artifacts.
make tracepilot-demo MESSAGE='Find a floral dress in size M, then explain which tool steps you used.'

# Local report rebuild from latest proof artifact, no new external calls.
make tracepilot-demo-local
```

## Pass criteria

- `check_real_stack.py` prints `READY`.
- `run_real_gemini_phoenix_gate.sh` completes without exception.
- Phoenix Cloud shows fresh spans for `tracepilot-proof` or configured project.
- Phoenix MCP can answer: "show/summarize the latest trace in my tracepilot-proof project."
- TracePilot package writes `tracepilot_artifacts/<timestamp>/diagnosis.json`, `demo_report.md`, `refined_task.txt`, and `phoenix_mcp_summary.safe.json`.

## Latest verified completion-fix pass

- Proof gate artifact: `proof_gate/artifacts/20260513T120554Z/`
- TracePilot artifact: `tracepilot_artifacts/20260513T120607Z/`
- Command: `proof_gate/run_tracepilot_demo.sh`
- Result: real Gemini/ADK/Phoenix/MCP proof gate passed; TracePilot diagnosis reached `100/100`.
- Phoenix MCP summary: `initialize_ok: true`, `list_projects_ok: true`, `list_traces_ok: true`, `get_trace_ok: true`
- Canonical trace ID: `52fa8eaf399d8cc4251a9e7f8441a903`

Do not use the earlier proof gate artifact `proof_gate/artifacts/20260513T034604Z/` / trace `c8ebc1c21c368228cc927d7f9f4a625d` as the latest or canonical public proof.

## Critical go/no-go rule

This gate is now green for a full internal TracePilot build/package if Ed chooses the hackathon lane. External publication/submission remains approval-gated.
