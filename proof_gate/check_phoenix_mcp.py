#!/usr/bin/env python3
"""Verify Phoenix MCP can retrieve the latest TracePilot trace.

This script intentionally prints and writes only redacted/safe proof metadata.
It never prints PHOENIX_API_KEY or other credentials.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import select
import subprocess
import sys
import time
from typing import Any


def load_dotenv(path: pathlib.Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def fail(message: str, code: int = 1) -> None:
    print(f"FAIL  Phoenix MCP — {message}")
    raise SystemExit(code)


class McpClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        env = os.environ.copy()
        self.proc = subprocess.Popen(
            [
                "npx",
                "-y",
                "@arizeai/phoenix-mcp@latest",
                "--baseUrl",
                base_url,
                "--apiKey",
                api_key,
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        self.next_id = 1

    def close(self) -> None:
        if self.proc.poll() is None:
            self.proc.kill()

    def send(self, method: str, params: dict[str, Any] | None = None, *, expect: bool = True) -> Any:
        msg: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        msg_id = None
        if expect:
            msg_id = self.next_id
            self.next_id += 1
            msg["id"] = msg_id
        if params is not None:
            msg["params"] = params
        assert self.proc.stdin is not None
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()
        if not expect:
            return None
        return self.read(msg_id)

    def read(self, msg_id: int, timeout_s: float = 25) -> dict[str, Any]:
        assert self.proc.stdout is not None
        assert self.proc.stderr is not None
        deadline = time.time() + timeout_s
        stderr_lines: list[str] = []
        while time.time() < deadline:
            ready, _, _ = select.select([self.proc.stdout, self.proc.stderr], [], [], 0.2)
            for stream in ready:
                line = stream.readline()
                if not line:
                    continue
                if stream is self.proc.stderr:
                    # Keep for debugging but never print unless there is no response.
                    stderr_lines.append(line.strip())
                    continue
                obj = json.loads(line)
                if obj.get("id") == msg_id:
                    return obj
        if stderr_lines:
            fail("server did not answer in time; stderr was non-empty")
        fail("server did not answer in time")


def extract_trace_ids(response: dict[str, Any]) -> list[str]:
    text = json.dumps(response)
    ids = re.findall(r'"trace_id"\s*:\s*"([0-9a-fA-F]{16,})"', text)
    if not ids:
        ids = re.findall(r"trace[_ ]id[^0-9a-fA-F]*([0-9a-fA-F]{16,})", text, flags=re.I)
    seen: list[str] = []
    for trace_id in ids:
        if trace_id not in seen:
            seen.append(trace_id)
    return seen


def safe_write(path: pathlib.Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def main() -> None:
    repo = pathlib.Path(__file__).resolve().parents[1]
    load_dotenv(repo / ".env")

    base_url = os.environ.get("PHOENIX_BASE_URL") or os.environ.get("PHOENIX_COLLECTOR_ENDPOINT")
    api_key = os.environ.get("PHOENIX_API_KEY")
    project = os.environ.get("PHOENIX_PROJECT_NAME", "tracepilot-proof")
    if not base_url:
        fail("PHOENIX_BASE_URL or PHOENIX_COLLECTOR_ENDPOINT missing")
    if not api_key:
        fail("PHOENIX_API_KEY missing")

    outdir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else repo / "proof_gate" / "artifacts" / "latest_mcp"
    outdir.mkdir(parents=True, exist_ok=True)

    client = McpClient(base_url=base_url, api_key=api_key)
    try:
        init = client.send(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "tracepilot-proof-gate", "version": "0.1"},
            },
        )
        client.send("notifications/initialized", expect=False)
        projects = client.send("tools/call", {"name": "list-projects", "arguments": {"limit": 20}})
        traces = client.send(
            "tools/call",
            {
                "name": "list-traces",
                "arguments": {"project_identifier": project, "limit": 5, "last_n_minutes": 60},
            },
        )
        trace_ids = extract_trace_ids(traces)
        if not trace_ids:
            safe_write(outdir / "phoenix_mcp_list_traces.json", traces)
            fail(f"no trace IDs returned for project {project!r}")
        trace = client.send(
            "tools/call",
            {
                "name": "get-trace",
                "arguments": {"project_identifier": project, "trace_id": trace_ids[0]},
            },
        )
        summary = {
            "mcp_server": "@arizeai/phoenix-mcp@latest",
            "project_identifier": project,
            "base_url_shape": re.sub(r"/s/[^/]+", "/s/<space>", base_url),
            "initialize_ok": "error" not in init,
            "list_projects_ok": "error" not in projects,
            "list_traces_ok": "error" not in traces,
            "latest_trace_id": trace_ids[0],
            "trace_ids_found": trace_ids[:5],
            "get_trace_ok": "error" not in trace,
        }
        safe_write(outdir / "phoenix_mcp_summary.json", summary)
        safe_write(outdir / "phoenix_mcp_list_projects.json", projects)
        safe_write(outdir / "phoenix_mcp_list_traces.json", traces)
        safe_write(outdir / "phoenix_mcp_get_trace.json", trace)
        if not all(summary[k] for k in ["initialize_ok", "list_projects_ok", "list_traces_ok", "get_trace_ok"]):
            fail("one or more MCP calls returned an error")
        print("PASS  Phoenix MCP — latest trace retrieved")
        print(f"project={project}")
        print(f"latest_trace_id={trace_ids[0]}")
        print(f"artifacts={outdir}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
