# Exercise 04: Sequential Pattern

## Objective

Implement a multi-agent pipeline where each agent's output feeds into the next — the sequential orchestration pattern.

## Concepts Covered

- Linear agent pipeline (Research → Draft → Edit)
- Fresh context per stage (only passing the previous agent's output)
- Progressive refinement of content
- Context compaction between stages

## How It Works

Three agents process content in a pipeline. The critical design decision: **each agent gets a fresh messages list** containing only the previous agent's final output — not its internal tool calls, reasoning, or full conversation history. This prevents context pollution and keeps each stage focused.

```mermaid
flowchart LR
    subgraph Stage1["Stage 1: Research Agent"]
        R_SYS["System prompt:<br/>'You are a research agent'"]
        R_TOOL["Tools: search_web,<br/>search_academic"]
        R_OUT["Research output<br/>(text summary)"]
        R_SYS --> R_TOOL --> R_OUT
    end

    subgraph Stage2["Stage 2: Draft Writer"]
        D_SYS["System prompt:<br/>'You are a writer'"]
        D_IN["Input: research<br/>output ONLY"]
        D_OUT["Draft article"]
        D_SYS --> D_IN --> D_OUT
    end

    subgraph Stage3["Stage 3: Editor Agent"]
        E_SYS["System prompt:<br/>'You are an editor'"]
        E_IN["Input: draft<br/>article ONLY"]
        E_OUT["Polished article"]
        E_SYS --> E_IN --> E_OUT
    end

    R_OUT -- "Only final text<br/>(no tool history)" --> D_IN
    D_OUT -- "Only draft text<br/>(no prior context)" --> E_IN

    style Stage1 fill:#e8f4fd,stroke:#4a90d9
    style Stage2 fill:#fef9e7,stroke:#f39c12
    style Stage3 fill:#eafaf1,stroke:#2ecc71
```

Each stage in detail:

```mermaid
sequenceDiagram
    participant Script as Orchestrator
    participant R as Research Agent
    participant D as Draft Writer
    participant E as Editor Agent
    participant LLM as LLM Provider

    Note over Script,LLM: Stage 1 — Research (has tools)
    Script->>R: Fresh messages: [system, user(topic)]
    R->>LLM: messages + tools=[search_web, search_academic]
    LLM-->>R: tool_calls → execute → loop until done
    R-->>Script: research_output (text only)

    Note over Script,LLM: Stage 2 — Draft (no tools)
    Script->>D: Fresh messages: [system, user(research_output)]
    D->>LLM: messages (no tools)
    LLM-->>D: draft article
    D-->>Script: draft_output (text only)

    Note over Script,LLM: Stage 3 — Edit (no tools)
    Script->>E: Fresh messages: [system, user(draft_output)]
    E->>LLM: messages (no tools)
    LLM-->>E: polished article
    E-->>Script: final_article
```

**Context sharing:** **Fresh context per stage.** Each agent gets a new `messages` list containing only `[system_prompt, user_message_with_previous_output]`. The Research Agent's tool calls, intermediate reasoning, and raw search results are never seen by the Draft Writer. Only the final text output crosses the boundary. The code uses `log_context_pass()` to make these handoff points visible in the logs.

**Structured output:** Not used. Plain text strings are passed between stages.

!!! info "Why fresh context?"
    Passing full history would waste tokens and risk confusing downstream agents with irrelevant details (like raw search API responses). Fresh context keeps each stage focused on its specific task while still receiving the essential information it needs.

## Files

1. **`01_content_pipeline.py`** — Three-agent content pipeline that produces a polished article

## How to Run

```bash
python exercises/04_sequential/01_content_pipeline.py
```

## Expected Output

Structured logging showing each pipeline stage, what context is passed between agents, and the progressive refinement of the article.

## Next

→ [Exercise 05: Concurrent Pattern](05_concurrent.md)
