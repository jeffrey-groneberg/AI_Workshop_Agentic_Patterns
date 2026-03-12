# Exercise 02: Tool Use & Function Calling

## Objective

Learn how LLMs interact with external tools through function calling — the foundation of agentic behavior.

## Concepts Covered

- Tool definitions with `openai.pydantic_function_tool()`
- The `tools` parameter and strict mode
- Parsing `tool_calls` from model responses
- The agent loop: Reason → Act → Observe → Repeat
- `tool` role messages for returning results

## Files (in order)

1. **`01_function_calling.py`** — Define and invoke tools with Pydantic schemas
2. **`02_tool_loop.py`** — Full agent loop that runs until the model is done
3. **`tools/`** — Reusable mock tool implementations

## How to Run

```bash
python exercises/02_tool_use/01_function_calling.py
python exercises/02_tool_use/02_tool_loop.py
```

## Expected Output

Structured logging showing each loop iteration, tool calls with arguments, tool return values, and the final model response.

## Next

→ [Exercise 03: Single Agent](../03_single_agent/)
