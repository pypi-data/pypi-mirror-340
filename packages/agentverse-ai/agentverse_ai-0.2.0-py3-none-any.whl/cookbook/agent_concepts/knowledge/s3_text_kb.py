from agentverse_ai.agent import Agent
from agentverse_ai.knowledge.s3.text import S3TextKnowledgeBase
from agentverse_ai.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = S3TextKnowledgeBase(
    bucket_name="agentverse_ai-public",
    key="recipes/recipes.docx",
    vector_db=PgVector(table_name="recipes", db_url=db_url),
)
knowledge_base.load(recreate=True)  # Comment out after first run

agent = Agent(knowledge=knowledge_base, search_knowledge=True)
agent.print_response("How to make Hummus?", markdown=True)
