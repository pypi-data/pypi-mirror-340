import asyncio

from agentverse_ai.agent import Agent, RunResponse  # noqa
from agentverse_ai.models.xai import xAI

agent = Agent(model=xAI(id="grok-beta"), markdown=True)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story")
# print(run.content)

# Print the response in the terminal
asyncio.run(agent.aprint_response("Share a 2 sentence horror story"))
