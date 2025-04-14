"""
Async example using DeepSeek with tool calls.
"""

import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.deepseek import DeepSeek
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=DeepSeek(id="deepseek-chat"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

asyncio.run(agent.aprint_response("Whats happening in France?", stream=True))
