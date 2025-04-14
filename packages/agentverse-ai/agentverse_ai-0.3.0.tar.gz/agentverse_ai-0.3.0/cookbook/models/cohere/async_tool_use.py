"""
Async example using Cohere with tool calls.
"""

import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.cohere import Cohere
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Cohere(id="command-a-03-2025"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

asyncio.run(agent.aprint_response("Whats happening in France?", stream=True))
