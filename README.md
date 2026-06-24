# FounderGPT — AI Startup Founder Agent

Turn a raw startup idea into a research-backed startup blueprint:
market research → competitor analysis & SWOT → GTM strategy & landing
page copy → revenue model, MVP roadmap, and an investor pitch.

Built for the Kaggle Agentic AI capstone using **Google ADK + Gemini
2.5**, with live web grounding via ADK's built-in `google_search` tool.

## How it works

Four specialist agents run **in sequence**. Each one writes its
output into shared session state, and every agent after it reads that
state straight into its own prompt — so the competitor agent sees the
market research, the marketing agent sees both, and the finance agent
sees everything before writing the final investor pitch.

```
                 ┌─────────────────┐
  startup idea → │ research_agent  │  (google_search) → market_research
                 └────────┬────────┘
                          ▼
                 ┌─────────────────┐
                 │ competitor_agent│  (google_search) → competitor_analysis
                 └────────┬────────┘
                          ▼
                 ┌─────────────────┐
                 │ marketing_agent │  (synthesis)      → gtm_and_landing_page
                 └────────┬────────┘
                          ▼
                 ┌─────────────────┐
                 │ finance_agent   │  (synthesis)      → finance_and_pitch
                 └────────┬────────┘
                          ▼
                  full Markdown report
```

`agents/orchestrator.py` wires these four into a single ADK
`SequentialAgent` called `root_agent`, and exposes one function,
`run_pipeline(idea)`, that both the Streamlit UI and the CLI call.

## Folder structure

```
foundergpt/
├── agent.py                  # re-exports root_agent for `adk web`/`adk run`
├── agents/
│   ├── orchestrator.py       # wires the 4 agents + run_pipeline()
│   ├── research_agent.py     # market research (uses google_search)
│   ├── competitor_agent.py   # competitors + SWOT (uses google_search)
│   ├── marketing_agent.py    # GTM strategy + landing page copy
│   └── finance_agent.py      # revenue model, MVP roadmap, investor pitch
├── tools/
│   ├── web_search.py         # re-exports ADK's built-in google_search tool
│   └── report_generator.py   # assembles the final Markdown report
├── ui/
│   └── app.py                # Streamlit front-end
├── cli.py                    # "Agents CLI" — run the full pipeline or one skill at a time
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. **Get a Gemini API key** (free): https://aistudio.google.com/app/apikey

2. **Install dependencies:**
   ```bash
   cd foundergpt
   python3 -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Add your API key:**
   ```bash
   cp .env.example .env
   # then edit .env and paste your key into GOOGLE_API_KEY
   ```

## Running it

**Streamlit UI** (the main demo surface):
```bash
streamlit run ui/app.py
```

**CLI** (run the full pipeline, or just one agent/skill at a time):
```bash
python cli.py full "I want to build an offline UPI reliability product"
python cli.py research "I want to build an offline UPI reliability product"
python cli.py competitor "I want to build an offline UPI reliability product"
```
`full` saves a Markdown report (`foundergpt_blueprint.md` by default,
override with `--out`).

**ADK Dev UI / ADK CLI** (useful for debugging agent reasoning and
tool calls step by step):
```bash
adk web .
# or
adk run .
```

## Kaggle requirements mapping

| Requirement | How FounderGPT satisfies it |
|---|---|
| Agent System | 4-agent sequential pipeline (`SequentialAgent` in `orchestrator.py`), each agent reading/writing shared session state |
| MCP Server | (see note below) |
| Antigravity | Demo recorded using Antigravity — see `/demo` notes when you add your video |
| Security | API key loaded from `.env` (never hardcoded), `.env` is gitignored |
| Deployability | `streamlit run ui/app.py` — one command, no infra |
| Agent Skills | `cli.py` exposes each agent as its own subcommand (`research`, `competitor`, `marketing`, `finance`) plus `full` for the whole pipeline |

**Note on MCP:** this build uses ADK's native `google_search` tool
for web grounding rather than a custom MCP server, since it's the
most reliable grounding option without extra infrastructure. If your
rubric specifically requires an MCP *server* (not just MCP-compatible
tooling), the cleanest add is to wrap `tools/web_search.py` as an MCP
tool server using `MCPToolset` (already available in `google.adk.tools`)
— ask me and I'll build that next as a follow-up, since it's a
genuinely separate piece of work from what's here.

## Known limitations / what to mention in your demo

- Agents synthesize from real `google_search` results, but you should
  spot-check a generated report before treating any numbers as fact —
  it's a founder *starting point*, not verified market data.
- The pipeline is sequential by design (so later agents can build on
  earlier output) — this is a deliberate tradeoff for coherence over
  raw speed. If you want `research_agent` and `competitor_agent` to
  run in parallel instead (both only need the original idea, not each
  other's output), that's a `ParallelAgent` swap in `orchestrator.py`.
