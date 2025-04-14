from typing import Iterator

from agentverse_ai.agent import Agent, RunResponse
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.tools.yfinance import YFinanceTools
from rich.pretty import pprint

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True)],
    markdown=True,
    show_tool_calls=True,
)

run_stream: Iterator[RunResponse] = agent.run(
    "What is the stock price of NVDA", stream=True, stream_intermediate_steps=True
)
for chunk in run_stream:
    pprint(chunk.to_dict())
    print("---" * 20)
