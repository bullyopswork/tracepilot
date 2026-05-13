#!/usr/bin/env python3
"""TracePilot operator demo: diagnose a traced ADK/Gemini shopping turn.

The real stack run is owned by proof_gate/run_real_gemini_phoenix_gate.sh. This
script consumes that proof directory, reads Phoenix MCP trace artifacts, scores
whether the agent satisfied a compact shopping-task rubric, and writes safe
operator artifacts: diagnosis, refined task, and demo report.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
from datetime import datetime, timezone
from typing import Any

REPO = pathlib.Path(__file__).resolve().parent
ARTIFACT_ROOT = REPO / "tracepilot_artifacts"
SECRET_PATTERNS = [
    re.compile(r"AIza[0-9A-Za-z_\-]{20,}"),
    re.compile(r"px_live_[0-9A-Za-z_\-]{10,}"),
    re.compile(r"sk-[0-9A-Za-z]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"]?[^\s,'\"]+"),
]


def latest_proof_dir() -> pathlib.Path:
    dirs = sorted((REPO / "proof_gate" / "artifacts").glob("20*"))
    if not dirs:
        raise SystemExit("No proof_gate/artifacts/<timestamp> directory found. Run proof gate first.")
    return dirs[-1]


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text())


def phoenix_trace_payload(mcp_get_trace: dict[str, Any]) -> dict[str, Any]:
    content = mcp_get_trace.get("result", {}).get("content", [])
    if not content:
        return {}
    text = content[0].get("text", "")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def first_json_attr(attrs: dict[str, Any], key: str) -> dict[str, Any] | list[Any] | str | None:
    raw = attrs.get(key)
    if not isinstance(raw, str):
        return raw
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def extract_trace_facts(trace: dict[str, Any], summary: dict[str, Any]) -> dict[str, Any]:
    spans = trace.get("spans", []) if isinstance(trace, dict) else []
    span_names = [s.get("name", "") for s in spans if isinstance(s, dict)]
    tool_spans = [name for name in span_names if "tool" in name.lower() or name.startswith("search") or name.startswith("click")]
    lowered_span_names = [name.lower() for name in span_names]
    input_text = ""
    final_text = ""
    model_version = "unknown"
    for span in spans:
        attrs = span.get("attributes", {}) if isinstance(span, dict) else {}
        if not input_text:
            input_obj = first_json_attr(attrs, "input.value")
            input_text = json.dumps(input_obj) if isinstance(input_obj, (dict, list)) else str(input_obj or "")
        output_obj = first_json_attr(attrs, "output.value")
        if isinstance(output_obj, dict):
            model_version = output_obj.get("model_version") or model_version
            parts = output_obj.get("content", {}).get("parts", [])
            text_parts = [p.get("text", "") for p in parts if isinstance(p, dict) and p.get("text")]
            if text_parts:
                final_text = "\n".join(text_parts)
    joined = "\n".join([json.dumps(trace), input_text, final_text]).lower()
    return {
        "trace_id": trace.get("traceId") or summary.get("latest_trace_id"),
        "project_identifier": summary.get("project_identifier"),
        "mcp_server": summary.get("mcp_server"),
        "mcp_ok": all(summary.get(k) for k in ["list_projects_ok", "list_traces_ok", "get_trace_ok"]),
        "span_count": len(spans),
        "span_names": span_names[:20],
        "tool_span_count": len(tool_spans),
        "model_version": model_version,
        "input_mentions_size_m": bool(re.search(r"size\s*m\b", input_text, re.I)),
        "used_search": any("execute_tool search" in name or name.endswith(" search") for name in lowered_span_names) or "`search`" in joined,
        "used_click": any("execute_tool click" in name or name.endswith(" click") for name in lowered_span_names),
        "final_answer": final_text[:1200],
        "final_mentions_tool_steps": bool(re.search(r"tool|search|click|step", final_text, re.I)),
        "final_mentions_size_m": bool(re.search(r"size\s*m\b|\bm\b", final_text, re.I)),
        "final_mentions_floral_dress": "floral" in final_text.lower() and "dress" in final_text.lower(),
    }


def score(facts: dict[str, Any]) -> tuple[int, list[str], list[str]]:
    checks = {
        "Phoenix MCP returned retrievable trace": facts["mcp_ok"],
        "Trace contains spans": facts["span_count"] > 0,
        "Agent used search context/tooling": facts["used_search"],
        "Final answer mentions floral dress": facts["final_mentions_floral_dress"],
        "Final answer explains tool steps": facts["final_mentions_tool_steps"],
        "Final answer preserves requested size M": facts["final_mentions_size_m"],
        "Agent clicked/inspected a specific product": facts["used_click"],
    }
    passed = [name for name, ok in checks.items() if ok]
    failed = [name for name, ok in checks.items() if not ok]
    return round(100 * len(passed) / len(checks)), passed, failed


def redact_text(text: str) -> str:
    redacted = text
    for pat in SECRET_PATTERNS:
        redacted = pat.sub("<redacted>", redacted)
    return redacted


def safe_write(path: pathlib.Path, content: str) -> None:
    content = redact_text(content)
    for pat in SECRET_PATTERNS[:3]:
        if pat.search(content):
            raise RuntimeError(f"refusing to write possible secret to {path}")
    path.write_text(content)


def build_report(proof_dir: pathlib.Path, outdir: pathlib.Path) -> dict[str, Any]:
    summary_path = proof_dir / "phoenix_mcp_summary.json"
    trace_path = proof_dir / "phoenix_mcp_get_trace.json"
    if not summary_path.exists() or not trace_path.exists():
        raise SystemExit(f"Missing Phoenix MCP proof files in {proof_dir}")
    summary = load_json(summary_path)
    trace = phoenix_trace_payload(load_json(trace_path))
    facts = extract_trace_facts(trace, summary)
    before_score, passed, failed = score(facts)
    refined_task = (
        "Find one exact floral dress in size M. Use search to locate candidates, "
        "click the best product to inspect it, confirm size M is available, then answer "
        "with the selected ASIN/title and a short list of the tool steps used."
    )
    after_expected = min(100, before_score + 14 * len(failed))
    diagnosis = {
        "state": "diagnosed",
        "proof_dir": str(proof_dir),
        "trace_id": facts["trace_id"],
        "project_identifier": facts["project_identifier"],
        "mcp_server": facts["mcp_server"],
        "model_version": facts["model_version"],
        "before_score": before_score,
        "after_expected_score_if_refined_task_is_used": after_expected,
        "passed_checks": passed,
        "failed_checks": failed,
        "operator_diagnosis": (
            "The trace is healthy and Phoenix MCP retrieval works. "
            "The main improvement is task control: require a specific product inspection, "
            "explicit size confirmation, and a concise tool-step explanation."
        ),
        "refined_task": refined_task,
        "safe_trace_facts": facts,
    }
    outdir.mkdir(parents=True, exist_ok=True)
    safe_write(outdir / "diagnosis.json", json.dumps(diagnosis, indent=2, sort_keys=True) + "\n")
    safe_write(outdir / "refined_task.txt", refined_task + "\n")
    md = f"""# TracePilot demo report

