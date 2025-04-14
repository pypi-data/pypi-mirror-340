"""Run `pip install duckduckgo-search` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.models.litellm import LiteLLMOpenAI
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=LiteLLMOpenAI(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response("Whats happening in France?")
