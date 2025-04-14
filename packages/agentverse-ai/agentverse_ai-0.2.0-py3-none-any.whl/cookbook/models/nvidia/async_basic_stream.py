"""
Basic streaming async example using Nvidia.
"""

import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.nvidia import Nvidia

agent = Agent(model=Nvidia(id="meta/llama-3.3-70b-instruct"), markdown=True)

asyncio.run(agent.aprint_response("Share a 2 sentence horror story", stream=True))
