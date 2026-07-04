"""
research_agent.py
------------------
First agent in the FounderGPT pipeline.

Job: take the raw startup idea and turn it into a structured market
research brief — target users, market size signals, relevant trends,
and risks. Uses ADK's built-in `google_search` tool so the output is
grounded in live web results instead of the model's static training data.

Output is saved into session state under the key "market_research" so
every agent that runs after this one can reference it directly inside
their own instruction prompt via {market_research}.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

MODEL = "gemini-2.5-flash-lite"

research_agent = LlmAgent(
    name="research_agent",
    model=MODEL,
    description=(
        "Researches the market for a startup idea: target users, market "
        "size signals, demand evidence, trends, and key risks."
    ),
    instruction="""
You are a senior market research analyst working inside a startup
advisory pipeline. A founder has given you a raw startup idea. Use the
google_search tool to ground your answer in current, real information
(news, market reports, forums, existing products) — do not rely purely
on memory.

Startup idea:
{startup_idea}

Produce a market research brief in clean Markdown with these exact
sections:

## Target Users
Who has this problem, how painful is it, how do they cope today.

## Market Signals
Concrete evidence the problem/market is real and sizable (cite what you
found via search — name sources, don't fabricate numbers).

## Trends
2-4 trends (technological, regulatory, behavioral) that make this idea
more or less timely right now.

## Key Risks
The 3 biggest reasons this could fail (market, technical, or
regulatory risk).

Be concrete and specific to the idea given. Avoid generic startup
advice that could apply to any product.
""".strip(),
    tools=[google_search],
    output_key="market_research",
)
