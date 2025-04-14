from agentverse_ai.agent import Agent
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.tools.giphy import GiphyTools

"""Create an agent specialized in creating gifs using Giphy """

gif_agent = Agent(
    name="Gif Generator Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[GiphyTools(limit=5)],
    description="You are an AI agent that can generate gifs using Giphy.",
    instructions=[
        "When the user asks you to create a gif, come up with the appropriate Giphy query and use the `search_gifs` tool to find the appropriate gif.",
    ],
    debug_mode=True,
    show_tool_calls=True,
)

gif_agent.print_response("I want a gif to send to a friend for their birthday.")
