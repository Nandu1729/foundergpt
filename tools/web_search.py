"""
web_search.py
---------------
FounderGPT doesn't implement its own search API client. Instead it
uses ADK's built-in `google_search` tool, which gives the model live
Google Search grounding directly through the Gemini API — no SerpAPI
key, no scraping, no extra cost beyond your Gemini API usage.

This file exists so the rest of the codebase (and your README) has one
obvious place that says "this is how agents search the web," instead
of importing google.adk.tools directly in five different files.

Only `research_agent` and `competitor_agent` use this tool. The
marketing and finance agents are deliberately tool-free — they
synthesize from state that earlier agents already wrote, so giving
them a search tool too would just slow the pipeline down for no gain.

Note: ADK currently allows at most one built-in tool per agent, and
built-in tools can't be mixed with custom FunctionTools on the same
agent. If you want to add a custom search backend later (e.g. Tavily,
SerpAPI), build it as a FunctionTool here and swap it in for
google_search in the relevant agent file — don't add both to one agent.
"""

from google.adk.tools import google_search

__all__ = ["google_search"]
