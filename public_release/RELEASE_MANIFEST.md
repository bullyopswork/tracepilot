# TracePilot public release manifest

Purpose: define the clean public bundle for the TracePilot hackathon submission. This manifest is local prep only; it does not publish, push, upload, deploy, or submit anything.

## Canonical proof to reference

- Proof narrative: `71/100 → 71/100 → 100/100`
- Latest fixed trace ID: `52fa8eaf399d8cc4251a9e7f8441a903`
- Canonical proof gate artifact: `proof_gate/artifacts/20260513T120554Z/`
- Canonical TracePilot artifact: `tracepilot_artifacts/20260513T120607Z/`
- Preferred demo video candidate: `demo_media_package/first_plus_phoenix/tracepilot_demo_first_plus_phoenix_fixed.mp4`

Do **not** use accidental/non-canonical proof artifact `proof_gate/artifacts/20260513T125917Z/` or trace `9e312aec...` in public claims.

## Public-safe files/directories

Recommended public repo contents after final review:

- `README.md`
- `LICENSE` (Apache-2.0)
- `.gitignore`
- `.env.example` with placeholders only
- `pyproject.toml`
- `uv.lock`
- `Makefile`
- `.gemini/settings.json` only if it contains no secrets and uses placeholders/safe command config
- `agent/` source files, excluding caches/runtime state
- `proof_gate/` scripts and README, excluding generated raw proof JSON unless explicitly approved
- `tracepilot_operator.py`
- `submission_package/DEVPOST_DRAFT.md`
- `submission_package/DEMO_SCRIPT.md`
- `submission_package/PROOF_TABLE.md`
- `submission_package/SUBMISSION_CHECKLIST.md`
- `public_release/` docs in this package
- `web_demo/` static demo shell
- `demo_media_package/first_plus_phoenix/tracepilot_demo_first_plus_phoenix_fixed.mp4` only for local video upload/review, not necessarily committed to GitHub

## Keep local/private or exclude from public repo

- `.env` and any shell history/env dumps
- `.venv/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`, `.adk/`, `.arize-tmp-traces/`
- `proof_gate/artifacts/*/phoenix_mcp_get_trace.json` unless manually sanitized and approved
- Raw proof JSON that contains verbose internal trace/model/span fields
- Phoenix UI screenshots/crops until reviewed for private trace/project/account metadata
- Local generated media working files unless needed for the approved demo video
- Any file containing API keys, OAuth tokens, bearer tokens, cookies, private endpoints with embedded secrets, account-private URLs, or credential filenames

## Public wording guardrails

Use claims like:

- "local proof slice"
- "real Gemini/ADK run with Phoenix/OpenInference traces"
- "built with Google ADK, documented under Gemini Enterprise Agent Platform / Agent Platform, and powered by Gemini"
- "Phoenix MCP retrieved trace context"
- "TracePilot produced a deterministic operator diagnosis and refined task"

Avoid claims like:

- "deployed on Google Cloud Agent Builder" unless an Agent Builder / Agent Platform / Agent Runtime deployment is completed and verified
- "production hosted shopping product" unless a hosted demo is deployed and verified
- "fully autonomous self-healing agent" beyond the demonstrated local operator loop
- "public trace available" unless Ed approves exposing the trace/project context

## Final release decision

Public release remains approval-gated. Ed/main must approve GitHub publication, video upload, hosted deploy, and Devpost submit separately.
