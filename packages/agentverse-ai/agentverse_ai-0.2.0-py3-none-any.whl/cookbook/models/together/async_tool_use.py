"""Run `pip install duckduckgo-search` to install dependencies."""

import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.together import Together
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Together(id="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)
asyncio.run(agent.aprint_response("Whats happening in France?", stream=True))
