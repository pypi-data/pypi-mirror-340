"""Run `pip install duckduckgo-search sqlalchemy pgvector pypdf openai` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.embedder.azure_openai import AzureOpenAIEmbedder
from agentverse_ai.knowledge.pdf_url import PDFUrlKnowledgeBase
from agentverse_ai.models.azure import AzureOpenAI
from agentverse_ai.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://agentverse_ai-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector(
        table_name="recipes",
        db_url=db_url,
        embedder=AzureOpenAIEmbedder(),
    ),
)
knowledge_base.load(recreate=False)  # Comment out after first run

agent = Agent(
    model=AzureOpenAI(id="gpt-4o-mini"),
    knowledge=knowledge_base,
    show_tool_calls=True,
    debug_mode=True,
)
agent.print_response("How to make Thai curry?", markdown=True)
