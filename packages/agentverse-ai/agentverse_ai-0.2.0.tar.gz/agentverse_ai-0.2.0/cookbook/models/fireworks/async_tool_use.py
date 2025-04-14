"""
Async example using Fireworks with tool calls.
"""

import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.fireworks import Fireworks
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Fireworks(id="accounts/fireworks/models/llama-v3p1-405b-instruct"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

asyncio.run(agent.aprint_response("Whats happening in France?", stream=True))
