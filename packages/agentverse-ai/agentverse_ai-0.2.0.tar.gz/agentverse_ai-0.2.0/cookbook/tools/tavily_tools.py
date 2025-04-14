from agentverse_ai.agent import Agent
from agentverse_ai.tools.tavily import TavilyTools

agent = Agent(tools=[TavilyTools()], show_tool_calls=True)
agent.print_response("Search tavily for 'language models'", markdown=True)
