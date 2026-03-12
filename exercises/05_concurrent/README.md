# Exercise 05: Concurrent Pattern

## Objective

Implement fan-out/fan-in execution where multiple agents work in parallel, then results are aggregated.

## Concepts Covered

- Parallel agent execution with `concurrent.futures`
- Independent context per agent (no shared state between parallel agents)
- Result aggregation by a synthesizer agent
- Fan-out/fan-in architecture

## How It Works

Four agents participate, but only three run concurrently. The Fundamental, Technical, and Sentiment analysts each analyze the same stock independently. Their results are then combined and given to an Aggregator agent that produces a final investment report.

```mermaid
flowchart TB
    Topic["User Query:<br/>'Analyze AAPL stock'"]

    subgraph Parallel["ThreadPoolExecutor (max_workers=3)"]
        direction LR
        subgraph FA["Fundamental<br/>Analyst"]
            FA_CTX["Own messages list<br/>Own system prompt<br/>Tools: get_financial_data"]
        end
        subgraph TA["Technical<br/>Analyst"]
            TA_CTX["Own messages list<br/>Own system prompt<br/>Tools: get_stock_price,<br/>get_price_history"]
        end
        subgraph SA["Sentiment<br/>Analyst"]
            SA_CTX["Own messages list<br/>Own system prompt<br/>Tools: search_news,<br/>get_social_sentiment"]
        end
    end

    subgraph Agg["Aggregator Agent"]
        AGG_CTX["Fresh messages list<br/>Input: all 3 outputs<br/>combined with headers"]
        AGG_OUT["Final investment<br/>report"]
        AGG_CTX --> AGG_OUT
    end

    Topic --> FA
    Topic --> TA
    Topic --> SA
    FA --> |"output text"| Agg
    TA --> |"output text"| Agg
    SA --> |"output text"| Agg

    style Parallel fill:#f5eef8,stroke:#8e44ad
    style Agg fill:#eafaf1,stroke:#2ecc71
```

The execution timeline:

```mermaid
sequenceDiagram
    participant Script as Orchestrator
    participant Pool as ThreadPoolExecutor
    participant F as Fundamental
    participant T as Technical
    participant S as Sentiment
    participant A as Aggregator
    participant LLM as LLM Provider

    Script->>Pool: Submit 3 agents in parallel
    par Fundamental analysis
        Pool->>F: Fresh messages + tools
        F->>LLM: get_financial_data calls
        LLM-->>F: financial analysis
    and Technical analysis
        Pool->>T: Fresh messages + tools
        T->>LLM: get_stock_price, get_price_history calls
        LLM-->>T: technical analysis
    and Sentiment analysis
        Pool->>S: Fresh messages + tools
        S->>LLM: search_news, get_social_sentiment calls
        LLM-->>S: sentiment analysis
    end
    F-->>Script: fundamental_output
    T-->>Script: technical_output
    S-->>Script: sentiment_output

    Note over Script: Combine with === headers ===

    Script->>A: Fresh messages: [system, user(combined)]
    A->>LLM: Produce final report
    LLM-->>A: investment report
    A-->>Script: final_report
```

**Context sharing:** **Completely isolated.** Each analyst gets its own `messages` list, its own system prompt, and its own tools. No agent can see another agent's reasoning or tool calls. The Aggregator receives only the final text outputs, formatted with `=== Analyst Name ===` headers. Thread safety is guaranteed because there is zero shared mutable state between the concurrent agents.

**Structured output:** Not used. Plain text strings are passed between agents.

!!! tip "When to use this pattern"
    The concurrent pattern works best when sub-tasks are **independent** — no agent needs another agent's output to do its work. If agents have dependencies, use the sequential pattern instead. You can also combine both: parallel fan-out followed by sequential refinement.

## Files

1. **`01_stock_analysis.py`** — Three parallel analyst agents + an aggregator for stock analysis

## How to Run

```bash
python exercises/05_concurrent/01_stock_analysis.py
```

## Expected Output

Logging showing parallel agent launches, individual completions, and the final aggregated analysis.

## Next

→ [Exercise 06: Group Chat Pattern](06_group_chat.md)
