# Exercise 06: Group Chat Pattern

## Objective

Implement multi-agent group conversations with shared context, including the maker-checker (reflection) variant.

## Concepts Covered

- Shared conversation thread across agents
- Chat manager for speaking order and termination
- Maker-checker / evaluator-optimizer loop
- Context window management in multi-agent conversations

## How It Works

This exercise contains two variants of the group chat pattern, each with different communication structures.

### Exercise 1: Brainstorm (Round-Robin)

Three agents — Product Manager, Designer, and Engineer — share a single `shared_messages` list and take turns in a fixed round-robin order. Each agent sees the entire conversation history, prepends its own system prompt, and adds its reply back to the shared list.

```mermaid
flowchart TB
    subgraph SharedThread["Shared Messages List"]
        M1["[user] 'Design a mobile health app'"]
        M2["[assistant] '[PM]: We should focus on...'"]
        M3["[assistant] '[Designer]: The UI should...'"]
        M4["[assistant] '[Engineer]: For the backend...'"]
        M5["[assistant] '[PM]: Building on that...'"]
        M6["...continues for MAX_ROUNDS=3"]
        M1 --> M2 --> M3 --> M4 --> M5 --> M6
    end

    subgraph Cycle["Round-Robin Order (per round)"]
        direction LR
        PM["Product<br/>Manager"] --> Des["Designer"] --> Eng["Engineer"] --> PM
    end

    Cycle -.- SharedThread

    style SharedThread fill:#fef9e7,stroke:#f39c12
    style Cycle fill:#e8f4fd,stroke:#4a90d9
```

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant PM as Product Manager
    participant D as Designer
    participant E as Engineer
    participant LLM as LLM Provider

    Note over O,LLM: Round 1 of 3

    O->>PM: [PM system_prompt] + shared_messages
    PM->>LLM: Full shared context
    LLM-->>PM: "[PM]: We should focus on..."
    PM->>O: Append reply to shared_messages

    O->>D: [Designer system_prompt] + shared_messages
    D->>LLM: Full shared context (includes PM reply)
    LLM-->>D: "[Designer]: The UI should..."
    D->>O: Append reply to shared_messages

    O->>E: [Engineer system_prompt] + shared_messages
    E->>LLM: Full shared context (includes PM + Designer)
    LLM-->>E: "[Engineer]: For the backend..."
    E->>O: Append reply to shared_messages

    Note over O,LLM: Rounds 2-3 repeat same cycle
```

**Context sharing:** **Fully shared.** All agents read and write to the same `shared_messages` list. Each agent sees every previous turn from every other agent. The system prompt is swapped per agent by prepending it to the shared messages before each call.

### Exercise 2: Maker-Checker (Reflection Loop)

Two agents — a Code Generator and a Code Reviewer — alternate on a shared conversation thread. The Generator produces code, the Reviewer critiques it, and the loop continues until the Reviewer responds with `APPROVED` or `MAX_ITERATIONS` (4) is reached.

```mermaid
flowchart TB
    Start["User: 'Write a Python function<br/>to calculate Fibonacci'"]
    Gen["Code Generator<br/>produces code"]
    Rev{"Code Reviewer<br/>evaluates code"}
    Approved["Output: Final<br/>approved code"]
    Reject["Feedback appended<br/>to shared thread"]
    MaxIter{"MAX_ITERATIONS<br/>reached?"}
    Timeout["Output: Last version<br/>(not approved)"]

    Start --> Gen
    Gen --> Rev
    Rev -- "starts with APPROVED" --> Approved
    Rev -- "critique / suggestions" --> Reject
    Reject --> MaxIter
    MaxIter -- "No" --> Gen
    MaxIter -- "Yes" --> Timeout

    style Approved fill:#eafaf1,stroke:#2ecc71
    style Timeout fill:#fdedec,stroke:#e74c3c
    style Rev fill:#fef9e7,stroke:#f39c12
```

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant G as Generator
    participant R as Reviewer
    participant LLM as LLM Provider

    Note over O,LLM: Iteration 1

    O->>G: [Generator sys_prompt] + shared_messages
    G->>LLM: Generate code
    LLM-->>G: "```python\ndef fibonacci(n):..."
    G->>O: Append code to shared_messages

    O->>R: [Reviewer sys_prompt] + shared_messages
    R->>LLM: Review the code
    LLM-->>R: "Issues found: no input validation..."
    R->>O: Append review to shared_messages

    Note over O,LLM: Iteration 2

    O->>G: [Generator sys_prompt] + shared_messages
    G->>LLM: Revise based on feedback
    LLM-->>G: "```python\ndef fibonacci(n):..." (improved)
    G->>O: Append revised code

    O->>R: [Reviewer sys_prompt] + shared_messages
    R->>LLM: Review revised code
    LLM-->>R: "APPROVED - code meets all criteria"
    R->>O: Loop terminates
```

**Context sharing:** **Fully shared.** Both agents operate on the same thread. The Reviewer sees the Generator's code and all prior iterations. The Generator sees the Reviewer's feedback and improves accordingly. This accumulating shared context is what enables iterative refinement.

**Structured output:** Not used in either variant. Agent replies are plain text strings. Termination is detected by checking if the review `strip().upper().startswith("APPROVED")`.

!!! warning "Context window growth"
    In both variants, the shared messages list grows with every turn. With 3 rounds × 3 agents = 9 turns in brainstorm, or up to 8 turns in maker-checker, the context can become substantial. For production systems, consider summarizing or truncating older messages.

## Files (in order)

1. **`01_brainstorm.py`** — Three agents debate a product idea in a shared thread
2. **`02_maker_checker.py`** — Code generator + reviewer in a reflection loop

## How to Run

```bash
python exercises/06_group_chat/01_brainstorm.py
python exercises/06_group_chat/02_maker_checker.py
```

## Expected Output

Turn-by-turn logging showing which agent speaks, the shared conversation growing, and (for maker-checker) the iterative refinement loop.

## Next

→ [Exercise 07: Handoff Pattern](07_handoff.md)
