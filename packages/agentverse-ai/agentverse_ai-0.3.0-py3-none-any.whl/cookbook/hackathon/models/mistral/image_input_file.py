from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.mistral.mistral import MistralChat

agent = Agent(
    model=MistralChat(id="pixtral-12b-2409"),
    markdown=True,
)

image_path = Path(__file__).parent.parent.parent.joinpath("data/sample_image.jpg")

agent.print_response(
    "Tell me about this image",
    images=[
        Image(filepath=image_path),
    ],
    stream=True,
)
