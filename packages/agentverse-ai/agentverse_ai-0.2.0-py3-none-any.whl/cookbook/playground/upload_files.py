from agentverse_ai.agent import Agent
from agentverse_ai.knowledge.combined import CombinedKnowledgeBase
from agentverse_ai.knowledge.csv import CSVKnowledgeBase
from agentverse_ai.knowledge.docx import DocxKnowledgeBase
from agentverse_ai.knowledge.json import JSONKnowledgeBase
from agentverse_ai.knowledge.pdf import PDFKnowledgeBase
from agentverse_ai.knowledge.text import TextKnowledgeBase
from agentverse_ai.models.google.gemini import Gemini
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.playground.playground import Playground
from agentverse_ai.playground.serve import serve_playground_app
from agentverse_ai.storage.postgres import PostgresStorage
from agentverse_ai.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = CombinedKnowledgeBase(
    sources=[
        PDFKnowledgeBase(
            vector_db=PgVector(table_name="recipes_pdf", db_url=db_url), path=""
        ),
        CSVKnowledgeBase(
            vector_db=PgVector(table_name="recipes_csv", db_url=db_url), path=""
        ),
        DocxKnowledgeBase(
            vector_db=PgVector(table_name="recipes_docx", db_url=db_url), path=""
        ),
        JSONKnowledgeBase(
            vector_db=PgVector(table_name="recipes_json", db_url=db_url), path=""
        ),
        TextKnowledgeBase(
            vector_db=PgVector(table_name="recipes_text", db_url=db_url), path=""
        ),
    ],
    vector_db=PgVector(table_name="recipes_combined", db_url=db_url),
)

file_agent = Agent(
    name="File Upload Agent",
    agent_id="file-upload-agent",
    role="Answer questions about the uploaded files",
    model=OpenAIChat(id="gpt-4o-mini"),
    storage=PostgresStorage(table_name="agent_sessions", db_url=db_url),
    knowledge=knowledge_base,
    show_tool_calls=True,
    markdown=True,
)


audio_agent = Agent(
    name="Audio Understanding Agent",
    agent_id="audio-understanding-agent",
    role="Answer questions about audio files",
    model=OpenAIChat(id="gpt-4o-audio-preview"),
    storage=PostgresStorage(table_name="agent_sessions", db_url=db_url),
    add_history_to_messages=True,
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
)

video_agent = Agent(
    name="Video Understanding Agent",
    model=Gemini(id="gemini-2.0-flash"),
    agent_id="video-understanding-agent",
    role="Answer questions about video files",
    storage=PostgresStorage(table_name="agent_sessions", db_url=db_url),
    add_history_to_messages=True,
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
)

app = Playground(agents=[file_agent, audio_agent, video_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("upload_files:app", reload=True)
