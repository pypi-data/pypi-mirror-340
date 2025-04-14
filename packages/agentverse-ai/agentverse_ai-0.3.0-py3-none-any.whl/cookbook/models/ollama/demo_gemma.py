from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.ollama import Ollama

agent = Agent(model=Ollama(id="gemma3:12b"), markdown=True)

image_path = Path(__file__).parent.joinpath("super-agents.png")
agent.print_response(
    "Write a 3 sentence fiction story about the image",
    images=[Image(filepath=image_path)],
    stream=True,
)
