from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.ollama import Ollama

agent = Agent(
    model=Ollama(id="llama3.2-vision"),
    markdown=True,
)

image_path = Path(__file__).parent.parent.parent.joinpath("data/sample_image.jpg")

agent.print_response(
    "Tell me about this image",
    images=[Image(filepath=image_path)],
)
