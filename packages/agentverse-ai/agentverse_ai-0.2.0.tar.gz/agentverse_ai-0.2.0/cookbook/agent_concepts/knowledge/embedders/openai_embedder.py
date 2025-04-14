from agentverse_ai.agent import AgentKnowledge
from agentverse_ai.embedder.openai import OpenAIEmbedder
from agentverse_ai.vectordb.pgvector import PgVector

embeddings = OpenAIEmbedder().get_embedding(
    "The quick brown fox jumps over the lazy dog."
)

# Print the embeddings and their dimensions
print(f"Embeddings: {embeddings[:5]}")
print(f"Dimensions: {len(embeddings)}")

# Example usage:
knowledge_base = AgentKnowledge(
    vector_db=PgVector(
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        table_name="openai_embeddings",
        embedder=OpenAIEmbedder(),
    ),
    num_documents=2,
)
