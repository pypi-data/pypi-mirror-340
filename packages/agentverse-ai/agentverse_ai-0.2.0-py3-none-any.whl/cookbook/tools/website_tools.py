from agentverse_ai.agent import Agent
from agentverse_ai.tools.website import WebsiteTools

agent = Agent(tools=[WebsiteTools()], show_tool_calls=True)
agent.print_response(
    "Search web page: 'https://docs.agentverse_ai.com/introduction'", markdown=True
)
