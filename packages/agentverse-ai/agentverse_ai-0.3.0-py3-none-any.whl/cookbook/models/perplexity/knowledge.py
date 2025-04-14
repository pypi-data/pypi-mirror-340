"""Run `pip install duckduckgo-search sqlalchemy pgvector pypdf openai google.generativeai` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.embedder.openai import OpenAIEmbedder
from agentverse_ai.knowledge.pdf_url import PDFUrlKnowledgeBase
from agentverse_ai.models.perplexity import Perplexity
from agentverse_ai.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector(
        table_name="recipes",
        db_url=db_url,
        embedder=OpenAIEmbedder(),
    ),
)
knowledge_base.load(recreate=True)  # Comment out after first run

agent = Agent(
    model=Perplexity(id="sonar-pro"),
    knowledge=knowledge_base,
    show_tool_calls=True,
)
agent.print_response("How to make Thai curry?", markdown=True)
