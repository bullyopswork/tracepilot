# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""TracePilot ADK multi-agent shopping demo.

The root coordinator keeps the direct search/click tools that produced the
verified completion-fix run, and wires two ADK specialist sub-agents so the demo
is defensibly a multi-agent ADK system instead of a single standalone tool user.
"""

import os
from pathlib import Path

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv

from instrumentation import setup_tracing
from shopping_demo.prompt import (
    product_selection_agent_instruction,
    purchase_verification_agent_instruction,
    tracepilot_coordinator_instruction,
)
from shopping_demo.tools.click import click
from shopping_demo.tools.search import search

# Ensure ADK CLI runs (`adk run shopping_demo`) load local env and tracing.
load_dotenv(Path(__file__).resolve().parents[2] / ".env")
setup_tracing()

_model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

product_selection_agent = Agent(
    model=_model,
    name="product_selection_agent",
    description="Searches the demo webshop and selects the best product candidate.",
    instruction=product_selection_agent_instruction,
    tools=[FunctionTool(func=search)],
)

purchase_verification_agent = Agent(
    model=_model,
    name="purchase_verification_agent",
    description="Inspects product pages and verifies requested options before final answers.",
    instruction=purchase_verification_agent_instruction,
    tools=[FunctionTool(func=click)],
)

root_agent = Agent(
    model=_model,
    name="personalized_shopping_agent",
    description="Coordinates specialist ADK agents for webshop search, selection, and verification.",
    instruction=tracepilot_coordinator_instruction,
    tools=[
        # Keep these direct tools on the coordinator to preserve the proven
        # one-turn completion-fix behavior; sub-agents expose the same work as
        # explicit ADK specialist agents for multi-agent orchestration.
        FunctionTool(func=search),
        FunctionTool(func=click),
    ],
    sub_agents=[
        product_selection_agent,
        purchase_verification_agent,
    ],
)
