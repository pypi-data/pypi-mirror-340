import httpx
from agentverse_ai.agent import Agent
from agentverse_ai.media import Audio
from agentverse_ai.models.google import Gemini

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    markdown=True,
)

url = "https://agno-public.s3.amazonaws.com/demo_data/sample_conversation.wav"

response = httpx.get(url)
audio_content = response.content

# Give a sentiment analysis of this audio conversation. Use speaker A, speaker B to identify speakers.

agent.print_response(
    "Give a sentiment analysis of this audio conversation. Use speaker A, speaker B to identify speakers.",
    audio=[Audio(content=audio_content)],
    stream=True,
)
