from agentverse_ai.agent import Agent
from agentverse_ai.models.google import Gemini

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp", search=True),
    show_tool_calls=True,
    markdown=True,
)
agent.print_response("Show me top 2 news stories from USA?")
