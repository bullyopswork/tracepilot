#!/usr/bin/env python3
"""Preflight for the real TracePilot Arize proof gate.

No secret values are printed. This checks whether the machine is ready to run:
Google ADK/Gemini -> Phoenix tracing -> Phoenix MCP inspection.
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def present(key: str) -> bool:
    value = os.environ.get(key, "").strip()
    return bool(value and not value.startswith("<"))


def status_line(ok: bool, name: str, detail: str = "") -> str:
    return f"{'PASS' if ok else 'FAIL'}  {name}{' — ' + detail if detail else ''}"


def main() -> int:
    load_dotenv(ENV_PATH)
    failures: list[str] = []

    print("TracePilot real-stack preflight")
    print(f"repo={ROOT}")
    print(f"env_file={'present' if ENV_PATH.exists() else 'missing'}")
    print()

    python_ok = sys.version_info >= (3, 10) and sys.version_info < (3, 13)
    print(status_line(python_ok, "Python 3.10-3.12", sys.version.split()[0]))
    if not python_ok:
        failures.append("Use Python 3.10-3.12 for google-adk starter.")

    for module in ["google.adk", "google.genai", "phoenix.otel", "openinference.instrumentation.google_adk"]:
        ok = importlib.util.find_spec(module) is not None
        print(status_line(ok, f"import {module}"))
        if not ok:
            failures.append(f"Missing Python package/module: {module}. Run venv install first.")

    gemini_auth = present("GOOGLE_API_KEY") or (
        present("GOOGLE_GENAI_USE_VERTEXAI") and present("GOOGLE_CLOUD_PROJECT") and present("GOOGLE_CLOUD_LOCATION")
    )
    print(status_line(gemini_auth, "Gemini auth", "GOOGLE_API_KEY or Vertex project/location"))
    if not gemini_auth:
        failures.append("Set GOOGLE_API_KEY, or set GOOGLE_GENAI_USE_VERTEXAI=1 plus GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION.")

    phoenix_key = present("PHOENIX_API_KEY")
    phoenix_endpoint = present("PHOENIX_COLLECTOR_ENDPOINT") or present("PHOENIX_BASE_URL") or present("OTEL_EXPORTER_OTLP_ENDPOINT")
    endpoint_value = os.environ.get("PHOENIX_COLLECTOR_ENDPOINT") or os.environ.get("PHOENIX_BASE_URL") or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT") or ""
    endpoint_shape = bool(endpoint_value.startswith("https://") and "/s/" in endpoint_value)
    print(status_line(phoenix_key, "Phoenix API key", "value hidden" if phoenix_key else "missing"))
    print(status_line(phoenix_endpoint, "Phoenix endpoint", "value hidden" if phoenix_endpoint else "missing"))
    print(status_line(endpoint_shape, "Phoenix Cloud endpoint shape", "should look like https://app.phoenix.arize.com/s/<space>"))
    if not phoenix_key:
        failures.append("Set PHOENIX_API_KEY in .env or shell; do not paste it into chat.")
    if not phoenix_endpoint:
        failures.append("Set PHOENIX_COLLECTOR_ENDPOINT to the Phoenix Cloud space hostname.")
    elif not endpoint_shape:
        failures.append("Phoenix endpoint should include /s/<space>; bare app.phoenix.arize.com often 401s.")

    for bin_name in ["node", "npm", "npx"]:
        ok = shutil.which(bin_name) is not None
        print(status_line(ok, f"binary {bin_name}", shutil.which(bin_name) or "missing"))
        if not ok:
            failures.append(f"Install/enable {bin_name} for Phoenix MCP/Gemini CLI path.")

    print()
    if failures:
        print("BLOCKED — real proof gate not ready:")
        for item in failures:
            print(f"- {item}")
        return 2
    print("READY — run proof_gate/run_real_gemini_phoenix_gate.sh next.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
