"""
finance_agent.py
------------------
Fourth and final agent in the pipeline. Runs after research_agent,
competitor_agent, and marketing_agent.

Job: pure synthesis. Pulls together everything the earlier agents
produced into a revenue model, an MVP build roadmap, and a tight
investor pitch summary — the final "startup blueprint" deliverable.

Reads {market_research}, {competitor_analysis}, {gtm_and_landing_page},
writes "finance_and_pitch".
"""

from google.adk.agents import LlmAgent

MODEL = "gemini-3.1-flash-lite"

finance_agent = LlmAgent(
    name="finance_agent",
    model=MODEL,
    description=(
        "Produces a revenue model, MVP roadmap, and investor pitch "
        "summary from the research the team has already gathered."
    ),
    instruction="""
You are a startup operator who has taken products from zero to seed
funding. No web search needed — synthesize everything below into a
final, investor-ready summary.

Startup idea:
{startup_idea}

Market research:
{market_research}

Competitor analysis & SWOT:
{competitor_analysis}

GTM strategy & landing page copy:
{gtm_and_landing_page}

Produce your output in clean Markdown with these exact sections:

## Revenue Model
- Pricing model recommendation (e.g. subscription, usage-based,
  one-time, freemium) with reasoning tied to the target user above
- A rough price point or range
- Primary revenue stream now, and one plausible expansion revenue
  stream later

## MVP Roadmap
A Markdown table with columns: Phase | Timeframe | What gets built |
Goal/metric to hit before moving on. 3 phases: MVP, Early Traction,
Scale prep. Keep timeframes realistic for a solo or 2-person founder
team.

## Investor Pitch Summary
A tight 150-200 word pitch covering: the problem, the solution, why
now, the wedge vs competitors, and the ask (what this founder needs
next — funding, design partners, or co-founder).
""".strip(),
    output_key="finance_and_pitch",
)
