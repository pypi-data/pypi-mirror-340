from agentverse_ai.agent import Agent
from agentverse_ai.tools.newspaper import NewspaperTools

agent = Agent(tools=[NewspaperTools()])
agent.print_response("Please summarize https://en.wikipedia.org/wiki/Language_model")
