# TracePilot hosted project plan

Goal: satisfy the hackathon "runs on web/Android/iOS" requirement with the lowest-risk path. The minimal static web demo shell has now been deployed to Cloud Run and verified public.

## Recommended path: static web demo shell

Local files:

- `web_demo/index.html` — single-page public demo
- `web_demo/styles.css` — static styling
- `web_demo/README.md` — local run and future deploy notes

Local command:

```bash
cd web_demo
python3 -m http.server 8080
# open http://localhost:8080
```

No secrets, no external API calls, and no Phoenix/Gemini calls are embedded in the static shell.

Verified hosted URL:

- https://tracepilot-demo-thryhyeqga-uc.a.run.app

## What the web shell should show

- Project title/tagline
- The stack: Gemini, Google ADK, OpenInference/Phoenix, Phoenix MCP, TracePilot operator
- Proof narrative: `71/100 → 71/100 → 100/100`
- Canonical trace/artifact references
- Sanitized final-answer excerpt
- Demo video placeholder pointing to `../demo_media_package/first_plus_phoenix/tracepilot_demo_first_plus_phoenix_fixed.mp4`
- Clear note that raw proof JSON and secrets are not public

## Future hosted options after approval

### Option A — Firebase Hosting/static hosting

Best if Ed wants a simple hosted URL quickly.

1. Final secret scan.
2. Copy only `web_demo/` contents plus approved static assets into a clean deploy folder.
3. Deploy through Firebase Hosting or another approved static host.
4. Open hosted URL in a clean browser and verify no private paths/secrets are visible.

### Option B — Cloud Run static container

Best if the submission needs a Google Cloud-hosted URL.

Prepared local files:

- `web_demo/Dockerfile`
- `web_demo/.dockerignore`

Deployment executed after Ed approval on 2026-05-13 using the Bully Ops Google Cloud project/account:

```bash
gcloud run deploy tracepilot-demo --source . --region us-central1 --project bullyopswork --allow-unauthenticated --quiet
```

Verified service:

- Service: `tracepilot-demo`
- Project: `bullyopswork`
- Region: `us-central1`
- Public URL: https://tracepilot-demo-thryhyeqga-uc.a.run.app

### Option C — Android/iOS wrapper

Not recommended for the current deadline. The static web shell can run in mobile browsers. A native wrapper would add risk without improving the core proof.

## Hosted URL status

Current status: **complete / verified**.

Verification on 2026-05-13:

- Public HTTP check returned `200`.
- Live page contained expected TracePilot title/H1, Phoenix MCP wording, and Gemini/ADK wording.
- Browser snapshot confirmed the rendered page and public demo shell content.
