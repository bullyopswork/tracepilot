# TracePilot submission approval gate

No external action is authorized by this file. It defines the required sequence before public GitHub, video, hosting, or Devpost actions.

## Gate 0 — local package review

- [ ] Main verifies canonical proof remains `52fa8eaf399d8cc4251a9e7f8441a903` / `proof_gate/artifacts/20260513T120554Z/` / `tracepilot_artifacts/20260513T120607Z/`.
- [ ] Lens reviews `public_release/`, `submission_package/`, and `web_demo/`.
- [ ] Main confirms accidental proof artifact `20260513T125917Z` is not public/canonical.

## Gate 1 — public repo approval

- [ ] Run `public_release/PUBLIC_REPO_CHECKLIST.md` commands.
- [ ] Review all staged/changed files exactly.
- [ ] Confirm `.env` remains ignored and absent from staged/public files.
- [ ] Ed/main explicitly approves public GitHub publication.

## Gate 2 — video approval

- [ ] Review `demo_media_package/first_plus_phoenix/tracepilot_demo_first_plus_phoenix_fixed.mp4` end-to-end.
- [ ] Confirm no secrets, account-private details, or misleading claims appear.
- [ ] Ed/main explicitly approves YouTube/Vimeo upload.
- [ ] After upload, verify public link in clean browser/session.

## Gate 3 — hosted web approval

- [ ] Review local `web_demo/` in browser.
- [ ] Choose hosting path: static host/Firebase/Cloud Run.
- [ ] Run final secret/path scan on deploy folder.
- [ ] Ed/main explicitly approves deploy.
- [ ] After deploy, verify hosted URL in clean browser/session.

## Gate 4 — Devpost approval

- [ ] Confirm required public links exist: hosted project URL, public repo, public demo video.
- [ ] Re-read `submission_package/DEVPOST_DRAFT.md` and `public_release/DEVPOST_REQUIREMENTS_MATRIX.md`.
- [ ] Confirm track selection and Agent Builder wording are acceptable.
- [ ] Ed/main explicitly approves Devpost submit/update.
- [ ] Submit/update once; then reopen public page and verify links/content.
