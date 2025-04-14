"""
Async example using Claude with tool calls.
"""

import asyncio
from pprint import pprint

from agentverse_ai.agent import Agent
from agentverse_ai.models.azure import AzureAIFoundry
from agentverse_ai.run.response import RunResponse
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=AzureAIFoundry(id="Cohere-command-r-08-2024"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)

response: RunResponse = asyncio.run(agent.arun("Whats happening in France?"))

print(response.content)
print()
print(response.metrics)
