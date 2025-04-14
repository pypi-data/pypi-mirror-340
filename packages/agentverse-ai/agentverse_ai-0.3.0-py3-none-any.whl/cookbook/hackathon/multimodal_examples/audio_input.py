from agentverse_ai.agent import Agent
from agentverse_ai.media import Audio
from agentverse_ai.models.openai import OpenAIChat

url = "https://openaiassets.blob.core.windows.net/$web/API/docs/audio/alloy.wav"

agent = Agent(
    model=OpenAIChat(id="gpt-4o-audio-preview", modalities=["text"]),
    markdown=True,
)

if __name__ == "__main__":
    agent.print_response(
        "What is in this audio?", audio=[Audio(url=url, format="wav")], stream=True
    )
