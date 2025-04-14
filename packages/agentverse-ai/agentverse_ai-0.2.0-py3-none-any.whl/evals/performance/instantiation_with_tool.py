"""Run `pip install agentverse_ai openai memory_profiler` to install dependencies."""

from typing import Literal

from agentverse_ai.agent import Agent
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.eval.perf import PerfEval

def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")

tools = [get_weather]

def instantiate_agent():
    return Agent(model=OpenAIChat(id='gpt-4o'), tools=tools)

instantiation_perf = PerfEval(func=instantiate_agent, num_iterations=1000)

if __name__ == "__main__":
    instantiation_perf.run(print_results=True)
