# Exercise 03: Single Agent

## Objective

Build a complete single agent with multiple tools — the building block for all orchestration patterns.

## Concepts Covered

- Agent with multiple tools (order lookup, FAQ search, refund processing)
- Conversation loop handling multi-turn interactions
- When a single agent is sufficient
- Context window growth in long conversations

## How It Works

This exercise uses the shared `Agent` dataclass and `run()` function from `commons/agent.py`. The agent is configured with a system prompt, three tools (`lookup_order`, `search_faq`, `process_refund`), and a tool function mapping. Three separate customer messages are sent sequentially, simulating a multi-turn support conversation.

```mermaid
sequenceDiagram
    participant Customer as Customer (Script)
    participant Agent as Support Agent
    participant LLM as LLM Provider
    participant Tools as Tool Functions

    Note over Customer,Tools: Turn 1 — "Where is my order ORD-12345?"
    Customer->>Agent: User message added to messages list
    Agent->>LLM: messages=[system, user] + tools
    LLM-->>Agent: tool_calls: [lookup_order("ORD-12345")]
    Agent->>Tools: lookup_order("ORD-12345")
    Tools-->>Agent: {status: "shipped", eta: "2 days"}
    Agent->>LLM: messages=[...previous + tool result]
    LLM-->>Agent: "Your order is shipped, arriving in 2 days"
    Agent-->>Customer: Response

    Note over Customer,Tools: Turn 2 — "What's your return policy?"
    Customer->>Agent: New user message appended to SAME list
    Agent->>LLM: messages=[...all previous + new user msg] + tools
    LLM-->>Agent: tool_calls: [search_faq("return policy")]
    Agent->>Tools: search_faq("return policy")
    Tools-->>Agent: FAQ result
    Agent->>LLM: messages=[...previous + tool result]
    LLM-->>Agent: "You can return within 30 days..."
    Agent-->>Customer: Response

    Note over Customer,Tools: Turn 3 — "Process a refund"
    Customer->>Agent: New user message appended to SAME list
    Agent->>LLM: messages=[...all previous + new user msg] + tools
    LLM-->>Agent: tool_calls: [process_refund(...)]
    Agent->>Tools: process_refund(...)
    Tools-->>Agent: {refund_id: "REF-001", status: "approved"}
    Agent->>LLM: messages=[...previous + tool result]
    LLM-->>Agent: "Your refund has been approved"
    Agent-->>Customer: Response
```

**Context sharing:** A **single `messages` list persists across all three turns**. This list IS the agent's memory — the model sees the full conversation history on every call, including previous tool calls and results. This means by Turn 3, the model knows about the order lookup from Turn 1 and the FAQ search from Turn 2.

**Structured output:** Not used. Tool inputs use Pydantic schemas for validation, but responses are plain text. Inter-turn context is carried entirely in the growing messages list.

!!! warning "Context window growth"
    In a real application, this messages list grows without bound. Long conversations will eventually exceed the model's context window. Production systems need strategies like summarization or sliding windows — covered in the [Context Management](../production-considerations/context-management.md) section.

## Files

1. **`01_customer_support_agent.py`** — Customer support agent with order, FAQ, and refund tools

## How to Run

```bash
python exercises/03_single_agent/01_customer_support_agent.py
```

## Expected Output

A multi-turn support conversation showing the agent selecting appropriate tools, executing them, and composing responses.

## Next

→ [Exercise 04: Sequential Pattern](04_sequential.md)
