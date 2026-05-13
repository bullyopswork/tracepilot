# TracePilot proof table

Core claim: TracePilot observed a real Gemini/ADK shopping agent through Phoenix MCP, diagnosed task-completion gaps, applied a completion fix, and proved the score improved from `71/100` to `100/100`.

## Score progression

| Run | Artifact | Trace ID | Score | Result |
| --- | --- | --- | ---: | --- |
| Baseline | `tracepilot_artifacts/20260513T040557Z/` | `ff9f2c11f553ed4ad5f0244604dfc579` | 71/100 | Searched and mentioned floral dress, but did not preserve size M and did not click/inspect a product. |
| Second turn | `tracepilot_artifacts/20260513T115604Z/` | `8e4e88b7bb1c6c9def497031a28c0988` | 71/100 | Clicked/inspected a product, but final answer did not preserve size M or explain tool steps. |
| Latest fixed | `tracepilot_artifacts/20260513T120607Z/` | `52fa8eaf399d8cc4251a9e7f8441a903` | 100/100 | Passed every rubric check: trace retrieval, spans, search, click, floral dress, size M, and tool-step explanation. |

## Check comparison

| Check | Baseline | Second turn | Latest fixed |
| --- | --- | --- | --- |
| Phoenix MCP returned retrievable trace | PASS | PASS | PASS |
| Trace contains spans | PASS | PASS | PASS |
| Agent used search context/tooling | PASS | PASS | PASS |
| Final answer mentions floral dress | PASS | PASS | PASS |
| Final answer explains tool steps | PASS | FAIL | PASS |
| Final answer preserves requested size M | FAIL | FAIL | PASS |
| Agent clicked/inspected a specific product | FAIL | PASS | PASS |

## Final answer excerpts

### Baseline — 71/100

```text
I used the `search` tool with the keywords "floral dress".
I found a floral dress. The ASINs are B09P5CRVQ6, B0DEMO0001, B0DEMO0002. Which one would you like to explore?
```

### Second turn — 71/100

```text
I found a few floral dresses. Let's start by looking at B09P5CRVQ6.
```

### Latest fixed — 100/100

```text
I found the "Floral Summer Dress flowy midi" (ASIN: B09P5CRVQ6) and confirmed that size M is available.

Here are the tool steps used:
1. Searched for "floral dress".
2. Clicked on "B09P5CRVQ6".
```

## What changed in the completion fix

Changed files:

- `agent/shopping_demo/tools/search.py`
- `agent/shopping_demo/tools/click.py`
- `agent/shopping_demo/prompt.py`

Behavioral change:

- Tool observations preserve enough WebShop page text for the model to see product title, selected/available sizes, and clicked-product context.
- The prompt allows a one-turn complete recommendation for exact-item requests.
- The final answer is required to include selected ASIN/title, explicit size confirmation, and a short tool-step list.

## Latest fixed proof facts

Source: `tracepilot_artifacts/latest/diagnosis.json`

- Project identifier: `tracepilot-proof`
- MCP server: `@arizeai/phoenix-mcp@latest`
- Model version: `gemini-2.5-flash`
- Trace ID: `52fa8eaf399d8cc4251a9e7f8441a903`
- Span count: `7`
- Tool span count: `2`
- Used search: `true`
- Used click: `true`
- Passed checks: `7/7`
- Failed checks: `0`

## Honest demo boundary

This is a local proof slice. It uses a compact in-memory catalog to make the agent/tool behavior reproducible without a large product corpus. It does not claim to be a deployed shopping product, and it does not submit, publish, deploy, or mutate external systems by itself.
