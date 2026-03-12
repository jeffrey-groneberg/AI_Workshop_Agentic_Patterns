# Exercise 01: LLM Basics

## Objective

Learn the fundamentals of interacting with Large Language Models through the Chat Completions API.

## Concepts Covered

- Messages list and roles (system, user, assistant)
- Temperature and max_tokens parameters
- System prompts for shaping agent behavior
- Structured outputs with Pydantic models

## Files (in order)

1. **`01_chat_completion.py`** — Basic chat completion with a travel assistant
2. **`02_system_prompts.py`** — Same query, different personas via system prompts
3. **`03_structured_outputs.py`** — Extract structured data using `client.chat.completions.parse()`

## How to Run

```bash
python exercises/01_llm_basics/01_chat_completion.py
python exercises/01_llm_basics/02_system_prompts.py
python exercises/01_llm_basics/03_structured_outputs.py
```

## Expected Output

Each script produces structured logging showing the LLM interaction, the messages sent, and the response received.

## Next

→ [Exercise 02: Tool Use](02_tool_use.md)
