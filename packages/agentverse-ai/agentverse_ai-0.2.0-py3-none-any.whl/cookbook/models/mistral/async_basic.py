"""
Basic async example using Mistral.
"""

import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.mistral.mistral import MistralChat

agent = Agent(
    model=MistralChat(id="mistral-large-latest"),
    markdown=True,
)

asyncio.run(agent.aprint_response("Share a 2 sentence horror story"))
