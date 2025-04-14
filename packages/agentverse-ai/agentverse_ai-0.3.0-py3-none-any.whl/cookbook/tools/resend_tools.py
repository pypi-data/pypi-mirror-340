from agentverse_ai.agent import Agent
from agentverse_ai.tools.resend import ResendTools

from_email = "<enter_from_email>"
to_email = "<enter_to_email>"

agent = Agent(tools=[ResendTools(from_email=from_email)], show_tool_calls=True)
agent.print_response(f"Send an email to {to_email} greeting them with hello world")
