# TracePilot safe hosted web demo

Safe hosted proof explorer for the hackathon hosted-project requirement. It is intentionally safe: no secrets, no external API calls, and no live Phoenix/Gemini/Google ADK calls embedded in the public page. The interactive button fetches bundled sanitized assets from `web_demo/assets/` and renders score, trace, before/after, and public proof-path evidence so judges can inspect the flow without credentials.

Verified Cloud Run URL:

- https://tracepilot-demo-thryhyeqga-uc.a.run.app

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

## Cloud Run deployment

Deployed after Ed approval on 2026-05-13:

- Project: `bullyopswork`
- Region: `us-central1`
- Service: `tracepilot-demo`
- Public URL: https://tracepilot-demo-thryhyeqga-uc.a.run.app

Command shape used from this directory:

```bash
gcloud run deploy tracepilot-demo --source . --region us-central1 --project bullyopswork --allow-unauthenticated --quiet
```

Verification: public HTTP status `200`; live page contains expected TracePilot title/H1, Phoenix MCP wording, and Gemini/ADK wording. After this local upgrade, redeploy is still required before the public URL reflects the evidence-backed sanitized proof explorer.
