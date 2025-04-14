from agentverse_ai.agent import Agent
from agentverse_ai.models.litellm import LiteLLM
from agentverse_ai.storage.sqlite import SqliteStorage
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

# Create a storage backend using the Sqlite database
storage = SqliteStorage(
    # store sessions in the ai.sessions table
    table_name="agent_sessions_storage",
    # db_file: Sqlite database file
    db_file="tmp/data.db",
)

# Add storage to the Agent
agent = Agent(
    model=LiteLLM(id="gpt-4o"),
    storage=storage,
    tools=[DuckDuckGoTools()],
    add_history_to_messages=True,
)

agent.print_response("How many people live in Canada?")
agent.print_response("What is their national anthem called?")
