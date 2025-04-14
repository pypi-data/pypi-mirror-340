from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.aws import AwsBedrock
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools
from agentverse_ai.utils.media import download_image

agent = Agent(
    model=AwsBedrock(id="amazon.nova-pro-v1:0"),
    tools=[DuckDuckGoTools()],
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
    "Tell me about this image and give me the latest news about it.",
    images=[
        Image(content=image_bytes, format="jpeg"),
    ],
)
