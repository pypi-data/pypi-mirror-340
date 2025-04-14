from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import File
from agentverse_ai.models.google import Gemini
from agentverse_ai.utils.media import download_file

pdf_path = Path(__file__).parent.joinpath("ThaiRecipes.pdf")

# Download the file using the download_file function
download_file(
    "https://agentverse_ai-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf", str(pdf_path)
)

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    markdown=True,
    add_history_to_messages=True,
)

agent.print_response(
    "Summarize the contents of the attached file.",
    files=[File(filepath=pdf_path)],
)
agent.print_response("Suggest me a recipe from the attached file.")
