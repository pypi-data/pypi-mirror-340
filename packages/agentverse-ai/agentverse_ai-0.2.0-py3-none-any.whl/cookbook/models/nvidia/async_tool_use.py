"""
Async example using Mistral with tool calls.
"""

import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.nvidia import Nvidia
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Nvidia(id="meta/llama-3.3-70b-instruct"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)

asyncio.run(agent.aprint_response("Whats happening in France?", stream=True))
