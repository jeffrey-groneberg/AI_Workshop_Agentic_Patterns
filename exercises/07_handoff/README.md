# Exercise 07: Handoff Pattern

## Objective

Implement dynamic routing where a triage agent analyzes queries and hands off to specialist agents.

## Concepts Covered

- Triage / routing agent with classification
- Structured handoff context (dataclass with query, category, relevant info)
- Specialist agents with focused capabilities
- Context passing strategies (full history vs. summary vs. structured object)

## Files

1. **`01_support_triage.py`** — Triage agent routes to billing, technical, or account specialists

## How to Run

```bash
python exercises/07_handoff/01_support_triage.py
```

## Expected Output

Logging showing the triage classification, handoff decision with reasoning, structured context passed to the specialist, and the specialist's resolution.

## Next

→ [Exercise 08: Magentic Pattern](08_magentic.md)
