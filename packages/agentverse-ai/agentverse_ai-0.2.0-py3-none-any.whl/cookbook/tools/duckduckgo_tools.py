from agentverse_ai.agent import Agent
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OpenAIChat(id="gpt-4.5-preview"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
)

agent.print_response("Whats the latest about gpt 4.5?", markdown=True)
