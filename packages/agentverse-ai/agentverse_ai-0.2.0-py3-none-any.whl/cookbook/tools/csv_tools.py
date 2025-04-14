from pathlib import Path

import httpx
from agentverse_ai.agent import Agent
from agentverse_ai.tools.csv_toolkit import CsvTools

url = "https://agentverse_ai-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv"
response = httpx.get(url)

imdb_csv = Path(__file__).parent.joinpath("imdb.csv")
imdb_csv.parent.mkdir(parents=True, exist_ok=True)
imdb_csv.write_bytes(response.content)

agent = Agent(
    tools=[CsvTools(csvs=[imdb_csv])],
    markdown=True,
    show_tool_calls=True,
    instructions=[
        "First always get the list of files",
        "Then check the columns in the file",
        "Then run the query to answer the question",
    ],
)
agent.cli_app(stream=False)
