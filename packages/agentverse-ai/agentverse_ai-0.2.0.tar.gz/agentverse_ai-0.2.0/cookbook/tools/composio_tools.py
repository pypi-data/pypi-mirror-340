from agentverse_ai.agent import Agent
from composio_agentverse_ai import Action, ComposioToolSet

toolset = ComposioToolSet()
composio_tools = toolset.get_tools(
    actions=[Action.GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER]
)

agent = Agent(tools=composio_tools, show_tool_calls=True)
agent.print_response("Can you star agentverse_ai-agi/agentverse_ai repo?")
