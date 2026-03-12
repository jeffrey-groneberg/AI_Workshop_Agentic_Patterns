# Exercise 05: Concurrent Pattern

## Objective

Implement fan-out/fan-in execution where multiple agents work in parallel, then results are aggregated.

## Concepts Covered

- Parallel agent execution with `concurrent.futures`
- Independent context per agent (no shared state between parallel agents)
- Result aggregation by a synthesizer agent
- Fan-out/fan-in architecture

## Files

1. **`01_stock_analysis.py`** — Three parallel analyst agents + an aggregator for stock analysis

## How to Run

```bash
python exercises/05_concurrent/01_stock_analysis.py
```

## Expected Output

Logging showing parallel agent launches, individual completions, and the final aggregated analysis.

## Next

→ [Exercise 06: Group Chat Pattern](../06_group_chat/)
