from textwrap import dedent

from agentverse_ai.agent import Agent
from agentverse_ai.embedder.openai import OpenAIEmbedder
from agentverse_ai.knowledge.url import UrlKnowledge
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.vectordb.lancedb import LanceDb, SearchType

agent_knowledge = UrlKnowledge(
    urls=["https://docs.agentverse_ai.com/llms-full.txt"],
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agentverse_ai_docs",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
)

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description=dedent("""\
    You are AgentVerse-AIAssist, an advanced AI Agent specialized in the AgentVerse-AI framework.
    Your goal is to help developers effectively use AgentVerse-AI by providing explanations and working code examples"""),
    instructions=dedent("""\
    1. Analyze the request
    2. Search your knowledge base for relevant information
    3. Present the information to the user\
    """),
    knowledge=agent_knowledge,
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
)

if __name__ == "__main__":
    load_knowledge = False
    if load_knowledge:
        agent_knowledge.load()

    agent.print_response(
        "What is AgentVerse-AI and how do I implement Agentic RAG?", stream=True
    )
