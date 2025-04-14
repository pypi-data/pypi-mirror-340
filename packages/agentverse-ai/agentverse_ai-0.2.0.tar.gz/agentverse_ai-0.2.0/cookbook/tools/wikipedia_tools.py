from agentverse_ai.agent import Agent
from agentverse_ai.tools.wikipedia import WikipediaTools

agent = Agent(tools=[WikipediaTools()], show_tool_calls=True)
agent.print_response("Search wikipedia for 'ai'")
