# The Responses API

!!! info "Forward-Looking"
    This page covers OpenAI's new Responses API — the future direction of the platform. The workshop exercises use the **Chat Completions API** because it works across all providers (OpenAI, Azure, GitHub Models). This page helps you understand where things are headed.

## Why a New API?

The Responses API (`client.responses.create()`) is OpenAI's new primary API, designed to simplify patterns that were complex with Chat Completions:

- **Built-in tools** — web search, file search, code interpreter (no external setup)
- **Simpler conversation passing** — pass `previous_response_id` instead of the whole message list
- **Flat tool definitions** — no nested `function` wrapper
- **Chain-of-thought passing** — include reasoning tokens from previous calls
- **Output compaction** — automatically summarize long conversations

## Side-by-Side Comparison

### Basic Chat

=== "Chat Completions (Workshop API)"

    ```python
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ],
    )
    text = response.choices[0].message.content
    ```

=== "Responses API"

    ```python
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions="You are a helpful assistant.",
        input="Hello!",
    )
    text = response.output_text
    ```

### Tool Definitions

=== "Chat Completions (Workshop API)"

    ```python
    tools = [
        openai.pydantic_function_tool(
            GetWeatherParams,
            name="get_weather",
            description="Get weather for a city",
        ),
    ]
    ```

=== "Responses API"

    ```python
    tools = [
        {
            "type": "function",
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": { ... },
        },
    ]
    ```

### Tool Results

=== "Chat Completions (Workshop API)"

    ```python
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(result),
    })
    ```

=== "Responses API"

    ```python
    input_items.append({
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": json.dumps(result),
    })
    ```

### Conversation Continuity

=== "Chat Completions (Workshop API)"

    ```python
    # You must pass the full message history every time
    messages.append({"role": "user", "content": "Follow-up question"})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,  # Full history
    )
    ```

=== "Responses API"

    ```python
    # Just reference the previous response
    response = client.responses.create(
        model="gpt-4o-mini",
        input="Follow-up question",
        previous_response_id=previous_response.id,
    )
    ```

## Key Differences

| Feature | Chat Completions | Responses API |
|---------|-----------------|---------------|
| **Endpoint** | `/chat/completions` | `/responses` |
| **Input format** | `messages` list | `input` (string or items) |
| **System prompt** | `system` role message | `instructions` parameter |
| **History** | Pass full `messages` | `previous_response_id` |
| **Tool defs** | Nested under `function` | Flat at top level |
| **Tool results** | `tool` role | `function_call_output` type |
| **Output text** | `choices[0].message.content` | `output_text` |
| **Built-in tools** | No | web_search, file_search, code_interpreter |
| **Provider support** | OpenAI, Azure, GitHub Models | OpenAI only (currently) |
| **Status** | Supported indefinitely | New primary API |

## Why the Workshop Uses Chat Completions

1. **Cross-provider compatibility** — Azure OpenAI and GitHub Models use Chat Completions. The Responses API may not be available on all providers.
2. **Universal patterns** — The concepts (messages, tools, loops) transfer directly to any provider or framework.
3. **Stability** — Chat Completions is mature and "supported indefinitely" per OpenAI.

## Translation Guide

If you want to convert any workshop exercise to the Responses API:

1. Replace `client.chat.completions.create()` → `client.responses.create()`
2. Move the `system` message → `instructions` parameter
3. Replace `messages` → `input`
4. Replace `response.choices[0].message` → check `response.output` items
5. Replace `.content` → `.output_text` for final text
6. Replace `tool` role messages → `function_call_output` items
7. For multi-turn: store `response.id` and pass as `previous_response_id`

## Key Takeaways

1. The Responses API is OpenAI's forward direction — simpler, with built-in tools
2. Chat Completions isn't going away — it's "supported indefinitely"
3. The core concepts are the same: messages, tools, loops
4. Cross-provider workshops like this one benefit from Chat Completions' universal support
5. Understanding Chat Completions makes it easy to adopt the Responses API later

## References

- [OpenAI Responses API Guide](https://platform.openai.com/docs/guides/responses-vs-chat-completions)
- [OpenAI Responses API Reference](https://platform.openai.com/docs/api-reference/responses)
- [OpenAI Migration Guide: Chat Completions → Responses](https://platform.openai.com/docs/guides/responses-vs-chat-completions)
