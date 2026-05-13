# TracePilot Agent Builder eligibility note

Purpose: local eligibility/wording review only. This file does **not** deploy, publish, submit, create Google Cloud resources, or mutate external systems.

## Official requirement summary

Known local requirement summary for the Google Cloud Rapid Agent Hackathon / Arize track:

- Build a functional agent powered by **Gemini** and **Google Cloud Agent Builder / Agent Builder**.
- Integrate the partner MCP capability for the selected track.
- Run on web, Android, or iOS.
- Submit a hosted project URL, public repository, demo video, and Devpost form.

## Authoritative Google references checked

- <https://cloud.google.com/products/agent-builder>
  - Page title observed: "Gemini Enterprise Agent Platform (formerly Vertex AI) | Google Cloud".
  - The page describes Gemini Enterprise Agent Platform as Google Cloud's platform to "build and deploy enterprise ready agents" and says Agent Platform lets developers "build, customize, and fine-tune sophisticated agents using frameworks like the Agent Development Kit (ADK)."
- <https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart>
  - Google Cloud docs page for **Agent Development Kit** under **Gemini Enterprise Agent Platform**.
  - Navigation includes "Create agents with frameworks" and "Quickstart: Develop with Agent Development Kit on Agent Runtime".
- <https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview>
  - Google Cloud docs page titled "Scale your agents" under **Gemini Enterprise Agent Platform**.
  - Navigation explicitly groups ADK with other frameworks under Agent Runtime / Agent Engine style deployment paths.
- <https://google.github.io/adk-docs/>
  - Google ADK docs say ADK can deploy to Google Cloud via **Agent Runtime (Agent Platform)**, Cloud Run, or GKE.

## What TracePilot currently satisfies

Local inspection found these concrete Google/agent pieces:

- `pyproject.toml` depends on:
  - `google-adk>=1.32.0`
  - `google-genai>=1.9.0`
  - `openinference-instrumentation-google-adk>=0.1.11`
- `agent/shopping_demo/agent.py` defines a real ADK `Agent` with Gemini model default `gemini-2.5-flash` and ADK `FunctionTool` tools.
- `agent/main.py` runs the ADK agent through `google.adk.runners.InMemoryRunner` and `google.genai.types`.
- `.env.example` supports both local `GOOGLE_API_KEY` and Vertex-compatible `GOOGLE_GENAI_USE_VERTEXAI=1`, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION` paths.
- Phoenix/OpenInference integration instruments the Google ADK run and the demo proof uses Phoenix MCP retrieval.

## Ambiguity / risk

The current implementation is a **local Google ADK + Gemini agent**, with a Vertex-compatible auth path. It is not yet deployed to, created in, or verified as a resource inside a branded Google Cloud Agent Builder / Gemini Enterprise Agent Platform / Agent Runtime / Agent Engine service.

The Google docs make the ADK connection defensible because ADK is documented inside Gemini Enterprise Agent Platform and Google describes Agent Platform as supporting frameworks like ADK. However, if Devpost/judges interpret "Google Cloud Agent Builder" as requiring a deployed Agent Builder/Agent Platform/Agent Runtime resource, the current local-only package remains risky.

## Recommended safest path

1. Keep the public claim narrow: TracePilot is "built with Google ADK, documented under Gemini Enterprise Agent Platform, and powered by Gemini."
2. Do **not** claim it is "deployed on Agent Builder" or "created in Agent Builder" unless a Google Cloud deployment/resource is actually performed and verified.
3. Before public Devpost submission, choose one of these gates:
   - **Fast wording gate:** main/Lens verifies the live Devpost rules accept ADK/Gemini as the Agent Builder path. If yes, submit with conservative wording.
   - **Safer implementation gate:** after explicit approval, deploy or wrap the ADK agent using a Google Cloud Agent Platform-compatible path such as Agent Runtime / Agent Engine or Cloud Run, then verify the hosted URL and update the submission wording.
4. Use `GOOGLE_AGENT_PLATFORM_DEPLOYMENT_STUB.md` as the local, non-executed plan for the safer implementation gate.

## Exact claim wording to use

Use:

- "TracePilot is powered by Gemini through Google ADK."
- "The agent is implemented with Google ADK, which Google documents under Gemini Enterprise Agent Platform / Agent Platform."
- "The current proof is a local ADK/Gemini proof slice with Phoenix/OpenInference tracing and Phoenix MCP retrieval."
- "The package includes an approval-gated Google Agent Platform deployment plan; no Google Cloud deployment has been performed yet."

## Exact claim wording to avoid

Avoid until verified by an actual deployment/resource or explicit rule confirmation:

- "TracePilot is deployed on Google Cloud Agent Builder."
- "TracePilot was created in Agent Builder."
- "TracePilot is a production Agent Builder app."
- "The hosted demo runs on Agent Builder / Agent Runtime" unless that hosted path is actually deployed and verified.

## Blocker decision

Verdict: **RESOLVED_WITH_CAVEAT**.

This is not a local-build blocker: the implementation has a defensible ADK/Gemini connection to Google Cloud's Agent Platform documentation. It **is** a public-submission caveat: before Devpost submission, main should either verify that ADK satisfies the Agent Builder wording for this hackathon, or perform an explicit approved Agent Platform / Agent Runtime / Cloud Run deployment and update the claim.
