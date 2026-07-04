"""
competitor_agent.py
--------------------
Second agent in the pipeline. Runs after research_agent.

Job: find real competitors/alternatives (via google_search) and produce
a competitor table plus a SWOT analysis for the founder's idea, using
the market research brief from the previous step as context.

Reads session state key "market_research" (via {market_research}
templating) and writes its own output to "competitor_analysis".
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

MODEL = "gemini-3.1-flash-lite"

competitor_agent = LlmAgent(
    name="competitor_agent",
    model=MODEL,
    description=(
        "Identifies real competitors/alternatives and produces a SWOT "
        "analysis for the startup idea."
    ),
    instruction="""
You are a competitive intelligence analyst. Use the google_search tool
to find real, currently-operating competitors or close alternatives
(direct competitors, indirect substitutes, and "do nothing" behavior).
Do not invent companies that don't exist.

Startup idea:
{startup_idea}

Market research already gathered by a teammate:
{market_research}

Produce your analysis in clean Markdown with these exact sections:

## Competitor Landscape
A Markdown table with columns: Competitor | What they do | Strength |
Gap they leave open. Include 3-5 real entries (direct + indirect).

## SWOT Analysis
A Markdown table with columns: Strengths | Weaknesses | Opportunities |
Threats, specific to this idea given the competitive landscape above.

## Differentiation Angle
2-3 sentences on the single sharpest way this idea could position
itself against what already exists.
""".strip(),
    tools=[google_search],
    output_key="competitor_analysis",
)
