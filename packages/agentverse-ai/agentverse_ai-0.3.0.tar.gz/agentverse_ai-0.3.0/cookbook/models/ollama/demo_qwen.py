from agentverse_ai.agent import Agent, RunResponse  # noqa
from agentverse_ai.models.ollama import Ollama
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Ollama(id="qwen2.5:latest "), tools=[DuckDuckGoTools()], markdown=True
)

# Print the response in the terminal
agent.print_response("What is happening in France?")
