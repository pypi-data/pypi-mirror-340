"""Run `pip install openai` to install dependencies."""

from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.tools.dalle import DalleTools
from agentverse_ai.utils.media import download_image

# Create an Agent with the DALL-E tool
agent = Agent(tools=[DalleTools()], name="DALL-E Image Generator")

# Example 1: Generate a basic image with default settings
agent.print_response(
    "Generate an image of a futuristic city with flying cars and tall skyscrapers",
    markdown=True,
)

# Example 2: Generate an image with custom settings
custom_dalle = DalleTools(
    model="dall-e-3", size="1792x1024", quality="hd", style="natural"
)

agent_custom = Agent(
    tools=[custom_dalle],
    name="Custom DALL-E Generator",
    show_tool_calls=True,
)

response = agent_custom.run(
    "Create a panoramic nature scene showing a peaceful mountain lake at sunset",
    markdown=True,
)
if response.images:
    download_image(
        url=response.images[0].url,
        output_path=Path(__file__).parent.joinpath("tmp/nature.jpg"),
    )
