"""
report_generator.py
----------------------
Pure formatting code — no LLM calls here. Takes the dict that
orchestrator.run_pipeline() returns and turns it into one clean
Markdown document the founder can download, paste into Notion, or
hand to an investor.

Kept as a plain function (not an ADK tool) because no agent needs to
call this mid-reasoning — it's a final assembly step the UI/CLI runs
once the pipeline is done.
"""

from datetime import datetime

from agents.orchestrator import SECTION_TITLES


def build_report(idea: str, results: dict[str, str]) -> str:
    """
    Combines the idea + all four agent outputs into a single Markdown
    report string.

    Args:
        idea: the original startup idea text the founder typed in.
        results: dict returned by orchestrator.run_pipeline(idea),
                 keyed by the same keys as SECTION_TITLES.

    Returns:
        A complete Markdown document as a string.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# FounderGPT Startup Blueprint",
        "",
        f"**Idea:** {idea.strip()}",
        f"**Generated:** {timestamp}",
        "",
        "---",
        "",
    ]

    for key, title in SECTION_TITLES.items():
        section_text = results.get(key, "").strip()
        lines.append(f"## {title}")
        lines.append("")
        lines.append(section_text if section_text else "_(no output generated)_")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def save_report(markdown_text: str, path: str) -> str:
    """Writes the report to disk and returns the path it was saved to."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    return path
