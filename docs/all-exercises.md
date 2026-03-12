# All Exercises

A quick-reference index of every hands-on exercise in the workshop. Click any exercise to jump to its page with full details.

!!! tip "Running exercises"
    You can run exercises individually from the terminal, or use the interactive [Workshop TUI](workshop-tui.md) to browse and run them all from one place.

## 0 — Setup

| Exercise | Description |
|----------|-------------|
| [Connection Test](exercises/00_setup.md) | Verify your OpenAI / Azure OpenAI connection is working |

## 1 — LLM Foundations

| Exercise | Description |
|----------|-------------|
| [Chat Completion](exercises/01_chat_completion.md) | Single-turn and multi-turn conversations with a travel assistant |
| [System Prompts](exercises/01_system_prompts.md) | Same query, different personas — see how system prompts shape behavior |
| [Structured Outputs](exercises/01_structured_outputs.md) | Extract structured JSON from product reviews using Pydantic models |

**Concepts:** [Chat Completions API](concepts/chat-completions-api.md) · [System Prompts](concepts/system-prompts.md) · [Structured Outputs](concepts/structured-outputs.md) · [What Is an Agent?](concepts/what-is-an-agent.md)

## 2 — Tools & Function Calling

| Exercise | Description |
|----------|-------------|
| [Function Calling](exercises/02_function_calling.md) | Define tools with `pydantic_function_tool()` and make a single-pass tool call |
| [Tool Loop](exercises/02_tool_loop.md) | Build the full agent loop: reason → call tool → observe → repeat |

**Concepts:** [Function Calling](concepts/function-calling.md) · [The Agent Run Loop](concepts/agent-run-loop.md)

## 3 — Single Agent

| Exercise | Description |
|----------|-------------|
| [Customer Support Agent](exercises/03_single_agent.md) | Multi-turn agent with order lookup, FAQ search, and refund processing |

**Pattern:** [Single Agent](patterns/single-agent.md)

## 4 — Sequential Pattern

| Exercise | Description |
|----------|-------------|
| [Content Pipeline](exercises/04_sequential.md) | Research → draft → edit pipeline with explicit context passing between stages |

**Pattern:** [Sequential](patterns/sequential.md)

## 5 — Concurrent Pattern

| Exercise | Description |
|----------|-------------|
| [Stock Analysis](exercises/05_concurrent.md) | Fan-out/fan-in with 3 parallel analysts and an aggregator |

**Pattern:** [Concurrent](patterns/concurrent.md)

## 6 — Group Chat Pattern

| Exercise | Description |
|----------|-------------|
| [Brainstorm](exercises/06_brainstorm.md) | PM, Designer, and Engineer debate a product idea in rounds |
| [Maker-Checker](exercises/06_maker_checker.md) | Code generator + reviewer in a reflection loop |

**Patterns:** [Brainstorm (Round-Robin)](patterns/brainstorm.md) · [Maker-Checker (Reflection)](patterns/maker-checker.md)

## 7 — Handoff Pattern

| Exercise | Description |
|----------|-------------|
| [Support Triage](exercises/07_handoff.md) | Triage agent classifies queries and routes to billing, technical, or account specialists |

**Pattern:** [Handoff](patterns/handoff.md)

## 8 — Magentic Pattern

| Exercise | Description |
|----------|-------------|
| [Incident Response](exercises/08_magentic.md) | Manager coordinates diagnostic, infrastructure, and communication workers |

**Pattern:** [Magentic](patterns/magentic.md)
