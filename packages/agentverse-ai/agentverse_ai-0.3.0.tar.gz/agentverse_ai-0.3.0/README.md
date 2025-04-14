<div align="center" id="top">
  <a href="https://docs.agentverseai.app">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://agentverse_ai-public.s3.us-east-1.amazonaws.com/assets/logo-dark.svg">
      <source media="(prefers-color-scheme: light)" srcset="https://agentverse_ai-public.s3.us-east-1.amazonaws.com/assets/logo-light.svg">
      <img src="https://agentverse_ai-public.s3.us-east-1.amazonaws.com/assets/logo-light.svg" alt="AgentVerse-AI">
    </picture>
  </a>
</div>
<div align="center">
  <a href="https://docs.agentverseai.app">📚 Documentation</a> &nbsp;|&nbsp;
  <a href="https://docs.agentverseai.app/examples/introduction">💡 Examples</a> &nbsp;|&nbsp;
</div>

## Overview

**[AgentVerse-AI](https://docs.agentverseai.app) is a lightweight library for building Multimodal Agents with memory, knowledge and tools.**

1. Build lightning-fast Agents that work with text, image, audio and video.
2. Add memory, knowledge and tools as needed.
3. Run anywhere, AgentVerse-AI is open-source.

## AI Engineering is Software Engineering

When building AI products, 80% of your solution will be standard python code, and the remaining 20% will use Agents for automation. AgentVerse-AI is designed for such use cases.

Write your AI logic using familiar programming constructs (if, else, while, for) and avoid complex abstractions like graphs and chains. Here's a simple Agent that can search the web:

```python websearch_agent.py
from agentverse_ai.agent import Agent
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    markdown=True
)
agent.print_response("What's happening in New York?", stream=True)
```

## Key features

AgentVerse-AI is designed to be simple, fast and model agentverse_aistic. Here are some key features:

- **Lightning Fast**: Agent creation is ~10,000x faster than LangGraph (see [performance](#performance)).
- **Model AgentVerse-AIstic**: Use any model, any provider, no lock-in.
- **Multi Modal**: Native support for text, image, audio and video.
- **Multi Agent**: Build teams of specialized agents.
- **Memory Management**: Store agent sessions and state in a database.
- **Knowledge Stores**: Use vector databases for RAG or dynamic few-shot.
- **Structured Outputs**: Make Agents respond with structured data.
- **Monitoring**: Track agent sessions and performance in real-time on [agentverseai.app](https://app.agentverseai.app).

## Installation

```shell
pip install -U agentverse_ai
```

## What are Agents?

**Agents** are AI programs that execute tasks autonomously. They solve problems by running tools, accessing knowledge and memory to improve responses. Unlike traditional programs that follow a predefined execution path, agents dynamically adapt their approach based on context, knowledge and tool results.

Instead of a rigid binary definition, let's think of Agents in terms of agency and autonomy.

- **Level 0**: Agents with no tools (basic inference tasks).
- **Level 1**: Agents with tools for autonomous task execution.
- **Level 2**: Agents with knowledge, combining memory and reasoning.
- **Level 3**: Teams of specialized agents collaborating on complex workflows.

## Example - Basic Agent

```python
from agentverse_ai.agent import Agent
from agentverse_ai.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="You are an enthusiastic news reporter with a flair for storytelling!",
    markdown=True
)
agent.print_response("Tell me about a breaking news story from New York.", stream=True)
```

To run the agent, install dependencies and export your `OPENAI_API_KEY`.

```shell
pip install agentverse_ai openai

export OPENAI_API_KEY=sk-xxxx

python basic_agent.py
```

[View this example in the cookbook](./cookbook/getting_started/01_basic_agent.py)

## Example - Agent with tools

This basic agent will obviously make up a story, lets give it a tool to search the web.

```python
from agentverse_ai.agent import Agent
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="You are an enthusiastic news reporter with a flair for storytelling!",
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True
)
agent.print_response("Tell me about a breaking news story from New York.", stream=True)
```

Install dependencies and run the Agent:

```shell
pip install duckduckgo-search

python agent_with_tools.py
```

Now you should see a much more relevant result.

[View this example in the cookbook](./cookbook/getting_started/02_agent_with_tools.py)

## Example - Agent with knowledge

Agents can store knowledge in a vector database and use it for RAG or dynamic few-shot learning.

**AgentVerse-AI agents use Agentic RAG** by default, which means they will search their knowledge base for the specific information they need to achieve their task.

```python
from agentverse_ai.agent import Agent
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.embedder.openai import OpenAIEmbedder
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools
from agentverse_ai.knowledge.pdf_url import PDFUrlKnowledgeBase
from agentverse_ai.vectordb.lancedb import LanceDb, SearchType

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="You are a Thai cuisine expert!",
    instructions=[
        "Search your knowledge base for Thai recipes.",
        "If the question is better suited for the web, search the web to fill in gaps.",
        "Prefer the information in your knowledge base over the web results."
    ],
    knowledge=PDFUrlKnowledgeBase(
        urls=["https://agentverse_ai-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="recipes",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        ),
    ),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True
)

# Comment out after the knowledge base is loaded
if agent.knowledge is not None:
    agent.knowledge.load()

agent.print_response("How do I make chicken and galangal in coconut milk soup", stream=True)
agent.print_response("What is the history of Thai curry?", stream=True)
```

Install dependencies and run the Agent:

```shell
pip install lancedb tantivy pypdf duckduckgo-search

python agent_with_knowledge.py
```

[View this example in the cookbook](./cookbook/getting_started/03_agent_with_knowledge.py)

## Example - Multi Agent Teams

Agents work best when they have a singular purpose, a narrow scope and a small number of tools. When the number of tools grows beyond what the language model can handle or the tools belong to different categories, use a team of agents to spread the load.

```python
from agentverse_ai.agent import Agent
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.tools.duckduckgo import DuckDuckGoTools
from agentverse_ai.tools.yfinance import YFinanceTools

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    instructions="Always include sources",
    show_tool_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions="Use tables to display data",
    show_tool_calls=True,
    markdown=True,
)

agent_team = Agent(
    team=[web_agent, finance_agent],
    model=OpenAIChat(id="gpt-4o"),
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response("What's the market outlook and financial performance of AI semiconductor companies?", stream=True)
```

Install dependencies and run the Agent team:

```shell
pip install duckduckgo-search yfinance

python agent_team.py
```

[View this example in the cookbook](./cookbook/getting_started/05_agent_team.py)

## Performance

At AgentVerse-AI, we're obsessed with performance. Why? because even simple AI workflows can spawn thousands of Agents to achieve their goals. Scale that to a modest number of users and performance becomes a bottleneck. AgentVerse-AI is designed to power high performance agentic systems:

- Agent instantiation: ~2μs on average (~10,000x faster than LangGraph).
- Memory footprint: ~3.75Kib on average (~50x less memory than LangGraph).

> Tested on an Apple M4 Mackbook Pro.

While an Agent's run-time is bottlenecked by inference, we must do everything possible to minimize execution time, reduce memory usage, and parallelize tool calls. These numbers may seem trivial at first, but our experience shows that they add up even at a reasonably small scale.

### Instantiation time

Let's measure the time it takes for an Agent with 1 tool to start up. We'll run the evaluation 1000 times to get a baseline measurement.

You should run the evaluation yourself on your own machine, please, do not take these results at face value.

```shell
# Setup virtual environment
./scripts/perf_setup.sh
source .venvs/perfenv/bin/activate
# OR Install dependencies manually
# pip install openai agentverse_ai langgraph langchain_openai

# AgentVerse-AI
python evals/performance/instantiation_with_tool.py

# LangGraph
python evals/performance/other/langgraph_instantiation.py
```

> The following evaluation is run on an Apple M4 Mackbook Pro. It also runs as a Github action on this repo.

LangGraph is on the right, **let's start it first and give it a head start**.

AgentVerse-AI is on the left, notice how it finishes before LangGraph gets 1/2 way through the runtime measurement, and hasn't even started the memory measurement. That's how fast AgentVerse-AI is.

https://github.com/user-attachments/assets/ba466d45-75dd-45ac-917b-0a56c5742e23

Dividing the average time of a Langgraph Agent by the average time of an AgentVerse-AI Agent:

```
0.020526s / 0.000002s ~ 10,263
```

In this particular run, **AgentVerse-AI Agents startup is roughly 10,000 times faster than Langgraph Agents**. The numbers continue to favor AgentVerse-AI as the number of tools grow, and we add memory and knowledge stores.

### Memory usage

To measure memory usage, we use the `tracemalloc` library. We first calculate a baseline memory usage by running an empty function, then run the Agent 1000x times and calculate the difference. This gives a (reasonably) isolated measurement of the memory usage of the Agent.

We recommend running the evaluation yourself on your own machine, and digging into the code to see how it works. If we've made a mistake, please let us know.

Dividing the average memory usage of a Langgraph Agent by the average memory usage of an AgentVerse-AI Agent:

```
0.137273/0.002528 ~ 54.3
```

**Langgraph Agents use ~50x more memory than AgentVerse-AI Agents**. In our opinion, memory usage is a much more important metric than instantiation time. As we start running thousands of Agents in production, these numbers directly start affecting the cost of running the Agents.

### Conclusion

AgentVerse-AI agents are designed for performance and while we do share some benchmarks against other frameworks, we should be mindful that accuracy and reliability are more important than speed.

We'll be publishing accuracy and reliability benchmarks running on Github actions in the coming weeks. Given that each framework is different and we won't be able to tune their performance like we do with AgentVerse-AI, for future benchmarks we'll only be comparing against ourselves.

## Cursor Setup

When building AgentVerse-AI agents, using AgentVerse-AI documentation as a source in Cursor is a great way to speed up your development.

1. In Cursor, go to the settings or preferences section.
2. Find the section to manage documentation sources.
3. Add `https://docs.agentverseai.app` to the list of documentation URLs.
4. Save the changes.

Now, Cursor will have access to the AgentVerse-AI documentation.

## Documentation, Community & More examples

- Docs: <a href="https://docs.agentverseai.app" target="_blank" rel="noopener noreferrer">docs.agentverseai.app</a>
- Getting Started Examples: <a href="https://github.com/agentverse_ai-agi/agentverse_ai/tree/main/cookbook/getting_started" target="_blank" rel="noopener noreferrer">Getting Started Cookbook</a>
- Community forum: <a href="https://community.agentverseai.app/" target="_blank" rel="noopener noreferrer">community.agentverseai.app</a>
- Chat: <a href="https://discord.gg/4MtYHHrgA8" target="_blank" rel="noopener noreferrer">discord</a>

## Telemetry

AgentVerse-AI logs which model an agent used so we can prioritize updates to the most popular providers. You can disable this by setting `AGENTVERSE_TELEMETRY=false` in your environment.

<p align="left">
  <a href="#top">⬆️ Back to Top</a>
</p>
