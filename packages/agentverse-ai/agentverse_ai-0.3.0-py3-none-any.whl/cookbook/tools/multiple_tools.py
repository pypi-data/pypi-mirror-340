"""Run `pip install openai duckduckgo-search yfinance` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools
from agentverse_ai.tools.yfinance import YFinanceTools

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools(), YFinanceTools(enable_all=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response(
    "Write a thorough report on NVDA, get all financial information and latest news",
    stream=True,
)
