# System Prompts

System prompts are the primary way to define an agent's personality, expertise, and constraints. They are the foundation of **agent identity** — when we build multi-agent systems later, each agent gets a different system prompt that defines its role.

## How System Prompts Work

The `system` role message is always the first message in the messages list. It sets the model's behavior for the entire conversation:

```python
messages = [
    {"role": "system", "content": "You are a senior financial advisor. Be precise and professional."},
    {"role": "user", "content": "Should I invest in index funds?"},
]
```

The model treats the system prompt as its **identity** — it shapes tone, expertise, format, and constraints for all subsequent turns.

## Same Query, Different Personas

The same user query with different system prompts produces completely different responses:

```python
# Formal advisor
{"role": "system", "content": "You are a senior financial advisor. Be precise and professional."}

# Casual buddy
{"role": "system", "content": "You are a chill friend who knows about money. Keep it casual."}
```

Both receive the same question, but the first responds with structured recommendations and caveats, while the second gives relaxed, conversational advice.

## Best Practices for System Prompts

| Practice | Example |
|----------|---------|
| **Define the role clearly** | "You are a customer support agent for an e-commerce platform." |
| **Set constraints** | "Keep responses under 100 words. Never discuss competitor products." |
| **Specify format** | "Always respond with a numbered list of recommendations." |
| **Include expertise** | "You have deep knowledge of AWS infrastructure and Kubernetes." |
| **Add guardrails** | "If you don't know the answer, say 'I'm not sure' instead of guessing." |

## System Prompts in Multi-Agent Systems

In this workshop's multi-agent exercises, system prompts are what differentiate agents:

- **Sequential pattern** — each pipeline stage has a specialized system prompt (researcher, writer, editor)
- **Group chat** — the same shared conversation, but each agent's system prompt is prepended before its turn
- **Handoff** — the triage agent and specialist agents have different system prompts defining their scope

!!! tip "Temperature for system prompts"
    Pair system prompts with appropriate temperature settings. A formal advisor works best with low temperature (`0.0`–`0.3`), while a creative brainstormer benefits from higher values (`0.7`–`1.0`).

## Key Takeaways

1. **System prompts define agent identity** — the same model becomes different agents with different prompts
2. System prompts set tone, expertise, format, and constraints
3. In multi-agent systems, each agent gets its own system prompt
4. Pair prompts with appropriate temperature settings for best results

## Hands-On Exercise

Now try it yourself — head to the [System Prompts exercise](../exercises/01_system_prompts.md){:target="_blank"} to see how the same query gets different responses with different personas.

You can run exercises from the terminal or use the [Workshop TUI](../workshop-tui.md).
