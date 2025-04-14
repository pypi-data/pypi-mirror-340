from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.mistral.mistral import MistralChat
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=MistralChat(id="pixtral-12b-2409"),
    tools=[
        DuckDuckGoTools()
    ],  # pixtral-12b-2409 is not so great at tool calls, but it might work.
    show_tool_calls=True,
    markdown=True,
)

image_path = Path(__file__).parent.joinpath("sample.jpeg")

agent.print_response(
    "Tell me about this image and give me the latest news about it from duckduckgo.",
    images=[
        Image(filepath=image_path),
    ],
    stream=True,
)
