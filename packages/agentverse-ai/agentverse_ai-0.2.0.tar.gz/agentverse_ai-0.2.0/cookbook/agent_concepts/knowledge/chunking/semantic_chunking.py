from agentverse_ai.agent import Agent
from agentverse_ai.document.chunking.semantic import SemanticChunking
from agentverse_ai.knowledge.pdf_url import PDFUrlKnowledgeBase
from agentverse_ai.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://agentverse_ai-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector(table_name="recipes_semantic_chunking", db_url=db_url),
    chunking_strategy=SemanticChunking(similarity_threshold=0.5),
)
knowledge_base.load(recreate=False)  # Comment out after first run

agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
)

agent.print_response("How to make Thai curry?", markdown=True)
