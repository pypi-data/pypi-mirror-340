from agentverse_ai.agent import Agent
from agentverse_ai.tools.crawl4ai import Crawl4aiTools

agent = Agent(tools=[Crawl4aiTools(max_length=None)], show_tool_calls=True)
agent.print_response("Tell me about https://github.com/agentverse_ai-agi/agentverse_ai.")
