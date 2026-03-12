# Agentic AI Design Patterns Workshop

> **Disclaimer:** This is **not** an official Microsoft product, does not represent official Microsoft learning materials, product documentation, or official statements by Microsoft Corporation. The content, opinions, and recommendations presented herein are the authors' own, provided solely for educational purposes, and should not be construed as official Microsoft guidance or endorsement.

A hands-on, multi-part workshop teaching **agentic AI design patterns** using pure Python and the OpenAI SDK — no AI frameworks required.

## What You'll Learn

This workshop progresses from LLM fundamentals to advanced multi-agent orchestration patterns:

1. **LLM Basics** — Chat completions, system prompts, structured outputs
2. **Tool Use** — Function calling, the agent loop (Reason → Act → Observe)
3. **Single Agent** — A complete agent with multiple tools
4. **Sequential Pattern** — Pipeline of agents processing in stages
5. **Concurrent Pattern** — Fan-out/fan-in with parallel agent execution
6. **Group Chat Pattern** — Round-robin brainstorm + maker-checker (reflection)
7. **Handoff Pattern** — Dynamic routing between specialist agents
8. **Magentic Pattern** — Adaptive planning with a task ledger

## Tech Stack

- **Python 3.11+** (no AI frameworks — just stdlib + OpenAI SDK)
- **OpenAI SDK v2.x** — Chat Completions API with modern patterns
- **Pydantic** — Structured outputs and tool definitions
- **MKDocs Material** — Documentation site with interactive message flow visualizations

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
git clone https://github.com/jeffreygroneberg/AI_Workshop_Agentic_Patterns.git
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

# 6. Launch the interactive workshop TUI
python workshop.py

# Or start the documentation site
mkdocs serve
# Open http://127.0.0.1:8000
```

## Repository Structure

```
AI_Workshop_Agentic_Patterns/
├── exercises/                # Hands-on Python exercises
│   ├── 00_setup/             # Connection test
│   ├── 01_llm_basics/        # Chat completions, system prompts, structured outputs
│   ├── 02_tool_use/          # Function calling, agent loop
│   ├── 03_single_agent/      # Complete single agent
│   ├── 04_sequential/        # Pipeline pattern
│   ├── 05_concurrent/        # Fan-out/fan-in pattern
│   ├── 06_group_chat/        # Round-robin brainstorm + maker-checker
│   ├── 07_handoff/           # Dynamic routing
│   ├── 08_magentic/          # Adaptive planning
│   └── commons/              # Provider abstraction, agent class, utilities
├── docs/                     # MKDocs Material site (primary learning material)
│   ├── concepts/             # Chat API, system prompts, function calling,
│   │                         #   structured outputs, agent loop, payload walkthrough
│   ├── patterns/             # Single agent, sequential, concurrent, brainstorm,
│   │                         #   maker-checker, handoff, magentic, orchestration overview
│   ├── exercises/            # Per-exercise documentation with interactive widgets
│   └── production-considerations/  # Context management, reliability, choosing patterns
├── mkdocs.yml
├── requirements.txt
└── .env.example
```

## Documentation Site

The MKDocs Material site is the **primary learning material**. It includes:

- **Concept pages** — Foundational theory (Chat API, system prompts, function calling, structured outputs)
- **Pattern pages** — Deep dives into each orchestration pattern with architecture diagrams
- **Exercise pages** — Step-by-step guidance with interactive message flow visualizations and API payload toggles
- **Production considerations** — Context management, reliability, and choosing the right pattern

Start the docs site with `mkdocs serve`, then follow the navigation from Setup → Concepts → Patterns.

## Presentation Slides

Chapter-by-chapter slide decks to guide participants through the workshop:

| Chapter | File | Topics |
|---------|------|--------|
| **1 — LLM Foundations** | [`Chapter1_LLM_Foundations.pdf`](docs/slides/Chapter1_LLM_Foundations.pdf) | Workshop overview, commons module, Chat API, system prompts, structured outputs |
| **2 — Tools & Function Calling** | [`Chapter2_Tools_Function_Calling.pdf`](docs/slides/Chapter2_Tools_Function_Calling.pdf) | Tool definitions, 4-step cycle, agent loop, mock tools |
| **3 — Single Agent** | [`Chapter3_Single_Agent.pdf`](docs/slides/Chapter3_Single_Agent.pdf) | Agent dataclass, run() function, persistent conversation |
| **4 — Multi-Agent Orchestration** | [`Chapter4_Multi_Agent.pdf`](docs/slides/Chapter4_Multi_Agent.pdf) | Sequential, concurrent, group chat, maker-checker |
| **5 — Advanced Patterns** | [`Chapter5_Advanced_Patterns.pdf`](docs/slides/Chapter5_Advanced_Patterns.pdf) | Handoff, magentic, choosing patterns, context management, reliability |

## Learning Path

> **Read the docs first, then code.** The MKDocs site is the primary learning material.
> Exercises reinforce what you learn — they don't replace the documentation.

## Share This Workshop

If you find this workshop useful, share it with your network!

[![Share on LinkedIn](https://img.shields.io/badge/LinkedIn-Share-0A66C2?logo=linkedin)](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fgithub.com%2Fjeffreygroneberg%2FAI_Workshop_Agentic_Patterns)
[![Share on X](https://img.shields.io/badge/X-Share-000?logo=x)](https://x.com/intent/tweet?text=Check%20out%20this%20hands-on%20workshop%20on%20Agentic%20AI%20Design%20Patterns%20%E2%80%94%20pure%20Python%2C%20no%20frameworks!&url=https%3A%2F%2Fgithub.com%2Fjeffreygroneberg%2FAI_Workshop_Agentic_Patterns)
[![Share on Reddit](https://img.shields.io/badge/Reddit-Share-FF4500?logo=reddit)](https://www.reddit.com/submit?url=https%3A%2F%2Fgithub.com%2Fjeffreygroneberg%2FAI_Workshop_Agentic_Patterns&title=Agentic%20AI%20Design%20Patterns%20Workshop)

## References

- [AI Agent Design Patterns — MS Learn](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)
- [Agentic Patterns — Andrew Ng](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/)
