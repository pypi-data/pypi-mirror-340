from typing import Optional

from agentverse_ai.agent import Agent
from agentverse_ai.eval.accuracy import AccuracyEval, AccuracyResult
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.tools.calculator import CalculatorTools


def multiply_and_exponentiate():
    evaluation = AccuracyEval(
        agent=Agent(
            model=OpenAIChat(id="gpt-4o-mini"),
            tools=[CalculatorTools(add=True, multiply=True, exponentiate=True)],
        ),
        question="What is 10*5 then to the power of 2? do it step by step",
        expected_answer="2500",
    )
    result: Optional[AccuracyResult] = evaluation.run(print_results=True)

    assert result is not None and result.avg_score >= 8


def factorial():
    evaluation = AccuracyEval(
        agent=Agent(
            model=OpenAIChat(id="gpt-4o-mini"),
            tools=[CalculatorTools(factorial=True)],
        ),
        question="What is 10!?",
        expected_answer="3628800",
    )
    result: Optional[AccuracyResult] = evaluation.run(print_results=True)

    assert result is not None and result.avg_score >= 8


if __name__ == "__main__":
    multiply_and_exponentiate()
    # factorial()
