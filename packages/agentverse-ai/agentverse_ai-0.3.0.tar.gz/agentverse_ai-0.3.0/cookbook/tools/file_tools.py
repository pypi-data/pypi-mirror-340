from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.tools.file import FileTools

agent = Agent(tools=[FileTools(Path("tmp/file"))], show_tool_calls=True)
agent.print_response(
    "What is the most advanced LLM currently? Save the answer to a file.", markdown=True
)
