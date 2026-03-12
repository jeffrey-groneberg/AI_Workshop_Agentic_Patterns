# Exercise 08: Magentic Pattern

## Objective

Implement adaptive planning where a manager agent builds and executes a dynamic task ledger, delegating to specialist workers.

## Concepts Covered

- Task ledger as shared mutable state
- Manager agent that creates, assigns, and tracks tasks
- Worker agents receiving task-specific context only
- Dynamic plan adjustment based on findings
- Synthesis of worker results

## Files

1. **`01_incident_response.py`** — Manager handles an incident by coordinating diagnostic, infrastructure, and communication agents

## How to Run

```bash
python exercises/08_magentic/01_incident_response.py
```

## Expected Output

Logging showing the task ledger being built, tasks assigned to workers, worker results flowing back, plan adjustments, and the final incident report.

## Next

→ Return to the [documentation site](../../docs/) to review implementation considerations.
