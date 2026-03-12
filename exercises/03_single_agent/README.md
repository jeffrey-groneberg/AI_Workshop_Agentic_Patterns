# Exercise 03: Single Agent

## Objective

Build a complete single agent with multiple tools — the building block for all orchestration patterns.

## Concepts Covered

- Agent with multiple tools (order lookup, FAQ search, refund processing)
- Conversation loop handling multi-turn interactions
- When a single agent is sufficient
- Context window growth in long conversations

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
