from agentverse_ai.agent import Agent
from agentverse_ai.tools.serpapi import SerpApiTools

agent = Agent(tools=[SerpApiTools()], show_tool_calls=True)
agent.print_response("Whats happening in the USA?", markdown=True)
