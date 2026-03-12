# Brainstorm (Round-Robin) Pattern

The brainstorm pattern puts multiple agents in a shared conversation where they take turns in a **fixed, repeating order** (round-robin), building on each other's messages.

## Pattern Architecture

```mermaid
graph TD
    M[Chat Manager] --> A1[Agent A<br/>Product Manager]
    M --> A2[Agent B<br/>Designer]
    M --> A3[Agent C<br/>Engineer]
    A1 --> SC[Shared Conversation]
    A2 --> SC
    A3 --> SC
    SC --> M

    style M fill:#607D8B,color:white
    style A1 fill:#2196F3,color:white
    style A2 fill:#FF9800,color:white
    style A3 fill:#4CAF50,color:white
```

## When to Use

- The task benefits from **multiple perspectives debating** the same problem
- Agents need to **build on each other's ideas**
- You want **predictable, democratic** conversations where every voice is heard equally
- Examples: brainstorming, collaborative planning, requirements gathering

## When to Avoid

- Agents don't need to see each other's output (use [Concurrent](concurrent.md))
- Tasks have a clear linear flow (use [Sequential](sequential.md))
- You need dynamic routing (use [Handoff](handoff.md))
- You need iterative quality refinement (use [Maker-Checker](maker-checker.md))

## Context Passing Strategy

All agents share the **same conversation thread** — a single `messages` list that grows with every turn. This is the "shared memory" approach.

```mermaid
sequenceDiagram
    participant M as Manager
    participant PM as Product Manager
    participant D as Designer
    participant E as Engineer
    participant Conv as Shared Messages

    M->>PM: Your turn to speak
    PM->>Conv: "I think we should focus on..."
    M->>D: Your turn to speak
    Note over D,Conv: Designer sees PM's<br/>message in full history
    D->>Conv: "Building on that, the UX should..."
    M->>E: Your turn to speak
    Note over E,Conv: Engineer sees PM's AND<br/>Designer's messages
    E->>Conv: "Technically, we could implement..."
```

**Why shared conversation?**

- Agents naturally build on each other's ideas
- Context accumulates — later agents have richer information
- Simulates a real team discussion

**Trade-off**: The message list grows with every turn, which can hit token limits in long discussions. For production systems, consider summarization between rounds.

## What We're Building

### [Brainstorm Exercise](../exercises/06_brainstorm.md){:target="_blank"}

```mermaid
graph TD
    T[Topic: Mobile app<br/>idea for seniors] --> PM[Product Manager<br/>Business viability]
    T --> D[Designer<br/>UX and accessibility]
    T --> E[Engineer<br/>Technical feasibility]
    PM --> SC[Shared Conversation<br/>3 rounds × 3 agents]
    D --> SC
    E --> SC
    SC --> S[Summary of discussion]

    style PM fill:#2196F3,color:white
    style D fill:#FF9800,color:white
    style E fill:#4CAF50,color:white
```

## Expected Console Output

```
══════════════════════════════════════════════════════════════════
  Group Chat: Brainstorm
══════════════════════════════════════════════════════════════════
[INFO] Topic: Design a mobile app for seniors

══════════════════════════════════════════════════════════════════
  Round 1 of 3
══════════════════════════════════════════════════════════════════
[INFO] [Product Manager] From a business perspective, the senior
       demographic is growing rapidly...
[INFO] [Designer] Accessibility is paramount. Large fonts, high
       contrast, simple navigation...
[INFO] [Engineer] We should consider offline capabilities and
       low bandwidth support...

══════════════════════════════════════════════════════════════════
  Round 2 of 3
══════════════════════════════════════════════════════════════════
[INFO] [Product Manager] Building on the accessibility points...
```

!!! tip "Ready to practice?"
    Continue with the hands-on exercise in the sidebar (✏️) to apply what you've learned.

## Key Takeaways

1. Round-robin = **fixed, repeating turn order** — predictable and democratic
2. All agents share the **same conversation thread** — each sees the full history
3. A **chat manager** controls turn order and termination
4. Shared context enables agents to build on each other's ideas
5. Watch token usage — shared conversations grow with every turn

## References

- [MS Learn — Group Chat Pattern](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Andrew Ng — Multi-Agent Collaboration (YouTube)](https://www.youtube.com/watch?v=sal78ACtGTc)
- [Microsoft Agent Framework — Group Chat Orchestration](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/group-chat)

## Hands-On Exercise

Head to the [Brainstorm exercise](../exercises/06_brainstorm.md){:target="_blank"} — PM, Designer, and Engineer debate a product idea in rounds.

You can run exercises from the terminal or use the [Workshop TUI](../workshop-tui.md).
