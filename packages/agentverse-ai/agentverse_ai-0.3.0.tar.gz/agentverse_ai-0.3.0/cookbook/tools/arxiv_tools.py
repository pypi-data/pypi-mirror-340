from agentverse_ai.agent import Agent
from agentverse_ai.tools.arxiv import ArxivTools

agent = Agent(tools=[ArxivTools()], show_tool_calls=True)
agent.print_response("Search arxiv for 'language models'", markdown=True)
