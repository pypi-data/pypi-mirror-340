import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.models.litellm import LiteLLM
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools
from agentverse_ai.tools.yfinance import YFinanceTools

agent = Agent(
    model=LiteLLM(
        id="gpt-4o",
        name="LiteLLM",
    ),
    markdown=True,
    tools=[DuckDuckGoTools()],
)

# Ask a question that would likely trigger tool use
asyncio.run(agent.aprint_response("What is happening in France?"))
