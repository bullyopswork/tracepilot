# TracePilot web demo shell

Static shell for the hackathon hosted-project requirement. It is intentionally safe: no secrets, no external API calls, and no Phoenix/Gemini calls embedded in the public page.

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
- Canonical proof references
- Sanitized `71/100 → 71/100 → 100/100` proof narrative
- Demo video placeholder; public YouTube/Vimeo URL will be added after approval and upload verification.
- Reviewed local video candidate: `../demo_media_package/first_plus_phoenix/tracepilot_demo_first_plus_phoenix_fixed.mp4`

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

Verification: public HTTP status `200`; live page contains expected TracePilot title/H1, Phoenix MCP wording, and Gemini/ADK wording.
