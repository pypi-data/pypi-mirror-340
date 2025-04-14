from agentverse_ai.agent import Agent
from agentverse_ai.tools.sql import SQLTools

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

agent = Agent(tools=[SQLTools(db_url=db_url)])
agent.print_response(
    "List the tables in the database. Tell me about contents of one of the tables",
    markdown=True,
)
