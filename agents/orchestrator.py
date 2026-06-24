"""
orchestrator.py
------------------
This is the spine of FounderGPT. It does two things:

1. Defines `root_agent` — a SequentialAgent that chains the four
   specialist agents in a fixed order:
       research_agent -> competitor_agent -> marketing_agent -> finance_agent
   Each agent writes its result into shared session state (via
   output_key) and the next agent reads it back out via {key}
   templating in its own instruction. This is the standard ADK
   "Sequential Workflow" pattern: see
   https://google.github.io/adk-docs (Workflow Agents).

2. Exposes `run_pipeline(idea)` — a plain async function the
   Streamlit UI (ui/app.py) and the CLI (cli.py) both call. It hides
   all the Runner/Session boilerplate behind one simple call that
   returns a dict of {section_name: markdown_text}.

`root_agent` is also exported so this folder works directly with the
ADK dev tools, e.g. from the foundergpt/ directory:
    adk web .
    adk run .
"""

import uuid

from google.adk.agents import SequentialAgent
from google.adk.runners import InMemoryRunner
from google.genai import types

from agents.research_agent import research_agent
from agents.competitor_agent import competitor_agent
from agents.marketing_agent import marketing_agent
from agents.finance_agent import finance_agent

APP_NAME = "foundergpt"

# Fixed pipeline order. Each agent reads the state keys written by the
# agents before it (see the {key} placeholders inside each agent's
# instruction) and writes its own output_key for the next agent to use.
root_agent = SequentialAgent(
    name="foundergpt_orchestrator",
    description=(
        "Runs research, competitor analysis, GTM/marketing, and "
        "finance agents in sequence to turn a raw idea into a full "
        "startup blueprint."
    ),
    sub_agents=[
        research_agent,
        competitor_agent,
        marketing_agent,
        finance_agent,
    ],
)

# Maps each agent's output_key -> a human-readable section title.
# Used by report_generator.py and the UI to label sections consistently.
SECTION_TITLES = {
    "market_research": "Market Research",
    "competitor_analysis": "Competitor Analysis & SWOT",
    "gtm_and_landing_page": "Go-To-Market & Landing Page",
    "finance_and_pitch": "Revenue Model, MVP Roadmap & Investor Pitch",
}


async def run_pipeline(idea: str) -> dict[str, str]:
    """
    Runs the full FounderGPT pipeline for one startup idea and returns
    the four section outputs as a plain dict:

        {
          "market_research": "...",
          "competitor_analysis": "...",
          "gtm_and_landing_page": "...",
          "finance_and_pitch": "...",
        }

    This is the one function both the Streamlit UI and the CLI call.
    It hides ADK's session/runner setup so callers don't need to know
    anything about Sessions or Events.
    """
    runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)

    user_id = "founder"
    session_id = str(uuid.uuid4())

    await runner.session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
        state={"startup_idea": idea},
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=idea)],
    )

    # Drain the event stream. We don't need to inspect events directly —
    # each agent's final answer is written into session.state via its
    # output_key, which is the cleanest way to read structured results
    # back out of an ADK pipeline.
    async for _event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message,
    ):
        pass

    session = await runner.session_service.get_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id
    )

    return {key: session.state.get(key, "") for key in SECTION_TITLES}
