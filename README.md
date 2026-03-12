# Agentic AI Design Patterns Workshop

A hands-on, multi-day workshop teaching **agentic AI design patterns** using pure Python and the OpenAI SDK — no AI frameworks required.

## What You'll Learn

This workshop progresses from LLM fundamentals to advanced multi-agent orchestration patterns:

1. **LLM Basics** — Chat completions, system prompts, structured outputs
2. **Tool Use** — Function calling, the agent loop (Reason → Act → Observe)
3. **Single Agent** — A complete agent with multiple tools
4. **Sequential Pattern** — Pipeline of agents processing in stages
5. **Concurrent Pattern** — Fan-out/fan-in with parallel agent execution
6. **Group Chat Pattern** — Shared conversation with multiple agents + maker-checker
7. **Handoff Pattern** — Dynamic routing between specialist agents
8. **Magentic Pattern** — Adaptive planning with a task ledger

## Tech Stack

- **Python 3.11+** (no AI frameworks — just stdlib + OpenAI SDK)
- **OpenAI SDK v2.x** — Chat Completions API with modern patterns
- **Pydantic** — Structured outputs and tool definitions
- **MKDocs Material** — Documentation site

## Supported LLM Providers

All exercises work with any of these providers — just set `LLM_PROVIDER` in your `.env`:

| Provider | Client | Config |
|----------|--------|--------|
| **OpenAI** | `OpenAI()` | `OPENAI_API_KEY` |
| **Azure OpenAI** | `AzureOpenAI()` | `AZURE_OPENAI_ENDPOINT` + `AZURE_OPENAI_API_KEY` |
| **GitHub Models** | `OpenAI(base_url=...)` | `GITHUB_TOKEN` |

## Quick Start

### Option 1: GitHub Codespaces (Recommended)

Click the button below to launch a fully configured environment — no local setup needed:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new?quickstart=1)

Once the codespace is ready, configure your `.env` file and run:

```bash
python exercises/00_setup/01_test_connection.py
```

### Option 2: Local Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd AI_Workshop_Agentic_Patterns

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your provider
cp .env.example .env
# Edit .env with your API keys and provider choice

# 5. Test your connection
python exercises/00_setup/01_test_connection.py

# 6. Start the documentation site
mkdocs serve
# Open http://127.0.0.1:8000
```

## Repository Structure

```
AI_Workshop_Agentic_Patterns/
├── exercises/           # Hands-on Python exercises
│   ├── 00_setup/        # Connection test
│   ├── 01_llm_basics/   # Chat completions, system prompts, structured outputs
│   ├── 02_tool_use/     # Function calling, agent loop
│   ├── 03_single_agent/ # Complete single agent
│   ├── 04_sequential/   # Pipeline pattern
│   ├── 05_concurrent/   # Fan-out/fan-in pattern
│   ├── 06_group_chat/   # Shared conversation + maker-checker
│   ├── 07_handoff/      # Dynamic routing
│   ├── 08_magentic/     # Adaptive planning
│   └── commons/         # Provider abstraction, agent class, utilities
├── docs/                # MKDocs Material site (primary learning material)
│   ├── concepts/        # Foundational concept pages
│   ├── patterns/        # Orchestration pattern deep-dives
│   └── implementation/  # Cross-cutting concerns
├── mkdocs.yml
├── requirements.txt
└── .env.example
```

## Presentation Slides

Chapter-by-chapter slide decks to guide participants through the workshop:

| Chapter | File | Slides | Topics |
|---------|------|--------|--------|
| **1 — LLM Foundations** | [`Chapter1_LLM_Foundations.pptx`](Chapter1_LLM_Foundations.pptx) | 12 | Workshop overview, commons module, Chat API, system prompts, structured outputs |
| **2 — Tools & Function Calling** | [`Chapter2_Tools_Function_Calling.pptx`](Chapter2_Tools_Function_Calling.pptx) | 7 | Tool definitions, 4-step cycle, agent loop, mock tools |
| **3 — Single Agent** | [`Chapter3_Single_Agent.pptx`](Chapter3_Single_Agent.pptx) | 4 | Agent dataclass, run() function, persistent conversation |
| **4 — Multi-Agent Orchestration** | [`Chapter4_Multi_Agent.pptx`](Chapter4_Multi_Agent.pptx) | 10 | Sequential, concurrent, group chat, maker-checker |
| **5 — Advanced Patterns** | [`Chapter5_Advanced_Patterns.pptx`](Chapter5_Advanced_Patterns.pptx) | 10 | Handoff, magentic, choosing patterns, context management, reliability |

Each deck includes both theory slides and exercise code walkthrough slides with key code snippets.

## Learning Path

> **Read the docs first, then code.** The MKDocs site is the primary learning material.
> Exercises reinforce what you learn — they don't replace the documentation.

Start the docs site with `mkdocs serve`, then follow the navigation from Setup → Concepts → Patterns.

## References

- [AI Agent Design Patterns — MS Learn](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)
- [Agentic Patterns — Andrew Ng](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/)
