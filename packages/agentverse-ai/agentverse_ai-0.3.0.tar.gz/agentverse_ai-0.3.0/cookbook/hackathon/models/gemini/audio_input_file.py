from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Audio
from agentverse_ai.models.google import Gemini

model = Gemini(id="gemini-2.0-flash-exp")
agent = Agent(
    model=model,
    markdown=True,
)

audio_path = Path(__file__).parent.parent.parent.joinpath("data/sample_audio.wav")

agent.print_response(
    "Tell me about this audio",
    audio=[Audio(filepath=audio_path)],
    stream=True,
)
