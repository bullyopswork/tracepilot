# TracePilot safe hosted web demo

Safe hosted demo mode for the hackathon hosted-project requirement. It is intentionally safe: no secrets, no external API calls, and no live Phoenix/Gemini/Google ADK calls embedded in the public page. The interactive button replays deterministic sanitized proof facts so judges can test the flow without credentials.

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
- Interactive “Run safe demo proof” path that deterministically replays the sanitized proof sequence
- Canonical proof references and sanitized `71/100 → 71/100 → 100/100` proof narrative
- Correct demo video link: https://youtu.be/Old2pqRtC70
- GitHub repo link: https://github.com/bullyopswork/tracepilot

## What it excludes

- `.env` contents
- API keys/tokens
- Raw proof JSON
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

Verification: public HTTP status `200`; live page contains expected TracePilot title/H1, Phoenix MCP wording, and Gemini/ADK wording. After this local upgrade, redeploy is still required before the public URL reflects the safe interactive proof mode.
