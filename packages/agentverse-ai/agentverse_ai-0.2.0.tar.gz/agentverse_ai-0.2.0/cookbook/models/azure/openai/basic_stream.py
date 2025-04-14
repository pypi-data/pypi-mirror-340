from typing import Iterator  # noqa

from agentverse_ai.agent import Agent, RunResponse  # noqa
from agentverse_ai.models.azure import AzureOpenAI

agent = Agent(model=AzureOpenAI(id="gpt-4o-mini"), markdown=True)

# Get the response in a variable
# run_response: Iterator[RunResponse] = agent.run("Share a 2 sentence horror story", stream=True)
# for chunk in run_response:
#     print(chunk.content)

# Print the response on the terminal
agent.print_response("Share a 2 sentence horror story", stream=True)
