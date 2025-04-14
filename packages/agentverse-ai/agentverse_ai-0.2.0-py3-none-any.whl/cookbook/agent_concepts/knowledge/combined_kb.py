from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.knowledge.combined import CombinedKnowledgeBase
from agentverse_ai.knowledge.csv import CSVKnowledgeBase
from agentverse_ai.knowledge.pdf import PDFKnowledgeBase
from agentverse_ai.knowledge.pdf_url import PDFUrlKnowledgeBase
from agentverse_ai.knowledge.website import WebsiteKnowledgeBase
from agentverse_ai.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Create CSV knowledge base
csv_kb = CSVKnowledgeBase(
    path=Path("data/csvs"),
    vector_db=PgVector(
        table_name="csv_documents",
        db_url=db_url,
    ),
)

# Create PDF URL knowledge base
pdf_url_kb = PDFUrlKnowledgeBase(
    urls=["https://agentverse_ai-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector(
        table_name="pdf_documents",
        db_url=db_url,
    ),
)

# Create Website knowledge base
website_kb = WebsiteKnowledgeBase(
    urls=["https://docs.agentverse_ai.com/introduction"],
    max_links=10,
    vector_db=PgVector(
        table_name="website_documents",
        db_url=db_url,
    ),
)

# Create Local PDF knowledge base
local_pdf_kb = PDFKnowledgeBase(
    path="data/pdfs",
    vector_db=PgVector(
        table_name="pdf_documents",
        db_url=db_url,
    ),
)

# Combine knowledge bases
knowledge_base = CombinedKnowledgeBase(
    sources=[
        csv_kb,
        pdf_url_kb,
        website_kb,
        local_pdf_kb,
    ],
    vector_db=PgVector(
        table_name="combined_documents",
        db_url=db_url,
    ),
)

# Initialize the Agent with the combined knowledge base
agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
)

knowledge_base.load(recreate=False)

# Use the agent
agent.print_response("Ask me about something from the knowledge base", markdown=True)
