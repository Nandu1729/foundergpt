"""
agent.py
----------
This file exists purely so the standard ADK dev tools work out of the
box from inside this folder, e.g.:

    cd foundergpt
    adk web .
    adk run .

ADK's CLI looks for a module exporting `root_agent` at the root of the
folder you point it at. The real pipeline definition lives in
agents/orchestrator.py — this file just re-exports it.
"""

from agents.orchestrator import root_agent

__all__ = ["root_agent"]
