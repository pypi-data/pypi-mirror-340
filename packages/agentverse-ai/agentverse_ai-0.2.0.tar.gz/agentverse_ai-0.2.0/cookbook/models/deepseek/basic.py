from agentverse_ai.agent import Agent, RunResponse  # noqa
from agentverse_ai.models.deepseek import DeepSeek

agent = Agent(model=DeepSeek(id="deepseek-chat"), markdown=True)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story")
# print(run.content)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story")
