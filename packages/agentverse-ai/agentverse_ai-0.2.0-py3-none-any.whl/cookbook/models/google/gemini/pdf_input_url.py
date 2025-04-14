from agentverse_ai.agent import Agent
from agentverse_ai.media import File
from agentverse_ai.models.google import Gemini

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    markdown=True,
)

agent.print_response(
    "Summarize the contents of the attached file.",
    files=[File(url="https://agentverse_ai-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf")],
)
