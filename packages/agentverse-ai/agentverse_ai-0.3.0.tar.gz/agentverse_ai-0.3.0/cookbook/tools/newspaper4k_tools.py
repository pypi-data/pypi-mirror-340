from agentverse_ai.agent import Agent
from agentverse_ai.tools.newspaper4k import Newspaper4kTools

agent = Agent(tools=[Newspaper4kTools()], debug_mode=True, show_tool_calls=True)
agent.print_response(
    "Please summarize https://www.rockymountaineer.com/blog/experience-icefields-parkway-scenic-drive-lifetime"
)
