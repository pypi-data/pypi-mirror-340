from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.mistral.mistral import MistralChat
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=MistralChat(id="pixtral-12b-2409"),
    markdown=True,
)

agent.print_response(
    "Tell me about this image",
    images=[
        Image(
            url="https://upload.wikimedia.org/wikipedia/commons/b/bf/Krakow_-_Kosciol_Mariacki.jpg"
        ),
    ],
    stream=True,
)
