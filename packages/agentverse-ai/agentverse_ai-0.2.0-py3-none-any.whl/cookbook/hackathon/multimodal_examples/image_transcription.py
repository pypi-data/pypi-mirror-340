"""
This agent transcribes an old written document from an image.
"""

from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.mistral.mistral import MistralChat

agent = Agent(
    model=MistralChat(id="pixtral-12b-2409"),
    markdown=True,
)

agent.print_response(
    "Transcribe this document.",
    images=[
        Image(url="https://ciir.cs.umass.edu/irdemo/hw-demo/page_example.jpg"),
    ],
)
