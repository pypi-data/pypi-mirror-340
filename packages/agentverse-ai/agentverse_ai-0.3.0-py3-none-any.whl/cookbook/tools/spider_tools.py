from agentverse_ai.agent import Agent
from agentverse_ai.tools.spider import SpiderTools

agent = Agent(tools=[SpiderTools(optional_params={"proxy_enabled": True})])
agent.print_response(
    'Can you scrape the first search result from a search on "news in USA"?'
)
