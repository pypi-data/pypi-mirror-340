"""Build a Web Search Agent using xAI."""

from agentverse_ai.agent import Agent
from agentverse_ai.models.xai import xAI
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=xAI(id="grok-beta"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response("Whats happening in France?", stream=True)
