import httpx
from agentverse_ai.agent import Agent
from agentverse_ai.media import Audio
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.utils.audio import write_audio_to_file

# Fetch the audio file and convert it to a base64 encoded string
url = "https://openaiassets.blob.core.windows.net/$web/API/docs/audio/alloy.wav"
response = httpx.get(url)
response.raise_for_status()
wav_data = response.content

agent = Agent(
    model=OpenAIChat(
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
    ),
    markdown=True,
)

agent.run(
    "What's in these recording?",
    audio=[Audio(content=wav_data, format="wav")],
)

if agent.run_response.response_audio is not None:
    write_audio_to_file(
        audio=agent.run_response.response_audio.content, filename="tmp/result.wav"
    )
