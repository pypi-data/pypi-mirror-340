from agentverse_ai.agent import Agent
from agentverse_ai.tools.shell import ShellTools

agent = Agent(tools=[ShellTools()], show_tool_calls=True)
agent.print_response("Show me the contents of the current directory", markdown=True)
