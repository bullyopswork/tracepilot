# TracePilot public repo checklist

Use this before creating or updating any public GitHub repo.

## Include

- [ ] `README.md`
- [ ] `LICENSE` with visible OSI license text (current: Apache-2.0)
- [ ] `.gitignore`
- [ ] `.env.example` placeholders only
- [ ] `pyproject.toml`, `uv.lock`, `Makefile`
- [ ] `agent/` source code
- [ ] `proof_gate/` scripts/README, excluding unsafe generated artifacts
- [ ] `tracepilot_operator.py`
- [ ] `submission_package/` reviewed markdown docs
- [ ] `public_release/` reviewed markdown docs
- [ ] `web_demo/` static shell
- [ ] Approved demo media only if repo storage policy allows it; otherwise upload video to YouTube/Vimeo and link it from Devpost

## Exclude

- [ ] `.env` (already ignored)
- [ ] `.venv/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`
- [ ] `.adk/`, `agent/**/.adk/`, `.arize-tmp-traces/`
- [ ] Raw `proof_gate/artifacts/*/phoenix_mcp_get_trace.json`
- [ ] Any raw proof JSON with verbose internal trace/model/span details unless sanitized and explicitly approved
- [ ] Accidental proof artifact `proof_gate/artifacts/20260513T125917Z/` and trace `9e312aec...` from public claims
- [ ] Phoenix screenshots/crops unless manually reviewed
- [ ] Secret-bearing files, private account URLs, credential filenames, billing/account screenshots

## Required review commands

```bash
git status --short
git diff -- . ':!*.mp4' ':!*.png' ':!*.jpg' ':!*.aiff'
git ls-files --others --exclude-standard
```

Secret-shape scan for planned public files:

```bash
grep -RInE '(AIza[0-9A-Za-z_-]{20,}|sk-[0-9A-Za-z_-]{20,}|px_live_[0-9A-Za-z_-]+|Bearer[[:space:]]+[0-9A-Za-z._-]+|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})' README.md .env.example pyproject.toml Makefile agent proof_gate submission_package public_release web_demo tracepilot_operator.py || true
```

Interpretation: placeholders such as `GOOGLE_API_KEY`, `PHOENIX_API_KEY`, and `px_live_...` in docs are acceptable. Real values are not.

## Staged-file review gate

Non-mutating first pass before push/publication:

```bash
git diff --name-only
git ls-files --others --exclude-standard
```

Only after Ed/main explicitly approves preparing a commit, stage the exact approved files and inspect:

```bash
git add <approved-file-or-dir> ...
git diff --cached --name-only
git diff --cached -- . ':!*.mp4' ':!*.png' ':!*.jpg' ':!*.aiff'
```

Then manually inspect every staged file. Public GitHub action requires explicit Ed/main approval after this review.
