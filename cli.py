"""
cli.py
--------
The "Agents CLI" referenced in the Kaggle requirements mapping
("Agent Skills -> Agents CLI"). Each specialist agent is exposed as
its own subcommand, so you can run a single agent in isolation
(useful for debugging/demoing one skill at a time) or run the full
pipeline in one shot.

Usage:
    python cli.py full "I want to build an offline UPI reliability product"
    python cli.py research "your idea here"
    python cli.py competitor "your idea here"
    python cli.py marketing "your idea here"
    python cli.py finance "your idea here"

`research`, `competitor`, `marketing`, and `finance` each run ONLY
that one agent (useful to demo or debug a single skill). `full` runs
the entire sequential pipeline, same as the Streamlit UI, and writes
a Markdown report to disk.
"""

import argparse
import asyncio
import sys
import uuid

from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import InMemoryRunner  # noqa: E402
from google.genai import types  # noqa: E402

from agents.orchestrator import run_pipeline, APP_NAME  # noqa: E402
from agents.research_agent import research_agent  # noqa: E402
from agents.competitor_agent import competitor_agent  # noqa: E402
from agents.marketing_agent import marketing_agent  # noqa: E402
from agents.finance_agent import finance_agent  # noqa: E402
from tools.report_generator import build_report, save_report  # noqa: E402

SINGLE_AGENTS = {
    "research": research_agent,
    "competitor": competitor_agent,
    "marketing": marketing_agent,
    "finance": finance_agent,
}


async def run_single_agent(agent, idea: str, state: dict | None = None) -> str:
    """Runs exactly one agent in isolation (no pipeline) and returns its text."""
    runner = InMemoryRunner(agent=agent, app_name=APP_NAME)
    user_id, session_id = "founder", str(uuid.uuid4())

    initial_state = {"startup_idea": idea}
    if state:
        initial_state.update(state)

    await runner.session_service.create_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id, state=initial_state
    )

    message = types.Content(role="user", parts=[types.Part(text=idea)])
    final_text = ""
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=message
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if getattr(part, "text", None):
                    final_text = part.text
    return final_text


def main():
    parser = argparse.ArgumentParser(
        description="FounderGPT Agents CLI — run the full pipeline or one skill at a time."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    full_p = sub.add_parser("full", help="Run the complete 4-agent pipeline")
    full_p.add_argument("idea", type=str, help="The startup idea")
    full_p.add_argument(
        "--out", type=str, default="foundergpt_blueprint.md", help="Output Markdown file"
    )

    for name in SINGLE_AGENTS:
        p = sub.add_parser(name, help=f"Run only the {name} agent")
        p.add_argument("idea", type=str, help="The startup idea")

    args = parser.parse_args()

    if args.command == "full":
        print(f"Running full pipeline for: {args.idea}\n")
        results = asyncio.run(run_pipeline(args.idea))
        report = build_report(args.idea, results)
        path = save_report(report, args.out)
        print(report)
        print(f"\nSaved full report to {path}")
    else:
        agent = SINGLE_AGENTS[args.command]
        print(f"Running '{args.command}' agent for: {args.idea}\n")
        output = asyncio.run(run_single_agent(agent, args.idea))
        print(output)


if __name__ == "__main__":
    sys.exit(main())
