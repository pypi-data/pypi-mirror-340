from agentverse_ai.agent import Agent
from agentverse_ai.embedder.openai import OpenAIEmbedder
from agentverse_ai.knowledge.url import UrlKnowledge
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.storage.sqlite import SqliteStorage
from agentverse_ai.vectordb.lancedb import LanceDb, SearchType

agentverse_ai_assist = Agent(
    name="AgentVerse-AI Assist",
    model=OpenAIChat(id="gpt-4o"),
    description="You help answer questions about the AgentVerse-AI framework.",
    instructions="Search your knowledge before answering the question.",
    knowledge=UrlKnowledge(
        urls=["https://docs.agentverse_ai.com/llms-full.txt"],
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="agentverse_ai_assist_knowledge",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        ),
    ),
    storage=SqliteStorage(table_name="agentverse_ai_assist_sessions", db_file="tmp/agents.db"),
    add_history_to_messages=True,
    add_datetime_to_instructions=True,
    markdown=True,
)

if __name__ == "__main__":
    agentverse_ai_assist.knowledge.load()  # Load the knowledge base, comment after first run
    agentverse_ai_assist.print_response("What is AgentVerse-AI?")
