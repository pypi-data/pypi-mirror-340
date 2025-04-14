"""Run `pip install duckduckgo-search sqlalchemy google.genai` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.models.google import Gemini
from agentverse_ai.storage.postgres import PostgresStorage
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    storage=PostgresStorage(table_name="agent_sessions", db_url=db_url),
    tools=[DuckDuckGoTools()],
    add_history_to_messages=True,
)
agent.print_response("How many people live in Canada?")
agent.print_response("What is their national anthem called?")
