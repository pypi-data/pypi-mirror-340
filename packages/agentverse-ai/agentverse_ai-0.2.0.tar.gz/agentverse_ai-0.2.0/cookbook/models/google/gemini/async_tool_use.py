"""
Async example using Gemini with tool calls.
"""

import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.google import Gemini
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

asyncio.run(agent.aprint_response("Whats happening in France?", stream=True))
