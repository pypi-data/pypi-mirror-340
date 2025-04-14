from agentverse_ai.agent import Agent
from agentverse_ai.tools.yfinance import YFinanceTools

agent = Agent(
    tools=[
        YFinanceTools(
            stock_price=True, analyst_recommendations=True, stock_fundamentals=True
        )
    ],
    show_tool_calls=True,
    description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
    instructions=[
        "Format your response using markdown and use tables to display data where possible."
    ],
)
agent.print_response(
    "Share the NVDA stock price and analyst recommendations", markdown=True
)
