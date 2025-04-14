from agentverse_ai.agent import Agent
from agentverse_ai.tools.jira import JiraTools

agent = Agent(tools=[JiraTools()])
agent.print_response("Find all issues in project PROJ", markdown=True)
