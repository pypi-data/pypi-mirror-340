from agentverse_ai.agent import Agent, RunResponse  # noqa
from agentverse_ai.models.aws import AwsBedrock

agent = Agent(model=AwsBedrock(id="mistral.mistral-small-2402-v1:0"), markdown=True)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story")
# print(run.content)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story")
