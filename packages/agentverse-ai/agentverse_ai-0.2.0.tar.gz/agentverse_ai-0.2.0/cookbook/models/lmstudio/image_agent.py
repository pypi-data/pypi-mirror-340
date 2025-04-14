import httpx
from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.lmstudio import LMStudio

agent = Agent(
    model=LMStudio(id="llama3.2-vision"),
    markdown=True,
)

response = httpx.get(
    "https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg"
)

agent.print_response(
    "Tell me about this image",
    images=[Image(content=response.content)],
    stream=True,
)
