# Exercise 04: Sequential Pattern

## Objective

Implement a multi-agent pipeline where each agent's output feeds into the next — the sequential orchestration pattern.

## Concepts Covered

- Linear agent pipeline (Research → Draft → Edit)
- Fresh context per stage (only passing the previous agent's output)
- Progressive refinement of content
- Context compaction between stages

## Files

1. **`01_content_pipeline.py`** — Three-agent content pipeline that produces a polished article

## How to Run

```bash
python exercises/04_sequential/01_content_pipeline.py
```

## Expected Output

Structured logging showing each pipeline stage, what context is passed between agents, and the progressive refinement of the article.

## Next

→ [Exercise 05: Concurrent Pattern](05_concurrent.md)
