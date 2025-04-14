from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.together import Together

agent = Agent(
    model=Together(id="meta-llama/Llama-Vision-Free"),
    markdown=True,
)

image_path = Path(__file__).parent.joinpath("sample.jpg")

# Read the image file content as bytes
image_bytes = image_path.read_bytes()

agent.print_response(
    "Tell me about this image",
    images=[
        Image(content=image_bytes),
    ],
    stream=True,
)
