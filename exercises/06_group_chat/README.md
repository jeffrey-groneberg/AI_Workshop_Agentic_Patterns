# Exercise 06: Group Chat Pattern

## Objective

Implement multi-agent group conversations with shared context, including the maker-checker (reflection) variant.

## Concepts Covered

- Shared conversation thread across agents
- Chat manager for speaking order and termination
- Maker-checker / evaluator-optimizer loop
- Context window management in multi-agent conversations

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

→ [Exercise 07: Handoff Pattern](../07_handoff/)
