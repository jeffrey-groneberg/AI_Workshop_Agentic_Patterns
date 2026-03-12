# Exercise 08: Magentic Pattern

## Objective

Implement adaptive planning where a manager agent builds and executes a dynamic task ledger, delegating to specialist workers.

## Concepts Covered

- Task ledger as shared mutable state
- Manager agent that creates, assigns, and tracks tasks
- Worker agents receiving task-specific context only
- Dynamic plan adjustment based on findings
- Synthesis of worker results

## How It Works

This is the most sophisticated pattern in the workshop. A Manager Agent creates a structured plan, delegates tasks to specialist Worker Agents, reviews their findings, and adaptively adjusts the plan — all coordinated through a shared `TaskLedger` data structure and multiple uses of structured output.

```mermaid
flowchart TB
    Incident["Incident Report:<br/>'Database latency spike<br/>in production'"]

    subgraph Phase1["Phase 1: Planning"]
        Manager1["Manager Agent"]
        Plan["chat.completions.parse()<br/>→ IncidentPlan"]
        Ledger["TaskLedger<br/>(shared mutable state)"]
        Manager1 --> Plan --> Ledger
    end

    subgraph Phase2["Phase 2: Worker Execution"]
        direction LR
        subgraph Diag["Diagnostic Agent"]
            D_Task["Task: 'Check DB metrics'"]
            D_Tools["Tools: check_logs,<br/>query_metrics,<br/>check_connections"]
            D_Task --> D_Tools
        end
        subgraph Infra["Infrastructure Agent"]
            I_Task["Task: 'Check server health'"]
            I_Tools["Tools: check_server_health,<br/>scale_service,<br/>restart_service"]
            I_Task --> I_Tools
        end
        subgraph Comms["Communication Agent"]
            C_Task["Task: 'Draft status update'"]
            C_Tools["Tools: send_notification,<br/>update_status_page"]
            C_Task --> C_Tools
        end
    end

    subgraph Phase3["Phase 3: Adapt"]
        Manager2["Manager reviews findings"]
        Adapt["chat.completions.parse()<br/>→ AdaptedPlan"]
        NewTasks["New tasks added<br/>to ledger if needed"]
        Manager2 --> Adapt --> NewTasks
    end

    subgraph Phase4["Phase 4: Report"]
        Report["Final incident report<br/>synthesized from all findings"]
    end

    Incident --> Phase1
    Ledger --> Phase2
    Phase2 --> Phase3
    NewTasks -.-> |"Re-execute if<br/>new tasks added"| Phase2
    Phase3 --> Phase4

    style Phase1 fill:#e8f4fd,stroke:#4a90d9
    style Phase2 fill:#fef9e7,stroke:#f39c12
    style Phase3 fill:#f5eef8,stroke:#8e44ad
    style Phase4 fill:#eafaf1,stroke:#2ecc71
```

The detailed execution flow:

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant M as Manager Agent
    participant LLM as LLM Provider
    participant TL as TaskLedger
    participant D as Diagnostic Agent
    participant I as Infrastructure Agent
    participant C as Communication Agent

    Note over O,C: Phase 1 — Planning (Structured Output)
    O->>M: "Database latency spike in production"
    M->>LLM: chat.completions.parse()<br/>response_format=IncidentPlan
    LLM-->>M: IncidentPlan(tasks=[<br/>  PlannedTask(agent="diagnostic", desc="..."),<br/>  PlannedTask(agent="infrastructure", desc="..."),<br/>  PlannedTask(agent="communication", desc="...")<br/>])
    M->>TL: Create tasks in ledger (status=pending)

    Note over O,C: Phase 2 — Worker Execution
    O->>D: Fresh messages: [sys_prompt, task description only]
    D->>LLM: Execute with diagnostic tools
    LLM-->>D: Findings
    D->>TL: Record result, mark completed

    O->>I: Fresh messages: [sys_prompt, task description only]
    I->>LLM: Execute with infrastructure tools
    LLM-->>I: Actions taken
    I->>TL: Record result, mark completed

    O->>C: Fresh messages: [sys_prompt, task description only]
    C->>LLM: Execute with communication tools
    LLM-->>C: Status update sent
    C->>TL: Record result, mark completed

    Note over O,C: Phase 3 — Adaptive Review (Structured Output)
    O->>M: All findings from ledger
    M->>LLM: chat.completions.parse()<br/>response_format=AdaptedPlan
    LLM-->>M: AdaptedPlan(new_tasks=[...],<br/>assessment="...")
    M->>TL: Add new tasks if any

    alt New tasks added
        Note over O,C: Re-execute Phase 2 for new tasks
    end

    Note over O,C: Phase 4 — Final Report
    O->>M: Synthesize all findings
    M->>LLM: Generate incident report
    LLM-->>M: Comprehensive incident report
```

**Context sharing:** **Task-specific isolation with shared ledger.** The `TaskLedger` dataclass is the single source of truth — it holds all tasks, their status, assigned agents, and results. However, each worker agent receives only its specific task description in a **fresh messages list**, not the full ledger or other workers' findings. Only the Manager sees everything. This gives the Manager full visibility while keeping workers focused.

**Structured output:** **Heavily used — three structured output models:**

- `IncidentPlan` — Manager's initial plan: a list of `PlannedTask` objects with agent assignment and description
- `AdaptedPlan` — Manager's revised plan after reviewing findings: new tasks + assessment
- `PlannedTask` — Individual task definition with agent, description, and status fields

All produced via `client.chat.completions.parse()` with Pydantic models, ensuring reliable plan structure.

!!! warning "Complexity tradeoff"
    The Magentic pattern is the most powerful but also the most complex. It involves multiple LLM calls (planning + N workers + adaptation + reporting), structured outputs for plan management, and mutable shared state. Use it when simpler patterns like sequential or concurrent don't provide enough flexibility — for example, when the plan itself needs to change based on intermediate results.

## Files

1. **`01_incident_response.py`** — Manager handles an incident by coordinating diagnostic, infrastructure, and communication agents

## How to Run

```bash
python exercises/08_magentic/01_incident_response.py
```

## Expected Output

Logging showing the task ledger being built, tasks assigned to workers, worker results flowing back, plan adjustments, and the final incident report.

## Next

→ Return to the [documentation site](../production-considerations/index.md) to review implementation considerations.
