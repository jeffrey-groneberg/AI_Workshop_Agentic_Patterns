# Magentic Pattern

The magentic pattern (adaptive planning) uses a manager agent that maintains a **task ledger** and dynamically coordinates specialist workers. The plan adapts based on findings.

## Pattern Architecture

```mermaid
graph TD
    I[Incident] --> MGR[Manager Agent]
    MGR --> TL[Task Ledger<br/>Shared Mutable State]
    TL --> W1[Diagnostic Worker]
    TL --> W2[Infrastructure Worker]
    TL --> W3[Communication Worker]
    W1 --> TL
    W2 --> TL
    W3 --> TL
    TL --> MGR
    MGR --> R[Final Report]

    style MGR fill:#607D8B,color:white
    style TL fill:#FFC107,color:black
    style W1 fill:#2196F3,color:white
    style W2 fill:#FF9800,color:white
    style W3 fill:#4CAF50,color:white
```

![MS Learn Magentic Pattern](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/_images/magentic-one-pattern.svg)

*Source: [MS Learn — AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)*

## When to Use

- The task is **complex and multi-step** with potential for plan changes
- Intermediate findings may require **adding or modifying tasks**
- A central coordinator needs to **track progress and synthesize results**
- Examples: incident response, project management, complex research

## When to Avoid

- The plan is **fixed and known upfront** (use [Sequential](sequential.md))
- Agents can work **completely independently** (use [Concurrent](concurrent.md))
- Simple classification-based routing suffices (use [Handoff](handoff.md))

## The Task Ledger

The task ledger is the central artifact of this pattern — a **shared mutable dataclass** that the manager uses to coordinate work:

```python
@dataclass
class TaskLedger:
    incident_description: str
    tasks: list[Task]       # All tasks (pending, in-progress, completed)
    findings: list[str]     # Accumulated findings from workers
    next_task_id: int = 1

    def add_task(self, description, assigned_to): ...
    def complete_task(self, task_id, result): ...
    def add_finding(self, finding): ...
```

The ledger is:

- **Maintained by the manager** — workers don't modify it directly
- **Mutable** — new tasks can be added based on findings
- **The single source of truth** for coordination state

## Context Passing Strategy

Workers get **task-specific context only** — not the full ledger, not other workers' outputs. The manager decides what each worker needs to know.

```mermaid
sequenceDiagram
    participant MGR as Manager
    participant TL as Task Ledger
    participant D as Diagnostic Worker
    participant I as Infrastructure Worker
    participant C as Communication Worker

    MGR->>TL: Create initial plan (3-5 tasks)
    MGR->>D: Task: "Check database connection pools"
    Note over MGR,D: Worker gets ONLY<br/>incident context +<br/>its specific task
    D-->>MGR: "Connection pool exhausted at 14:32"
    MGR->>TL: Complete task, add finding
    MGR->>I: Task: "Check deployment v2.3.1 changes"
    I-->>MGR: "New query added without index"
    MGR->>TL: Complete task, add finding

    MGR->>MGR: Review findings, adapt plan
    Note over MGR: Manager decides to<br/>add new task based<br/>on findings
    MGR->>TL: Add task: "Draft customer notice"
    MGR->>C: Task: "Draft status page update"
    C-->>MGR: Draft communication
    MGR->>TL: All tasks complete
    MGR-->>MGR: Write final incident report
```

**Why task-specific context?**

- Workers stay **focused** on their specific task
- Prevents **information overload** — diagnostic details would confuse the communication agent
- The **manager controls information flow** — deciding what each worker needs to know
- Enables the manager to **synthesize** across all workers' findings

**Trade-off**: The manager is a bottleneck — all information flows through it. For very complex tasks, consider hierarchical managers.

## Phases of Execution

