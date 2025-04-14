"""
Basic streaming async example using Claude.
"""

import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.anthropic import Claude

agent = Agent(
    model=Claude(id="claude-3-5-sonnet-20240620"),
    markdown=True,
)

asyncio.run(agent.aprint_response("Share a 2 sentence horror story", stream=True))
