from agentverse_ai.agent import Agent
from agentverse_ai.tools.zendesk import ZendeskTools

agent = Agent(tools=[ZendeskTools()], show_tool_calls=True)
agent.print_response("How do I login?", markdown=True)
