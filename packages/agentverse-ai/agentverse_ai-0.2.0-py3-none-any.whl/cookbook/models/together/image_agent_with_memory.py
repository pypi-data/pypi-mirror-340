from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.together import Together

agent = Agent(
    model=Together(id="meta-llama/Llama-Vision-Free"),
    markdown=True,
    add_history_to_messages=True,
    num_history_responses=3,
)

agent.print_response(
    "Tell me about this image",
    images=[
        Image(
            url="https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg"
        )
    ],
    stream=True,
)

agent.print_response("Tell me where I can get more images?")
