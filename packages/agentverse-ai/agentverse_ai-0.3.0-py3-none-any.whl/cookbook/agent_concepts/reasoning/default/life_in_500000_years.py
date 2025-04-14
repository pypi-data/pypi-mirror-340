from agentverse_ai.agent import Agent
from agentverse_ai.models.openai import OpenAIChat

task = "Write a short story about life in 500000 years"

reasoning_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning=True,
    markdown=True,
)
reasoning_agent.print_response(task, stream=True, show_full_reasoning=True)
