# TracePilot

## Public links

- Hosted demo: https://tracepilot-demo-thryhyeqga-uc.a.run.app
- GitHub repo: https://github.com/bullyopswork/tracepilot
- Demo video: https://youtu.be/Old2pqRtC70
- Architecture diagram: `docs/architecture.mmd`

## Tagline

A Phoenix MCP-powered operator loop that watches a real Gemini/ADK agent fail quietly, diagnoses the trace, fixes the loop, and proves the next run reaches 100/100.

## Inspiration / problem

AI agents can look successful while missing the actual user constraint. In the shopping demo, the agent could search for a floral dress and produce a plausible answer, but early traces showed it failed to preserve `size M` or inspect a specific product. That is the failure mode TracePilot targets: not “did the model say something fluent?” but “did the agent actually use tools and satisfy the task?”

## What it does

TracePilot sits above a compact Google ADK/Gemini shopping agent and turns observability into an operator feedback loop. The hosted page is a safe demo mode: it replays sanitized proof facts in-browser and does not expose live API keys or require public Phoenix/Gemini credentials.

1. Run a real Gemini/ADK shopping turn with OpenInference spans emitted to Phoenix.
2. Retrieve the latest Phoenix trace through `@arizeai/phoenix-mcp`.
3. Score the trace against concrete task-completion checks: trace retrievability, spans, search/click usage, floral-dress mention, size-M preservation, product inspection, and tool-step explanation.
4. Write safe local artifacts: diagnosis JSON, a human-readable report, a refined task, and a before/after proof table.
5. Demonstrate the fix: the score moved from `71/100` to `71/100` to `100/100` after improving tool observations and prompt behavior.

## How we built it

- **Agent runtime:** Google ADK shopping agent using Gemini (`gemini-2.5-flash` in the verified run).
- **Demo domain:** a compact in-memory WebShop-style catalog with `search` and `click` tools. This keeps the proof local and fast while preserving the core agent/tool behavior.
- **Tracing:** OpenInference/Phoenix instrumentation records agent, LLM, and tool spans.
- **Retrieval:** Phoenix MCP retrieves trace/project context for the latest run.
- **Operator layer:** `tracepilot_operator.py` deterministically reads safe proof artifacts and generates the score, diagnosis, and next-task refinement.
- **Hosted demo mode:** `web_demo/` provides a static, judge-testable safe replay of the same proof sequence without live external calls.
- **Completion fix:** the search/click tool observations were changed to preserve enough product page context, and the shopping prompt was tightened so a one-turn exact-item request must answer with ASIN/title, explicit size confirmation, and the tool steps used.

## Arize / Phoenix usage

Phoenix is the observability backbone of the demo. The proof gate confirms that Phoenix receives real spans and that Phoenix MCP can retrieve them:

- Project identifier: `tracepilot-proof`
- MCP server: `@arizeai/phoenix-mcp@latest`
- Latest fixed trace ID: `52fa8eaf399d8cc4251a9e7f8441a903`
- Latest fixed artifact: `tracepilot_artifacts/20260513T120607Z/`
- Proof gate artifact: `proof_gate/artifacts/20260513T120554Z/`

TracePilot does not need to guess from the final text alone. It uses Phoenix trace facts such as span count, tool spans, search/click usage, and final answer content to explain what happened.

## Gemini usage

Gemini powers the ADK shopping agent. The verified fixed run used Gemini to interpret the user request, call the shopping tools, and produce the final answer:

> I found the "Floral Summer Dress flowy midi" (ASIN: B09P5CRVQ6) and confirmed that size M is available.
>
> Here are the tool steps used:
> 1. Searched for "floral dress".
> 2. Clicked on "B09P5CRVQ6".

## Challenges

- Making the proof honest without turning it into a heavyweight hosted product.
- Keeping reports safe: no credentials are printed in generated artifacts.
- Separating plausible natural-language answers from verifiable task completion.
- Avoiding a fake “self-healing” story: the demo shows a real local operator loop and proof artifacts, not an external production automation claim.

## Accomplishments

- Real Gemini/ADK execution completed.
- Phoenix received retrievable OpenInference traces.
- Phoenix MCP retrieved the latest trace successfully.
- TracePilot produced a deterministic diagnosis and proof narrative.
- The completion fix moved the rubric from a `71/100` plateau to `100/100`.
- The final run passed every rubric check, including size-M preservation, product inspection, and tool-step explanation.

## What’s next

- Turn the local operator loop into a repeatable evaluation harness across multiple tasks.
- Add richer Phoenix-backed evals and trend views across agent revisions.
- Expand beyond the compact in-memory catalog to the full WebShop or real commerce data.
- Turn the Cloud Run static shell into a fuller hosted interactive demo.
- Add richer multi-task benchmark runs beyond the compact shopping proof slice.
- Expand the operator loop to automatically compare Phoenix-backed eval trends across agent revisions.

## Local-only boundary

This draft is for local review before public submission. Do not submit to Devpost, publish GitHub, deploy, or make external changes without explicit approval.
