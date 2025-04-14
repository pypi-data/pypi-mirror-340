from agentverse_ai.agent import Agent
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.playground import Playground, serve_playground_app
from agentverse_ai.storage.sqlite import SqliteStorage

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
audio_and_text_agent = Agent(
    agent_id="audio-text-agent",
    name="Audio and Text Chat Agent",
    model=OpenAIChat(
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "pcm16"},  # Wav not supported for streaming
    ),
    debug_mode=True,
    add_history_to_messages=True,
    add_datetime_to_instructions=True,
    storage=SqliteStorage(table_name="audio_agent", db_file="tmp/audio_agent.db"),
)

app = Playground(agents=[audio_and_text_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("audio_conversation_agent:app", reload=True)