```mermaid
graph LR
    P1[Phase 1<br/>Plan] --> P2[Phase 2<br/>Execute]
    P2 --> P3[Phase 3<br/>Adapt]
    P3 -->|New tasks needed| P3b[Phase 3b<br/>Execute additions]
    P3 -->|Ready| P4[Phase 4<br/>Report]
    P3b --> P4

    style P1 fill:#2196F3,color:white
    style P2 fill:#FF9800,color:white
    style P3 fill:#9C27B0,color:white
    style P3b fill:#9C27B0,color:white
    style P4 fill:#4CAF50,color:white
```

1. **Plan**: Manager analyzes the incident and creates initial tasks using structured outputs
2. **Execute**: Workers complete their assigned tasks, findings flow back to the ledger
3. **Adapt**: Manager reviews all findings and decides if more tasks are needed
4. **Report**: Manager synthesizes all findings into a final report

## What We're Building

```mermaid
graph TD
    INC[Incident: Checkout 500 errors<br/>30% of payments failing<br/>Started after v2.3.1 deploy] --> MGR[Manager Agent]

    MGR -->|Plan| TL[Task Ledger]

    TL -->|Task 1| D[Diagnostic Worker<br/>Check error logs,<br/>DB connection pools]
    TL -->|Task 2| I[Infrastructure Worker<br/>Check deployment,<br/>system health]
    TL -->|Task 3| C[Communication Worker<br/>Draft status update]

    D -->|Findings| MGR
    I -->|Findings| MGR
    C -->|Draft| MGR

    MGR -->|Adapt?| TL
    MGR --> R[Final Incident Report]

    style MGR fill:#607D8B,color:white
    style TL fill:#FFC107,color:black
    style D fill:#2196F3,color:white
    style I fill:#FF9800,color:white
    style C fill:#4CAF50,color:white
```

## Expected Console Output

```
══════════════════════════════════════════════════════════════════
  Magentic Pattern: Incident Response
══════════════════════════════════════════════════════════════════
[INFO] Incident: The checkout service is returning 500 errors...

══════════════════════════════════════════════════════════════════
  Phase 1: Initial Planning
══════════════════════════════════════════════════════════════════
[INFO] [Manager] Assessment: Critical incident affecting payment processing...
[INFO] [Task Ledger] Added task #1: 'Investigate database connection pool metrics'
[INFO] [Task Ledger] Added task #2: 'Review v2.3.1 deployment changes'
[INFO] [Task Ledger] Added task #3: 'Draft initial customer communication'

══════════════════════════════════════════════════════════════════
  Phase 2: Executing Tasks
══════════════════════════════════════════════════════════════════
[INFO] Context: task-specific context only (not full ledger)
[INFO] [Diagnostic Worker] Connection pool exhausted at 14:32...
[INFO] [Infrastructure Worker] Deployment v2.3.1 added new query...
[INFO] [Communication Worker] Status update draft: ...

══════════════════════════════════════════════════════════════════
  Phase 3: Plan Adaptation
══════════════════════════════════════════════════════════════════
[INFO] [Manager] Analysis: Root cause identified — missing index...
[INFO] [Task Ledger] Added task #4: 'Verify index fix resolves issue'

══════════════════════════════════════════════════════════════════
  Phase 4: Final Incident Report
══════════════════════════════════════════════════════════════════
[INFO] Incident Summary: ...
       Root Cause: ...
       Resolution: ...
       Prevention: ...
```

## Hands-On Exercise

**`exercises/08_magentic/01_incident_response.py`** — Build a manager that coordinates diagnostic, infrastructure, and communication workers to respond to a production incident.

```bash
python exercises/08_magentic/01_incident_response.py
```

## Key Takeaways

1. Magentic = **adaptive planning with a task ledger**
2. The **task ledger** is shared mutable state maintained by the manager
3. Workers get **task-specific context only** — the manager controls information flow
4. The plan can **adapt** — new tasks added based on intermediate findings
5. The manager **synthesizes** all results into a final output

## References

- [MS Learn — Magentic Pattern](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [CAMEL: Communicative Agents for "Mind" Exploration (Li et al., 2023)](https://arxiv.org/abs/2303.17760)
