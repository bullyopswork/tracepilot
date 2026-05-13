#!/usr/bin/env python3
"""Local static/runtime proof that TracePilot is wired as an ADK multi-agent app.

This check does not call Gemini, Phoenix, Devpost, GitHub, or any other external
service. It validates the local ADK agent graph shape only.
"""

from __future__ import annotations

import ast
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENT_FILE = REPO_ROOT / "agent" / "shopping_demo" / "agent.py"


def _agent_assignments(tree: ast.AST) -> dict[str, ast.Call]:
    assignments: dict[str, ast.Call] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Call):
            continue
        func = node.value.func
        if not isinstance(func, ast.Name) or func.id != "Agent":
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                assignments[target.id] = node.value
    return assignments


def _keyword_names(call: ast.Call, keyword: str) -> list[str]:
    for kw in call.keywords:
        if kw.arg != keyword or not isinstance(kw.value, ast.List):
            continue
        names: list[str] = []
        for item in kw.value.elts:
            if isinstance(item, ast.Name):
                names.append(item.id)
        return names
    return []


def static_check() -> list[str]:
    tree = ast.parse(AGENT_FILE.read_text(), filename=str(AGENT_FILE))
    agents = _agent_assignments(tree)
    root = agents.get("root_agent")
    if root is None:
        raise AssertionError("root_agent = Agent(...) not found")
    sub_agent_names = _keyword_names(root, "sub_agents")
    if len(agents) < 3:
        raise AssertionError(f"expected >=3 Agent(...) assignments, found {sorted(agents)}")
    if len(sub_agent_names) < 2:
        raise AssertionError(f"expected root_agent.sub_agents to wire >=2 agents, found {sub_agent_names}")
    missing = [name for name in sub_agent_names if name not in agents]
    if missing:
        raise AssertionError(f"root_agent.sub_agents references non-Agent names: {missing}")
    return sub_agent_names


def runtime_check(expected_sub_agents: list[str]) -> None:
    # Keep imports side-effect-local: disable Phoenix registration even if .env
    # contains credentials, and only inspect the in-memory agent graph.
    os.environ["PHOENIX_API_KEY"] = ""
    sys.path.insert(0, str(REPO_ROOT / "agent"))
    from shopping_demo.agent import root_agent  # noqa: PLC0415

    names = [agent.name for agent in root_agent.sub_agents]
    expected_runtime_names = {
        "product_selection_agent",
        "purchase_verification_agent",
    }
    if len(names) < 2:
        raise AssertionError(f"runtime root_agent has too few sub_agents: {names}")
    if not expected_runtime_names.issubset(names):
        raise AssertionError(
            f"runtime sub_agents {names} missing expected {sorted(expected_runtime_names)}"
        )
    if len(expected_sub_agents) != len(names):
        raise AssertionError(
            f"static sub_agent refs {expected_sub_agents} differ from runtime names {names}"
        )


def main() -> None:
    sub_agent_refs = static_check()
    runtime_check(sub_agent_refs)
    print(
        "MULTI_AGENT_READY: root_agent wires ADK sub_agents "
        f"{', '.join(sub_agent_refs)}"
    )


if __name__ == "__main__":
    main()
