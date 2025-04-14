"""Run `pip install duckduckgo-search sqlalchemy pgvector pypdf openai ollama` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.embedder.ollama import OllamaEmbedder
from agentverse_ai.knowledge.pdf_url import PDFUrlKnowledgeBase
from agentverse_ai.models.lmstudio import LMStudio
from agentverse_ai.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://agentverse_ai-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector(
        table_name="recipes",
        db_url=db_url,
    ),
)
knowledge_base.load(recreate=True)  # Comment out after first run

agent = Agent(
    model=LMStudio(id="qwen2.5-7b-instruct-1m"),
    knowledge=knowledge_base,
    show_tool_calls=True,
)
agent.print_response("How to make Thai curry?", markdown=True)
