"""Run `pip install yfinance` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.models.google import Gemini
from agentverse_ai.tools.yfinance import YFinanceTools

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[YFinanceTools()],
    add_history_to_messages=True,
    num_history_responses=5,
    show_tool_calls=True,
    markdown=True,
)
agent.print_response("What is the price of TSLA and of NVDA?", stream=True)

agent.print_response("What is the price of AAPL?", stream=True)

agent.print_response("Summarize the conversation so far.", stream=True)
