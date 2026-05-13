# TracePilot hosted project plan

Goal: satisfy the hackathon "runs on web/Android/iOS" requirement with the lowest-risk path. The original static shell was deployed to Cloud Run and verified public. The local `web_demo/` has now been upgraded into a safe interactive demo mode; redeploy is required before the public URL reflects the upgraded judge-testable page.

## Recommended path: safe static interactive hosted demo

Local files:

- `web_demo/index.html` — single-page public demo with deterministic “Run safe demo proof” interaction
- `web_demo/styles.css` — static styling
- `web_demo/README.md` — local run and deployment notes
- `docs/architecture.mmd` — simple Mermaid architecture diagram for README/Devpost citation

Local command:

```bash
cd web_demo
python3 -m http.server 8080
# open http://localhost:8080
```

No secrets, no external API calls, and no live Phoenix/Gemini/Google ADK calls are embedded in the static page. The browser interaction uses sanitized proof facts; the source repo and demo video show the real runnable proof path.

Verified hosted URL:

- https://tracepilot-demo-thryhyeqga-uc.a.run.app

## What the web shell should show

- Project title/tagline
- The stack: Gemini, Google ADK, OpenInference/Phoenix, Phoenix MCP, TracePilot operator
- Proof narrative: `71/100 → 71/100 → 100/100`
- Interactive safe proof replay: user task → ADK coordinator/specialists → Gemini/ADK output → Phoenix/OpenInference trace retrieval via Phoenix MCP → TracePilot diagnosis/refinement
- Canonical trace/artifact references
- Sanitized final-answer excerpt
- Correct demo video link: https://youtu.be/Old2pqRtC70
- GitHub repo link: https://github.com/bullyopswork/tracepilot
- Clear note that raw proof JSON, secrets, and private Phoenix UI/account data are not public

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

Current status: **public URL verified for the earlier shell; upgraded safe interactive demo is local-only until redeployed after approval**.

Verification on 2026-05-13:

- Public HTTP check returned `200`.
- Live page contained expected TracePilot title/H1, Phoenix MCP wording, and Gemini/ADK wording.
- Browser snapshot confirmed the rendered page and public demo shell content.
