from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Audio
from agentverse_ai.models.openai import OpenAIChat

audio_path = Path(__file__).parent.parent.parent.joinpath("data/sample_audio.wav")

agent = Agent(
    model=OpenAIChat(id="gpt-4o-audio-preview", modalities=["text"]),
    markdown=True,
)
agent.print_response(
    "What is in this audio?", audio=[Audio(filepath=audio_path, format="wav")]
)
