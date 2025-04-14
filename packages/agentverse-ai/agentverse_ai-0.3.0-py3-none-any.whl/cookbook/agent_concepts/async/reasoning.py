import asyncio

from agentverse_ai.agent import Agent
from agentverse_ai.cli.console import console
from agentverse_ai.models.openai import OpenAIChat

task = "9.11 and 9.9 -- which is bigger?"

regular_agent = Agent(model=OpenAIChat(id="gpt-4o"), markdown=True)
reasoning_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning=True,
    markdown=True,
)

console.rule("[bold green]Regular Agent[/bold green]")
asyncio.run(regular_agent.aprint_response(task, stream=True))
console.rule("[bold yellow]Reasoning Agent[/bold yellow]")
asyncio.run(
    reasoning_agent.aprint_response(task, stream=True, show_full_reasoning=True)
)
