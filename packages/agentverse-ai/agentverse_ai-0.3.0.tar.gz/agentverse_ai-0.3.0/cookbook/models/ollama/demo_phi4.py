from agentverse_ai.agent import Agent, RunResponse  # noqa
from agentverse_ai.models.ollama import Ollama
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(model=Ollama(id="phi4"), markdown=True)

# Print the response in the terminal
agent.print_response("Tell me a scary story in exactly 10 words.")
