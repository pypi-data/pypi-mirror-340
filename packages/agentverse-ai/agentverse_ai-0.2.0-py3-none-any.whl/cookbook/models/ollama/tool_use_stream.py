"""Run `pip install duckduckgo-search` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.models.ollama import Ollama
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Ollama(id="llama3.1:8b"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response("Whats happening in France?", stream=True)
