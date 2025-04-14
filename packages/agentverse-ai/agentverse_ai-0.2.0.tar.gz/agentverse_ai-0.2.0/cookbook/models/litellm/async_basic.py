import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.litellm import LiteLLM

openai_agent = Agent(
    model=LiteLLM(
        id="gpt-4o",
        name="LiteLLM",
    ),
    markdown=True,
)

asyncio.run(openai_agent.aprint_response("Share a 2 sentence horror story"))
