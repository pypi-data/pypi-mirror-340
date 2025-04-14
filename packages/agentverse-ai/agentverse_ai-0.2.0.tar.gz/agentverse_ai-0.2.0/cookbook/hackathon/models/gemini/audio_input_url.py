from agentverse_ai.agent import Agent
from agentverse_ai.media import Audio
from agentverse_ai.models.google import Gemini

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    markdown=True,
)

url = "https://openaiassets.blob.core.windows.net/$web/API/docs/audio/alloy.wav"

agent.print_response(
    "Tell me about this audio",
    audio=[Audio(url=url)],
)
