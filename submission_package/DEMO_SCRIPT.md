# TracePilot demo script

Audience: Arize @ Google Cloud Partnerships Hackathon judges  
Length: 2–3 minutes  
Mode: local walkthrough; no public submission implied

## Setup / artifact paths

Repo root:

```bash
cd projects/agent-money-loop-pilot/tracepilot_proof_slice/arize-gemini-hackathon
```

Key proof artifacts:

- Local demo media kit: `demo_media_package/`
  - `STORYBOARD.md` — timed 2–3 minute screen-record plan
  - `SHOT_LIST.md` — safe local captures plus approval-gated Phoenix UI shot
  - `VOICEOVER_SCRIPT.md` — read-aloud narration
  - `CAPTURE_COMMANDS.md` — local commands with no public side effects
  - `ASSET_MANIFEST.md` — proof artifact index
- Latest before/after report: `tracepilot_artifacts/latest/before_after_report.md`
- Latest diagnosis: `tracepilot_artifacts/latest/diagnosis.json`
- Latest fixed artifact: `tracepilot_artifacts/20260513T120607Z/`
- Latest fixed trace ID: `52fa8eaf399d8cc4251a9e7f8441a903`
- Proof gate: `proof_gate/artifacts/20260513T120554Z/`
- Submission package: `submission_package/`

Safe local commands:

```bash
# Inspect the final proof narrative.
sed -n '1,220p' tracepilot_artifacts/latest/before_after_report.md

# Inspect the deterministic diagnosis JSON.
.venv/bin/python -m json.tool tracepilot_artifacts/latest/diagnosis.json | sed -n '1,220p'

# Rebuild local TracePilot report from existing proof artifacts; no new Gemini run.
make tracepilot-demo-local
```

Optional real-stack rerun, only if credentials are configured and another external Gemini/Phoenix call is intended:

```bash
make tracepilot-demo MESSAGE='Find a floral dress in size M, then explain which tool steps you used.'
```

## 2–3 minute narration

### 0:00–0:20 — Problem

“TracePilot is an operator layer for agent reliability. Agents often fail quietly: they produce a plausible answer, but the trace shows they skipped a required step or lost a constraint. In this demo, the user asks for a floral dress in size M and asks the agent to explain which tools it used.”

### 0:20–0:50 — Stack

“This is a real Google ADK/Gemini shopping agent with `search` and `click` tools. The catalog is intentionally compact and in-memory so the demo runs locally in minutes. OpenInference spans are sent to Phoenix, and Phoenix MCP retrieves the latest trace for the operator loop.”

Show:

```bash
sed -n '1,120p' README.md
```

### 0:50–1:30 — Failure trace / diagnosis

“The first run looked reasonable but only scored 71/100. It searched, but it did not preserve size M and did not inspect a specific product. The second run also scored 71/100: it clicked a product, but the final answer still did not explain tool steps or preserve size M.”

Show:

```bash
sed -n '1,180p' submission_package/PROOF_TABLE.md
```

Call out the baseline and second-turn trace IDs:

- Baseline: `ff9f2c11f553ed4ad5f0244604dfc579`
- Second turn: `8e4e88b7bb1c6c9def497031a28c0988`

### 1:30–2:15 — Fix and proof

“The fix was not a hand-wavy prompt tweak. The tool observations now preserve enough product page text after search/click, and the prompt requires a one-turn exact-item answer with ASIN/title, explicit size confirmation, and tool steps. The latest real Gemini/ADK/Phoenix/MCP run scored 100/100.”

Show:

```bash
sed -n '1,220p' tracepilot_artifacts/latest/before_after_report.md
```

Call out the fixed trace ID:

- Latest fixed: `52fa8eaf399d8cc4251a9e7f8441a903`

### 2:15–2:45 — Phoenix MCP value

“Phoenix is what makes this an operator loop instead of a text-only eval. TracePilot uses the trace: span count, tool spans, search/click behavior, MCP retrieval status, and the final answer. The local diagnosis JSON is safe to share because it contains proof facts, not credentials.”

Show:

```bash
.venv/bin/python -m json.tool tracepilot_artifacts/latest/diagnosis.json | sed -n '1,220p'
cat proof_gate/artifacts/20260513T120554Z/result.txt
.venv/bin/python -m json.tool proof_gate/artifacts/20260513T120554Z/phoenix_mcp_summary.json | sed -n '1,180p'
```

### 2:45–3:00 — Close

“The result is a compact proof slice: TracePilot observes a failing trace through Phoenix MCP, diagnoses missing behavior, improves the agent loop, and proves the improvement from 71/100 to 100/100. The next step is a short video and public submission, but those remain approval-gated.”

## Screenshot / video checklist for demo capture

- README architecture / quickstart section.
- `submission_package/PROOF_TABLE.md` showing 71 → 71 → 100.
- `tracepilot_artifacts/latest/before_after_report.md` verdict.
- `tracepilot_artifacts/latest/diagnosis.json` showing `before_score: 100` and the fixed trace facts.
- Phoenix UI showing the fixed trace ID, if logged in and safe to capture.
- Terminal showing `proof_gate/artifacts/20260513T120554Z/result.txt` pass result.
