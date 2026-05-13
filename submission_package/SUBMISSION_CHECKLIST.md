# TracePilot submission checklist

Use this before any public Devpost/GitHub/video action.

## Approval gate

- [ ] Ed/main explicitly approves public submission.
- [ ] Ed/main explicitly approves any GitHub publish/push if needed.
- [ ] Ed/main explicitly approves any Devpost submit/update action.
- [ ] Ed/main explicitly approves any deploy/hosted demo action if proposed.

Until all relevant approvals are granted, this package is **local prep only**.

## Required pre-public checks

- [ ] Re-read `public_release/RELEASE_MANIFEST.md` and `public_release/DEVPOST_REQUIREMENTS_MATRIX.md`.
- [ ] Re-read `submission_package/DEVPOST_DRAFT.md` for accuracy and tone.
- [ ] Confirm the proof story is represented honestly: `71/100 → 71/100 → 100/100`.
- [ ] Confirm latest fixed trace ID is correct: `52fa8eaf399d8cc4251a9e7f8441a903`.
- [ ] Confirm latest fixed artifact exists: `tracepilot_artifacts/20260513T120607Z/`.
- [ ] Confirm proof gate exists: `proof_gate/artifacts/20260513T120554Z/`.
- [ ] Confirm `tracepilot_artifacts/latest/before_after_report.md` matches the submission claims.
- [ ] Confirm `tracepilot_artifacts/latest/diagnosis.json` is valid JSON.
- [ ] Confirm README and draft clearly state the compact in-memory catalog/local proof boundary.
- [ ] Confirm no generated artifact or screenshot reveals credentials, private account details, or hidden `.env` values.

## Screenshot / video checklist

- [ ] Preferred upload candidate reviewed end-to-end: `demo_media_package/first_plus_phoenix/tracepilot_demo_first_plus_phoenix_fixed.mp4`.
- [ ] README: project summary, architecture, and local quickstart.
- [ ] `submission_package/PROOF_TABLE.md`: score progression table.
- [ ] `tracepilot_artifacts/latest/before_after_report.md`: check comparison and verdict.
- [ ] `tracepilot_artifacts/latest/diagnosis.json`: passed checks, trace ID, span/tool facts.
- [ ] `proof_gate/artifacts/20260513T120554Z/result.txt`: proof gate passed.
- [ ] Phoenix UI trace page, if safe and no credentials/account-private details are visible.
- [ ] Optional terminal capture of `make tracepilot-demo-local` only; this avoids extra Gemini/Phoenix calls during recording.

## Secret hygiene

Do not include any of the following in Devpost, README, screenshots, video, commit history, or chat:

- `.env` contents.
- API keys, OAuth tokens, bearer tokens, cookies, private URLs with tokens, or full credential filenames.
- Phoenix API keys or Google API keys.
- Raw terminal output that includes environment variables.
- Browser chrome showing private account or billing details.

Recommended local scan before publishing:

```bash
grep -RInE '(AIza[0-9A-Za-z_-]{20,}|sk-[0-9A-Za-z_-]{20,}|px_live_[0-9A-Za-z_-]+|Bearer[[:space:]]+[0-9A-Za-z._-]+|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})' README.md submission_package public_release web_demo tracepilot_artifacts/latest || true
```

Interpretation: the command should not print real secrets. Placeholder names such as `PHOENIX_API_KEY` are acceptable; real key-like values are not.

## Devpost content checklist

- [ ] Title: TracePilot.
- [ ] Tagline: Phoenix MCP-powered operator loop for self-debugging Gemini/ADK agents.
- [ ] Include the 71 → 71 → 100 proof narrative.
- [ ] Mention Arize/Phoenix/OpenInference/Phoenix MCP concretely.
- [ ] Mention Gemini/Google ADK concretely.
- [ ] Mention the local compact catalog boundary.
- [ ] Link/demo video only after approval.
- [ ] Keep claims to “proof slice/local operator loop” unless a public hosted demo exists.

## Post-approval publish sequence

0. Use `public_release/SUBMISSION_APPROVAL_GATE.md` as the controlling approval sequence.
1. Final local secret scan.
2. Final README/draft review.
3. Capture or attach demo video/screenshots.
4. If approved, publish/update GitHub.
5. If approved, submit/update Devpost.
6. Re-open public links in a clean browser/session and verify they do not expose secrets.
