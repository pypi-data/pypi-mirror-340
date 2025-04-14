"""Run `pip install duckduckgo-search sqlalchemy groq` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.models.groq import Groq
from agentverse_ai.storage.postgres import PostgresStorage
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    storage=PostgresStorage(table_name="agent_sessions", db_url=db_url),
    tools=[DuckDuckGoTools()],
    add_history_to_messages=True,
)
agent.print_response("How many people live in Canada?")
agent.print_response("What is their national anthem called?")
