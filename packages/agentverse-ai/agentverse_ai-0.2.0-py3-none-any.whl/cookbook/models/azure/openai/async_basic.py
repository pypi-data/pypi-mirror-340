import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.azure import AzureOpenAI

agent = Agent(
    model=AzureOpenAI(id="gpt-4o-mini"),
    description="You help people with their health and fitness goals.",
    instructions=["Recipes should be under 5 ingredients"],
)
# -*- Print a response to the cli
asyncio.run(agent.aprint_response("Share a breakfast recipe.", markdown=True))
