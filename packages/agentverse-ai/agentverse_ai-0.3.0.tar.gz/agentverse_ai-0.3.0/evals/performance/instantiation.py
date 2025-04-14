"""Run `pip install agno openai` to install dependencies."""

from agentverse_ai.agent import Agent
from agentverse_ai.eval.perf import PerfEval

def instantiate_agent():
    return Agent(system_message='Be concise, reply with one sentence.')

instantiation_perf = PerfEval(func=instantiate_agent, num_iterations=1000)

if __name__ == "__main__":
    instantiation_perf.run(print_results=True)
