from agentverse_ai.agent import Agent
from agentverse_ai.media import Image
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    markdown=True,
)

if __name__ == "__main__":
    agent.print_response(
        "Tell me about this image and search the web for more information.",
        images=[
            Image(
                url="https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg"
            )
        ],
        stream=True,
    )
