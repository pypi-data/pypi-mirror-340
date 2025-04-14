from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.cohere.chat import Cohere
from agentverse_ai.utils.media import download_image

agent = Agent(
    model=Cohere(id="c4ai-aya-vision-8b"),
    markdown=True,
)

image_path = Path(__file__).parent.joinpath("sample.jpg")

download_image(
    url="https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg",
    output_path=str(image_path),
)

# Read the image file content as bytes
image_bytes = image_path.read_bytes()

agent.print_response(
    "Tell me about this image.",
    images=[
        Image(content=image_bytes),
    ],
    stream=True,
)