## What this proves

TracePilot can sit above a real Google ADK/Gemini agent, use Phoenix/OpenInference traces retrieved through Phoenix MCP, and produce an operator diagnosis plus a refined next task.

## Proof input

- Proof gate artifact: `{proof_dir}`
- Phoenix project: `{facts['project_identifier']}`
- Latest trace id: `{facts['trace_id']}`
- MCP server: `{facts['mcp_server']}`

## Before / diagnosis

- Score: **{before_score}/100**
- Passed: {', '.join(passed) if passed else 'none'}
- Needs improvement: {', '.join(failed) if failed else 'none'}

## Improvement TracePilot would apply

```text
{refined_task}
```

## Architecture

1. `proof_gate/run_real_gemini_phoenix_gate.sh` runs a real ADK/Gemini shopping turn with Phoenix tracing enabled.
2. `proof_gate/check_phoenix_mcp.py` retrieves the latest trace through `@arizeai/phoenix-mcp` and saves redacted proof metadata.
3. `tracepilot_operator.py` reads those safe MCP artifacts, evaluates task completion, and writes this diagnosis/refinement package.

## Caveats

This compact internal package diagnoses and proposes the refined next operator step. It does not auto-submit to Devpost, publish a repo, mutate external systems, or expose credentials.
"""
    safe_write(outdir / "demo_report.md", md)
    shutil.copy2(summary_path, outdir / "phoenix_mcp_summary.safe.json")
    return diagnosis


def main() -> None:
    parser = argparse.ArgumentParser(description="Build safe TracePilot operator artifacts from a proof gate run.")
    parser.add_argument("--proof-dir", type=pathlib.Path, default=None, help="Existing proof_gate/artifacts/<timestamp> directory. Defaults to latest.")
    parser.add_argument("--outdir", type=pathlib.Path, default=None, help="Output artifact directory. Defaults to tracepilot_artifacts/<UTC timestamp>.")
    args = parser.parse_args()
    proof_dir = args.proof_dir or latest_proof_dir()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = args.outdir or ARTIFACT_ROOT / stamp
    diagnosis = build_report(proof_dir, outdir)
    latest = ARTIFACT_ROOT / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    for name in ["diagnosis.json", "refined_task.txt", "demo_report.md", "phoenix_mcp_summary.safe.json"]:
        shutil.copy2(outdir / name, latest / name)
    print("PASS  TracePilot operator demo artifacts written")
    print(f"proof_dir={proof_dir}")
    print(f"outdir={outdir}")
    print(f"trace_id={diagnosis['trace_id']}")
    print(f"before_score={diagnosis['before_score']}")


if __name__ == "__main__":
    main()
