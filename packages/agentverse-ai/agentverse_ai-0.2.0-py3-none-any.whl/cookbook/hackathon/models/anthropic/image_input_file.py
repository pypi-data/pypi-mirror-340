from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.anthropic import Claude
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Claude(id="claude-3-5-sonnet-20241022"),
    tools=[DuckDuckGoTools()],
    markdown=True,
)

image_path = Path(__file__).parent.parent.parent.joinpath("data/sample_image.jpg")

agent.print_response(
    "Tell me about this image and give me the latest news about it.",
    images=[Image(filepath=image_path)],
    stream=True,
)
