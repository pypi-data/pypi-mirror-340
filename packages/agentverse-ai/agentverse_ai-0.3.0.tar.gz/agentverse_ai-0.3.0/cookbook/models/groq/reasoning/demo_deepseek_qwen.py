"""Run `pip install duckduckgo-search sqlalchemy pgvector pypdf openai groq` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.knowledge.pdf_url import PDFUrlKnowledgeBase
from agentverse_ai.models.groq import Groq
from agentverse_ai.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

agent_with_reasoning = Agent(
    model=Groq(id="Qwen-2.5-32b"),
    reasoning=True,
    reasoning_model=Groq(
        id="Deepseek-r1-distill-qwen-32b", temperature=0.6, max_tokens=1024, top_p=0.95
    ),
    show_tool_calls=True,
    debug_mode=True,
)
agent_with_reasoning.print_response("9.11 and 9.9 -- which is bigger?", markdown=True)
