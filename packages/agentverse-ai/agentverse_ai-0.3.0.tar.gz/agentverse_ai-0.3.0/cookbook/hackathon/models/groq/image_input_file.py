from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.groq import Groq

agent = Agent(model=Groq(id="llama-3.2-90b-vision-preview"))

image_path = Path(__file__).parent.parent.parent.joinpath("data/sample_image.jpg")

agent.print_response(
    "Tell me about this image",
    images=[Image(filepath=image_path)],
    stream=True,
)
