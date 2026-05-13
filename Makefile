.PHONY: setup run run-adk tracepilot-demo tracepilot-demo-local help

help:
	@echo "Targets:"
	@echo "  make setup   - uv sync + remind to copy .env"
	@echo "  make run     - one-shot traced run (MESSAGE=...)"
	@echo "  make run-adk - ADK CLI dev loop (cd agent && adk run shopping_demo)"
	@echo "  make tracepilot-demo - run real proof gate, then write TracePilot artifacts"
	@echo "  make tracepilot-demo-local - analyze latest proof artifacts without a new Gemini run"

setup:
	uv sync
	@test -f .env || echo "Tip: copy .env.example to .env and add keys."

run:
	cd agent && uv run python main.py "$(if $(MESSAGE),$(MESSAGE),Help me find a floral summer dress and buy size M.)"

run-adk:
	cd agent && uv run adk run shopping_demo

tracepilot-demo:
	proof_gate/run_tracepilot_demo.sh

tracepilot-demo-local:
	TRACEPILOT_SKIP_REAL_GATE=1 proof_gate/run_tracepilot_demo.sh
