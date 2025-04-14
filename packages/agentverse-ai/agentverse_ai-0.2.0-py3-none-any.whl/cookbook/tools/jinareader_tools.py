from agentverse_ai.agent import Agent
from agentverse_ai.tools.jina import JinaReaderTools

agent = Agent(tools=[JinaReaderTools()], debug_mode=True, show_tool_calls=True)
agent.print_response("Summarize: https://github.com/agentverse_ai-agi")
