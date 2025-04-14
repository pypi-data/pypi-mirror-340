from agentverse_ai.agent import Agent
from agentverse_ai.tools.apify import ApifyTools

agent = Agent(tools=[ApifyTools()], show_tool_calls=True)
agent.print_response("Tell me about https://docs.agentverse_ai.com/introduction", markdown=True)
