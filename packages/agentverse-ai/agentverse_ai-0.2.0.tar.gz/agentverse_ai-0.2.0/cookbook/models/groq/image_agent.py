from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.groq import Groq

agent = Agent(model=Groq(id="llama-3.2-90b-vision-preview"))

agent.print_response(
    "Tell me about this image",
    images=[
        Image(url="https://upload.wikimedia.org/wikipedia/commons/f/f2/LPU-v1-die.jpg"),
    ],
    stream=True,
)
