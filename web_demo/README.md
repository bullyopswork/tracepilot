# TracePilot proof viewer

This static proof viewer was built for the hackathon. It contains no secrets and makes no external API calls or live Phoenix, Gemini, or Google ADK calls. The interactive button fetches bundled sanitized assets from `web_demo/assets/` and renders score, trace, before/after, and public proof-path evidence so judges can inspect the flow without credentials.

Read the [archived before and after report](../public_proof/before_after_report.md) on GitHub, or run the interactive viewer locally. Neither requires API credentials.

## Run locally

```bash
cd web_demo
python3 -m http.server 8080
# open http://localhost:8080
```

## What it includes

- TracePilot project story
- Stack summary: Gemini, Google ADK, OpenInference/Phoenix, Phoenix MCP
- Multi-agent names: `personalized_shopping_agent`, `product_selection_agent`, and `purchase_verification_agent`
- Interactive “Load sanitized proof evidence” path that fetches local static assets from `assets/proof_summary.safe.json` and `assets/before_after_excerpt.md`
- Evidence-backed `71/100 → 71/100 → 100/100` score table with canonical trace ID `52fa8eaf399d8cc4251a9e7f8441a903`
- Direct public proof-path links for `proof_gate/check_multi_agent_structure.py`, `proof_gate/run_real_gemini_phoenix_gate.sh`, `tracepilot_operator.py`, and `public_proof/*`
- Correct demo video link: https://youtu.be/Old2pqRtC70
- GitHub repo link: https://github.com/bullyopswork/tracepilot

## What it excludes

- `.env` contents
- API keys/tokens
- Raw Phoenix trace JSON or private proof payloads
- Private Phoenix/account UI screenshots
- Any runtime external calls from the public static page

## Historical Cloud Run deployment

Deployed after Ed approval on 2026-05-13:

- Project: `bullyopswork`
- Region: `us-central1`
- Service: `tracepilot-demo`
- Historical endpoint: `https://tracepilot-demo-thryhyeqga-uc.a.run.app`

Command shape used from this directory:

```bash
gcloud run deploy tracepilot-demo --source . --region us-central1 --project bullyopswork --allow-unauthenticated --quiet
```

The original static shell returned HTTP `200` when verified in May 2026. The old endpoint is not a working public demo. Use the archived report or the local viewer above.
