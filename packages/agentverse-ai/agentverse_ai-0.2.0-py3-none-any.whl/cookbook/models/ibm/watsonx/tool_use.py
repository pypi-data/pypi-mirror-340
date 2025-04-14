"""Run `pip install duckduckgo-search` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.models.ibm import WatsonX
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=WatsonX(id="meta-llama/llama-3-3-70b-instruct"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response("Whats happening in France?", stream=True)
