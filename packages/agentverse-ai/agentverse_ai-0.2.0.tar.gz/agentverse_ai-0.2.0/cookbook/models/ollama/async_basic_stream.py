import asyncio
from typing import Iterator  # noqa

from agentverse_ai.agent import Agent, RunResponse  # noqa
from agentverse_ai.models.ollama import Ollama

agent = Agent(model=Ollama(id="llama3.1:8b"), markdown=True)

# Get the response in a variable
# run_response: Iterator[RunResponse] = agent.run("Share a 2 sentence horror story", stream=True)
# for chunk in run_response:
#     print(chunk.content)

# Print the response in the terminal
asyncio.run(agent.aprint_response("Share a 2 sentence horror story", stream=True))
