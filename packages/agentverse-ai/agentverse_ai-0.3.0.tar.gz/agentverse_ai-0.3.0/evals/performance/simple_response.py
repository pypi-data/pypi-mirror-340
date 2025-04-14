"""Run `pip install openai agno memory_profiler` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.eval.perf import PerfEval

def simple_response():
    agent = Agent(model=OpenAIChat(id='gpt-4o-mini'), system_message='Be concise, reply with one sentence.')
    response = agent.run('What is the capital of France?')
    print(response.content)
    return response

simple_response_perf = PerfEval(func=simple_response, num_iterations=10)

if __name__ == "__main__":
    simple_response_perf.run(print_results=True)
