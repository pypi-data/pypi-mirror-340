from agentverse_ai.agent import Agent, RunResponse  # noqa
from agentverse_ai.models.litellm import LiteLLMOpenAI

agent = Agent(model=LiteLLMOpenAI(id="gpt-4o"), markdown=True)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story")
# print(run.content)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story", stream=True)
