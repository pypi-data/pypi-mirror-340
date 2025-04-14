"""Run `pip install duckduckgo-search openai` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.storage.json import JsonStorage
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    storage=JsonStorage(dir_path="tmp/agent_sessions_json"),
    tools=[DuckDuckGoTools()],
    add_history_to_messages=True,
)
agent.print_response("How many people live in Canada?")
agent.print_response("What is their national anthem called?")
