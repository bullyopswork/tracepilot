# Google Agent Platform deployment stub

Purpose: document the TracePilot Agent Builder / hosted-demo eligibility path.

External Cloud Run action was executed only after Ed approval on 2026-05-13. Do not deploy additional resources, change auth/billing/IAM, publish, or submit without explicit Ed/main approval.

## Current local agent shape

- Runtime: Google ADK Python agent in `agent/shopping_demo/agent.py`.
- Model: Gemini, default `gemini-2.5-flash` via `GEMINI_MODEL`.
- Tools: ADK `FunctionTool` wrappers for `search` and `click`.
- Runner: local `InMemoryRunner` in `agent/main.py`.
- Observability: OpenInference instrumentation for Google ADK, exporting to Phoenix.

## Approval-gated hardening option A — Agent Runtime / Agent Engine path

Use this if judges require a Google Cloud Agent Platform-branded runtime instead of local ADK only.

Planned work after approval:

1. Confirm target Google Cloud project, region, budget/risk cap, and auth context.
2. Follow the Google Cloud ADK / Agent Runtime documentation for packaging an ADK agent.
3. Add only the minimal deployment metadata required for the TracePilot ADK agent.
4. Deploy a non-sensitive demo instance.
5. Verify from a clean browser that the hosted endpoint/demo works and contains no private data.
6. Update Devpost wording from "local ADK/Gemini proof slice" to the exact verified hosted runtime wording.

Do not claim this path is complete until the hosted runtime is deployed and independently verified.

## Approval-gated hardening option B — Cloud Run web shell path

Use this if the submission only needs a hosted URL and accepts the ADK/Gemini implementation as the Agent Builder/Agent Platform path.

Executed after approval:

1. Final web shell review confirmed the static shell has no embedded secrets or live Phoenix/Gemini calls.
2. Enabled Cloud Run / Cloud Build / Artifact Registry APIs in the Bully Ops project.
3. Deployed the static `web_demo/` shell to Cloud Run.
4. Verified the public URL from a clean browser/tooling path.
5. Keep Devpost wording conservative: the public site demonstrates a local ADK/Gemini proof and links to the repository/video.

Verified public URL:

- https://tracepilot-demo-thryhyeqga-uc.a.run.app

## Wording rule

Cloud Run web shell path is executed and verified. Use conservative wording: "built with Google ADK and powered by Gemini, with a verified Cloud Run-hosted web demo." Do not say "deployed on Agent Builder" or "running on Agent Runtime" unless the separate Agent Runtime/Agent Engine path is actually completed and verified.
