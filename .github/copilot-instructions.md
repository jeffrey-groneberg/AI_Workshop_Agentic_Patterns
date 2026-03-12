---
applyTo: "**"
---

# Workshop Conventions

This is a multi-day workshop teaching agentic AI design patterns using pure Python and the OpenAI SDK.

## Core Principles

- **No AI frameworks**: No LangChain, LangGraph, CrewAI, Semantic Kernel, Azure AI Agent Service, or Pydantic AI. We teach the underlying patterns from scratch using only `openai`, `pydantic`, and Python stdlib.
- **Only stable APIs**: Use `client.chat.completions.create()` and `client.chat.completions.parse()`. **Never use `client.beta.*`** — no beta namespaces anywhere.
- **Chat Completions API**: This is the primary API for all exercises. The Responses API is documented for reference only.
- **Provider-agnostic**: All exercises work with OpenAI, Azure OpenAI, and GitHub Models via the shared client factory.

## Exercise Structure

- Each exercise is a standalone `.py` file with a `main()` function and `if __name__ == "__main__":` guard.
- Exercises use numbered prefixes: `01_`, `02_`, etc.
- All exercises import from `exercises/commons/` for the LLM client, agent abstraction, and logging utilities.
- Use `logging` (never `print()`) for all output. Logging IS the teaching tool — it makes the agent loop visible.

## API Patterns

- Tool definitions: `openai.pydantic_function_tool(MyModel)` with `strict=True`
- Tool results: role `"tool"` (not `"function"`)
- Tools parameter: `tools=[...]` (not `functions=[...]`)
- Structured outputs: `client.chat.completions.parse(response_format=MyModel)`
- Multi-turn: accumulate messages list with assistant + tool responses

## MKDocs Documentation

- Site lives in `docs/` with Material theme
- Pattern pages follow a template: Overview → Architecture (mermaid) → Context Strategy → Exercise → Expected Output → Key Takeaways → References
- Code examples in docs use `python` fenced code blocks
- Mermaid diagrams for architecture visualization

## Project Layout

```
exercises/
  commons/         # LLM client factory, Agent abstraction, logging utilities
  00_setup/        # Connection test
  01_llm_basics/   # Chat completions, system prompts, structured outputs
  02_tool_use/     # Function calling, tool loop
  03_single_agent/ # Customer support agent
  04_sequential/   # Content pipeline
  05_concurrent/   # Parallel stock analysis
  06_group_chat/   # Brainstorm + maker-checker
  07_handoff/      # Support triage
  08_magentic/     # Incident response (manager pattern)
docs/              # MKDocs Material site
```
