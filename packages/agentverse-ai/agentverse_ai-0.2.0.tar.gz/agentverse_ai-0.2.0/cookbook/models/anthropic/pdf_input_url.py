from agentverse_ai.agent import Agent
from agentverse_ai.media import File
from agentverse_ai.models.anthropic import Claude

agent = Agent(
    model=Claude(id="claude-3-5-sonnet-20241022"),
    markdown=True,
)

agent.print_response(
    "Summarize the contents of the attached file.",
    files=[
        File(url="https://agentverse_ai-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"),
    ],
    stream=True,
)
