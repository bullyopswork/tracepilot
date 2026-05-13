# TracePilot — self-debugging ADK/Gemini operator demo

Compact internal hackathon package for the **Arize @ Google Cloud Partnerships Hackathon** track: a small **Google ADK** shopping agent, **Gemini**, **OpenInference/Phoenix** tracing, **Phoenix MCP** retrieval, and a thin **TracePilot operator loop** that diagnoses a real trace and proposes the next better task.

Hosted demo: https://tracepilot-demo-thryhyeqga-uc.a.run.app

This repo uses a **tiny in-memory catalog** so you can run locally in minutes (no PyTorch, Pyserini, or multi-gigabyte product downloads). The agent still exposes familiar **search** / **click** tools and a shopping-focused system prompt derived from [google/adk-samples personalized-shopping](https://github.com/google/adk-samples/tree/main/python/agents/personalized-shopping).

## What it proves

TracePilot is an operator layer above an agent, not another shopping bot. The demo flow is:

1. Run a real Google ADK/Gemini shopping turn.
2. Emit OpenInference spans to Phoenix Cloud.
3. Retrieve the latest trace through `@arizeai/phoenix-mcp`.
4. Score whether the agent satisfied the task: trace health, search/click behavior, size constraint, and tool-step explanation.
5. Write safe before/diagnosis/improvement artifacts with a refined next task.

No credentials are printed or saved in generated reports.

## Prerequisites

- Python 3.10–3.12
- [uv](https://docs.astral.sh/uv/)
- Google auth for Gemini: either `GOOGLE_API_KEY` **or** Vertex (`gcloud auth application-default login` + project/location)
- Phoenix Cloud API key ([Phoenix](https://app.phoenix.arize.com))

## 10-minute quickstart

1. **Clone and install**
  ```bash
   cd gemini-hackathon
   cp .env.example .env
   # Edit .env: PHOENIX_API_KEY, PHOENIX_COLLECTOR_ENDPOINT (Hostname with /s/...), and either GOOGLE_API_KEY or Vertex settings.
   uv sync
  ```
2. **Run the TracePilot proof/demo package**
  ```bash
   make tracepilot-demo MESSAGE='Find a floral dress in size M, then explain which tool steps you used.'
  ```
   This runs the real proof gate, retrieves Phoenix trace context through MCP, and writes `tracepilot_artifacts/<timestamp>/diagnosis.json`, `demo_report.md`, and `refined_task.txt`.
3. **Fast local re-render of the package** — if a proof gate artifact already exists and you do not want another Gemini run:
  ```bash
   make tracepilot-demo-local
  ```
4. **Run a single traced shopping turn only**
  ```bash
   make run MESSAGE='Find a floral dress in size M'
  ```
5. **Open Phoenix** — project name defaults to `PHOENIX_PROJECT_NAME` (`gemini-hackathon`). Confirm LLM and tool spans appear.
6. **(Optional) ADK CLI**
  ```bash
   make run-adk
   # Find a floral dress in size M
  ```
   This path also loads `.env` and initializes Phoenix tracing.

### Phoenix MCP (Gemini CLI)

Phoenix MCP runs **inside Gemini CLI**, not inside the Python ADK process. After traces are flowing from `make run`, you can inspect the same Phoenix space from the CLI. Setup patterns and clients are covered in [Phoenix MCP server](https://arize.com/docs/phoenix/integrations/phoenix-mcp-server).

1. **Configure MCP** — Ensure `[.gemini/settings.json](.gemini/settings.json)` in this repo (or `~/.gemini/settings.json`) includes the `phoenix` server with `@arizeai/phoenix-mcp@latest`. Set `--baseUrl` to your Phoenix space hostname (same idea as `PHOENIX_COLLECTOR_ENDPOINT`: `https://app.phoenix.arize.com/s/your-space`) and set `--apiKey` to your Phoenix API key (`px_live_...`), or keep keys only in env if your CLI supports that pattern.
2. **Export your API key** in the shell that launches Gemini CLI (if the MCP server reads it from the environment):
  ```bash
   export PHOENIX_API_KEY=...
  ```
3. **Start Gemini CLI** from the repo root (or merge the `mcpServers` block into your global Gemini config). Restart the CLI if you just changed MCP settings.
4. **Agent queries Phoenix via MCP (runtime superpower)** — With `@arizeai/phoenix-mcp` configured, the assistant gets **tools** over your Phoenix workspace (traces, sessions, experiments, prompts, datasets, and more). Try prompts such as:
  - *“In Phoenix, show me the last 3 traces in my **gemini-hackathon** project.”*
  - *“In Phoenix, summarize my latest experiment results.”*
  - *“In Phoenix, create a prompt that classifies user intent.”*
   Additional ideas (sessions, annotation configs, datasets): [Using the Phoenix MCP server](https://arize.com/docs/phoenix/integrations/phoenix-mcp-server#using-the-phoenix-mcp-server).
5. **(Optional)** The same file defines **Phoenix Docs MCP** (`phoenix-docs`) for in-IDE Phoenix documentation.

More context: [Phoenix docs](https://arize.com/docs/phoenix).

## TracePilot demo commands

```bash
# Full real-stack proof + operator package.
make tracepilot-demo MESSAGE='Find a floral dress in size M, then explain which tool steps you used.'

# Existing real proof gate remains available.
MESSAGE='Find a floral dress in size M, then explain which tool steps you used.' proof_gate/run_real_gemini_phoenix_gate.sh

# Rebuild diagnosis/report from an existing proof artifact, no external calls.
make tracepilot-demo-local
```

Expected proof artifacts:

- `proof_gate/artifacts/<timestamp>/preflight.txt` — local dependency/auth readiness, no secrets.
- `proof_gate/artifacts/<timestamp>/phoenix_mcp_summary.json` — Phoenix MCP retrieval metadata.
- `proof_gate/artifacts/<timestamp>/phoenix_mcp_get_trace.json` — latest trace payload returned by MCP.
- `tracepilot_artifacts/<timestamp>/diagnosis.json` — rubric score, failed checks, trace facts, refined task.
- `tracepilot_artifacts/<timestamp>/demo_report.md` — human-readable before/diagnosis/improvement card.
- `tracepilot_artifacts/latest/` — copy of the latest TracePilot package.

## Architecture

```text
User task
  -> Google ADK shopping agent (Gemini + search/click tools)
  -> OpenInference instrumentation
  -> Phoenix Cloud traces
  -> Phoenix MCP retrieval
  -> tracepilot_operator.py rubric + diagnosis
  -> safe demo artifacts + refined next task
```

The operator script is intentionally small and deterministic. It does not mutate Phoenix, submit anything externally, or store credentials. It reads proof artifacts, extracts safe trace facts, scores the run, and writes a concrete next task that should force better agent behavior.

## Local submission package

An operator-ready local review package is available in [`submission_package/`](submission_package/):

- [`DEVPOST_DRAFT.md`](submission_package/DEVPOST_DRAFT.md) — draft public story, still approval-gated.
- [`DEMO_SCRIPT.md`](submission_package/DEMO_SCRIPT.md) — 2–3 minute walkthrough with exact local commands and artifact paths.
- [`PROOF_TABLE.md`](submission_package/PROOF_TABLE.md) — verified 71/100 → 71/100 → 100/100 evidence table.
- [`SUBMISSION_CHECKLIST.md`](submission_package/SUBMISSION_CHECKLIST.md) — approval, screenshot/video, and secret-hygiene gates.

Suggested internal demo narrative:

- **Problem:** agents often fail quietly: they produce plausible answers without proving they followed constraints or used tools correctly.
- **Demo:** ask the shopping agent for a floral dress in size M and a tool-step explanation.
- **Observability loop:** Phoenix/OpenInference captures the actual ADK/Gemini/tool trace; Phoenix MCP gives TracePilot retrieval access.
- **Self-debugging moment:** TracePilot scores the trace, finds missing behavior such as product inspection or explicit size confirmation, and emits a refined task.
- **Evidence:** show `demo_report.md`, `diagnosis.json`, Phoenix trace ID, and MCP summary.

Known caveats:

- This is a proof slice with a static Cloud Run-hosted web shell, not a production hosted shopping product.
- The refined task is generated locally; the default demo does not automatically run a second Gemini turn unless the operator chooses to run the proof gate again with `tracepilot_artifacts/latest/refined_task.txt`.
- Current verified proof: baseline `71/100` → second turn `71/100` → latest completion-fix run `100/100` (`tracepilot_artifacts/latest/before_after_report.md`).
- Further external Devpost/video updates remain approval-gated.

## Layout

| Path                       | Purpose                                                                                                                                |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `README.md`                | Demo quickstart, architecture, submission notes                                                                                         |
| `.env.example`             | `PHOENIX_`*, `GOOGLE_`*, optional `GEMINI_MODEL`                                                                                       |
| `.gemini/settings.json`    | Phoenix MCP + Phoenix Docs MCP                                                                                                         |
| `agent/main.py`            | One-shot CLI run with tracing                                                                                                          |
| `agent/instrumentation.py` | `phoenix.otel.register(..., auto_instrument=True)` for ADK tracing                                                                      |
| `agent/shopping_demo/`     | ADK `root_agent`, prompt, tools, mini webshop                                                                                          |
| `proof_gate/`              | Real-stack preflight, ADK/Gemini/Phoenix/MCP proof gate, generated proof artifacts                                                      |
| `tracepilot_operator.py`   | Deterministic TracePilot diagnosis/refinement package builder                                                                           |
| `tracepilot_artifacts/`    | Generated safe demo package artifacts                                                                                                  |
| `submission_package/`      | Local Devpost draft, demo script, proof table, and public-submission checklist                                                         |
| `Makefile`                 | `make setup`, `make run`, `make run-adk`, `make tracepilot-demo`, `make tracepilot-demo-local`                                          |

## Upstream credit

Agent structure and prompts are adapted from **Google ADK Samples** — [personalized-shopping](https://github.com/google/adk-samples/tree/main/python/agents/personalized-shopping) (Apache-2.0). Replace `shopping_demo/mini_webshop.py` with the full WebShop stack when you need the original fidelity.

## License

Apache-2.0 — see [LICENSE](LICENSE).