"""
Async example using Mistral with tool calls.
"""

import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.mistral.mistral import MistralChat
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=MistralChat(id="mistral-large-latest"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)

asyncio.run(agent.aprint_response("Whats happening in France?", stream=True))
