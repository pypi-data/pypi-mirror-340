"""Run `pip install duckduckgo-search` to install dependencies."""

import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.ollama import OllamaTools
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OllamaTools(id="llama3.1:8b"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)
asyncio.run(agent.aprint_response("Whats happening in France?", stream=True))
