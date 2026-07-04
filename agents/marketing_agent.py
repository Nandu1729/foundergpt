"""
marketing_agent.py
--------------------
Third agent in the pipeline. Runs after research_agent and
competitor_agent.

Job: pure synthesis, no external tool calls. Takes the market research
and competitor/SWOT output already sitting in session state and turns
them into a go-to-market angle plus ready-to-paste landing page copy.

Reads {market_research} and {competitor_analysis}, writes
"gtm_and_landing_page".
"""

from google.adk.agents import LlmAgent

MODEL = "gemini-3.1-flash-lite"

marketing_agent = LlmAgent(
    name="marketing_agent",
    model=MODEL,
    description=(
        "Turns market + competitor research into a go-to-market angle "
        "and landing page copy."
    ),
    instruction="""
You are a startup positioning and copywriting specialist. You do not
need to search the web — use the research already produced by your
teammates below as your source of truth.

Startup idea:
{startup_idea}

Market research:
{market_research}

Competitor analysis & SWOT:
{competitor_analysis}

Produce your output in clean Markdown with these exact sections:

## Go-To-Market Strategy
- Primary early-adopter segment (be specific, not "everyone")
- The single channel most likely to reach them first, and why
- One sentence positioning statement ("For [user], [product] is the
  [category] that [benefit], unlike [alternative], we [differentiator]")

## Landing Page Copy
Write copy ready to paste into a page, using this structure:
- **Headline** (under 12 words)
- **Subheadline** (1 sentence, names the pain and the fix)
- **3 feature bullets** (benefit-first, not feature-first)
- **CTA button text** (2-4 words)
- **One-line social proof / credibility placeholder**
""".strip(),
    output_key="gtm_and_landing_page",
)
