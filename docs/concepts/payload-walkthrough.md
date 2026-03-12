# Payload Walkthrough — What Actually Goes Over the Wire

This page shows the **exact JSON payloads** exchanged between your code and the OpenAI API during function calling and the agent loop. No hand-waving — every field explained.

We'll trace through the weather assistant from [Exercise 02: Function Calling](../exercises/02_function_calling.md){:target="_blank"} step by step.

---

## The Setup

The user asks: *"What's the weather in Berlin and Tokyo? Also, convert 18°C to Fahrenheit."*

Your code defines two tools and sends an API request. Here's what happens at each step.

---

## Step 1: Your Code → API (Initial Request)

This is what `client.chat.completions.create()` sends to the API:

```json
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful weather assistant."
    },
    {
      "role": "user",
      "content": "What's the weather in Berlin and Tokyo? Also, convert 18°C to Fahrenheit."
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
          "type": "object",
          "properties": {
            "city": {
              "type": "string",
              "description": "City name to get weather for"
            },
            "unit": {
              "type": "string",
              "default": "celsius",
              "description": "Temperature unit: 'celsius' or 'fahrenheit'"
            }
          },
          "required": ["city", "unit"],
          "additionalProperties": false
        },
        "strict": true
      }
    },
    {
      "type": "function",
      "function": {
        "name": "convert_temperature",
        "description": "Convert temperature between Celsius and Fahrenheit",
        "parameters": {
          "type": "object",
          "properties": {
            "value": {
              "type": "number",
              "description": "Temperature value to convert"
            },
            "from_unit": {
              "type": "string",
              "description": "Source unit: 'celsius' or 'fahrenheit'"
            },
            "to_unit": {
              "type": "string",
              "description": "Target unit: 'celsius' or 'fahrenheit'"
            }
          },
          "required": ["value", "from_unit", "to_unit"],
          "additionalProperties": false
        },
        "strict": true
      }
    }
  ]
}
```

??? info "Where does the `tools` JSON come from?"

    You don't write this by hand. The SDK generates it from your Pydantic models:

    ```python
    class GetWeatherParams(BaseModel):
        city: str = Field(description="City name to get weather for")
        unit: str = Field(default="celsius", description="Temperature unit: 'celsius' or 'fahrenheit'")

    tools = [
        openai.pydantic_function_tool(GetWeatherParams, name="get_weather", description="Get current weather for a city"),
    ]
    ```

    `pydantic_function_tool()` converts the Pydantic model to a JSON Schema and wraps it in the `{"type": "function", "function": {...}}` structure. The `strict: true` field tells the API to guarantee the model's output exactly matches this schema.

**Key fields:**

| Field | Purpose |
|-------|---------|
| `tools[].type` | Always `"function"` — the only tool type currently supported |
| `tools[].function.name` | The function name the model will reference when making a call |
| `tools[].function.parameters` | JSON Schema describing the expected arguments |
| `tools[].function.strict` | When `true`, the model is **guaranteed** to produce valid JSON matching the schema |
| `additionalProperties: false` | Required by strict mode — no extra fields allowed |

---

## Step 2: API → Your Code (Tool Calls Response)

The model sees the user wants three things (Berlin weather, Tokyo weather, temperature conversion) and responds with **three parallel tool calls** in a single response:

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "model": "gpt-4o-2024-08-06",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_xK9f2a",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"city\": \"Berlin\", \"unit\": \"celsius\"}"
            }
          },
          {
            "id": "call_mP7b3c",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"city\": \"Tokyo\", \"unit\": \"celsius\"}"
            }
          },
          {
            "id": "call_qR4d5e",
            "type": "function",
            "function": {
              "name": "convert_temperature",
              "arguments": "{\"value\": 18.0, \"from_unit\": \"celsius\", \"to_unit\": \"fahrenheit\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ],
  "usage": {
    "prompt_tokens": 142,
    "completion_tokens": 85,
    "total_tokens": 227
  }
}
```

**Key observations:**

| Field | What it tells you |
|-------|-------------------|
| `content: null` | The model didn't produce text — it wants to call tools first |
| `finish_reason: "tool_calls"` | The model stopped because it wants tool results, not because it's done |
| `tool_calls` | An **array** — the model can request multiple tools at once (parallel calls) |
| `tool_calls[].id` | Unique ID — you must include this when returning the result so the API can match them up |
| `tool_calls[].function.arguments` | A **JSON string** (not an object) — you must `json.loads()` it |

!!! warning "Arguments are a string, not a dict"
    Notice `arguments` is `"{\"city\": \"Berlin\"}"` — a JSON-encoded **string**. Your code must parse it:
    ```python
    arguments = json.loads(tool_call.function.arguments)
    # Now it's a Python dict: {"city": "Berlin", "unit": "celsius"}
    ```

---

## Step 3: Your Code Executes the Tools

This happens entirely in your process — no API call. Your code looks up the function and calls it:

```python
for tool_call in assistant_message.tool_calls:
    function_name = tool_call.function.name        # "get_weather"
    arguments = json.loads(tool_call.function.arguments)  # {"city": "Berlin", "unit": "celsius"}

    result = TOOL_FUNCTIONS[function_name](**arguments)
    # → get_weather(city="Berlin", unit="celsius")
```

The `**arguments` unpacking converts the dict into keyword arguments — see the [Agent Run Loop](agent-run-loop.md) page for details on this Python pattern.

The mock functions return:

```python
# get_weather(city="Berlin", unit="celsius")
{"city": "Berlin", "temperature": 18, "unit": "°C", "condition": "Partly cloudy", "humidity": 65}

# get_weather(city="Tokyo", unit="celsius")
{"city": "Tokyo", "temperature": 28, "unit": "°C", "condition": "Sunny", "humidity": 45}

# convert_temperature(value=18.0, from_unit="celsius", to_unit="fahrenheit")
{"original": 18.0, "converted": 64.4, "from_unit": "celsius", "to_unit": "fahrenheit"}
```

---

## Step 4: Your Code → API (Tool Results)

Now your code sends **everything** back to the API — the original messages, the assistant's tool-call message, and all three tool results:

```json
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful weather assistant."
    },
    {
      "role": "user",
      "content": "What's the weather in Berlin and Tokyo? Also, convert 18°C to Fahrenheit."
    },
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_xK9f2a",
          "type": "function",
          "function": {
            "name": "get_weather",
            "arguments": "{\"city\": \"Berlin\", \"unit\": \"celsius\"}"
          }
        },
        {
          "id": "call_mP7b3c",
          "type": "function",
          "function": {
            "name": "get_weather",
            "arguments": "{\"city\": \"Tokyo\", \"unit\": \"celsius\"}"
          }
        },
        {
          "id": "call_qR4d5e",
          "type": "function",
          "function": {
            "name": "convert_temperature",
            "arguments": "{\"value\": 18.0, \"from_unit\": \"celsius\", \"to_unit\": \"fahrenheit\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_xK9f2a",
      "content": "{\"city\": \"Berlin\", \"temperature\": 18, \"unit\": \"°C\", \"condition\": \"Partly cloudy\", \"humidity\": 65}"
    },
    {
      "role": "tool",
      "tool_call_id": "call_mP7b3c",
      "content": "{\"city\": \"Tokyo\", \"temperature\": 28, \"unit\": \"°C\", \"condition\": \"Sunny\", \"humidity\": 45}"
    },
    {
      "role": "tool",
      "tool_call_id": "call_qR4d5e",
      "content": "{\"original\": 18.0, \"converted\": 64.4, \"from_unit\": \"celsius\", \"to_unit\": \"fahrenheit\"}"
    }
  ],
  "tools": [...]
}
```

**Key observations:**

| Field | Why it matters |
|-------|---------------|
| `role: "assistant"` with `tool_calls` | You **must** include the assistant's tool-call message — the API needs to see what it asked for |
| `role: "tool"` | The role for tool results (not `"function"` — that's deprecated) |
| `tool_call_id` | Links each result to the specific tool call that requested it |
| `content` | The tool result as a **JSON string** — always use `json.dumps()` |
| `tools: [...]` | You send the full tool definitions again — the API is stateless |

!!! tip "The API is stateless"
    Every request must include the **full** messages history and **all** tool definitions. The API doesn't remember previous calls. This is why the `messages` list keeps growing.

---

## Step 5: API → Your Code (Final Response)

The model now has all three tool results and produces its final text answer:

```json
{
  "id": "chatcmpl-def456",
  "object": "chat.completion",
  "model": "gpt-4o-2024-08-06",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Here's what I found:\n\n**Berlin**: 18°C, partly cloudy, humidity at 65%.\n**Tokyo**: 28°C, sunny, humidity at 45%.\n\nAnd 18°C converts to **64.4°F**."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 385,
    "completion_tokens": 52,
    "total_tokens": 437
  }
}
```

| Field | What changed |
|-------|-------------|
| `content` | Now contains text — the model has its answer |
| `finish_reason: "stop"` | The model is done — no more tool calls needed |
| `tool_calls` | Absent — only present when the model wants to call tools |

---

## The Complete Messages Timeline

Here's how the `messages` list grows through the entire exchange:

```
Request 1 (2 messages):
┌──────────────────────────────────────────────────────┐
│ [0] system:    "You are a helpful weather assistant." │
│ [1] user:      "What's the weather in Berlin..."      │
└──────────────────────────────────────────────────────┘
                         ↓ API Call ↓
                  Model returns 3 tool_calls

After appending tool calls + results (6 messages):
┌──────────────────────────────────────────────────────┐
│ [0] system:    "You are a helpful weather assistant." │
│ [1] user:      "What's the weather in Berlin..."      │
│ [2] assistant: tool_calls: [get_weather, get_weather, │
│                             convert_temperature]      │
│ [3] tool:      Berlin weather result                  │
│ [4] tool:      Tokyo weather result                   │
│ [5] tool:      Conversion result                      │
└──────────────────────────────────────────────────────┘
                         ↓ API Call ↓
                  Model returns final text

After final response (7 messages):
┌──────────────────────────────────────────────────────┐
│ [0] system:    "You are a helpful weather assistant." │
│ [1] user:      "What's the weather in Berlin..."      │
│ [2] assistant: tool_calls: [3 calls]                  │
│ [3] tool:      Berlin weather result                  │
│ [4] tool:      Tokyo weather result                   │
│ [5] tool:      Conversion result                      │
│ [6] assistant: "Here's what I found: ..."             │
└──────────────────────────────────────────────────────┘
```

---

## Multi-Turn: What Happens on the Next User Message

If the user follows up with *"What about Paris?"*, the messages list keeps growing:

```
┌──────────────────────────────────────────────────────┐
│ [0] system:    "You are a helpful weather assistant." │
│ [1] user:      "What's the weather in Berlin..."      │
│ [2] assistant: tool_calls: [3 calls]                  │
│ [3] tool:      Berlin weather result                  │
│ [4] tool:      Tokyo weather result                   │
│ [5] tool:      Conversion result                      │
│ [6] assistant: "Here's what I found: ..."             │
│ [7] user:      "What about Paris?"                    │  ← new
└──────────────────────────────────────────────────────┘
                         ↓ API Call ↓
                  Model returns 1 tool_call

┌──────────────────────────────────────────────────────┐
│ [0-7] ...previous messages...                         │
│ [8] assistant: tool_calls: [get_weather("Paris")]     │  ← new
│ [9] tool:      Paris weather result                   │  ← new
└──────────────────────────────────────────────────────┘
                         ↓ API Call ↓
                  Model returns final text

┌──────────────────────────────────────────────────────┐
│ [0-9] ...previous messages...                         │
│ [10] assistant: "Paris is 20°C and overcast."         │  ← new
└──────────────────────────────────────────────────────┘
```

This is why context management matters for long conversations — the messages list grows indefinitely. See [Context Management](../production-considerations/context-management.md) for strategies.

---

## The Agent Loop in Code

Putting it all together, here's the complete loop that handles any number of tool-calling rounds:

```python
messages = [
    {"role": "system", "content": "You are a helpful weather assistant."},
    {"role": "user", "content": user_query},
]

while True:
    # ── Send everything to the API ──
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
    )

    assistant_message = response.choices[0].message
    messages.append(assistant_message.model_dump())

    # ── No tool calls? We're done ──
    if not assistant_message.tool_calls:
        print(assistant_message.content)
        break

    # ── Execute each tool call ──
    for tool_call in assistant_message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        result = tool_functions[name](**args)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result),
        })

    # Loop back → send tool results to the API
```

This is exactly what the shared `run()` function does — see [The Agent Run Loop](agent-run-loop.md) for the annotated version.

---

## Common Mistakes

!!! danger "Forgetting to append the assistant message"
    ```python
    # ❌ Wrong — skipping the assistant's tool_call message
    for tool_call in message.tool_calls:
        messages.append({"role": "tool", ...})

    # ✅ Correct — append assistant message FIRST, then tool results
    messages.append(message.model_dump())
    for tool_call in message.tool_calls:
        messages.append({"role": "tool", ...})
    ```
    The API needs to see `assistant → tool` pairs. Without the assistant message, the tool results are orphaned and the API returns an error.

!!! danger "Using the wrong role"
    ```python
    # ❌ Wrong — "function" role is deprecated
    {"role": "function", "name": "get_weather", "content": "..."}

    # ✅ Correct — use "tool" role with tool_call_id
    {"role": "tool", "tool_call_id": "call_xK9f2a", "content": "..."}
    ```

!!! danger "Forgetting `tool_call_id`"
    Each tool result **must** reference the specific `tool_call.id` from the assistant's response. The API uses this to match results to requests, especially when there are parallel calls.

!!! danger "Sending tool result as dict instead of string"
    ```python
    # ❌ Wrong — content must be a string
    {"role": "tool", "content": {"temperature": 18}}

    # ✅ Correct — JSON-serialize the result
    {"role": "tool", "content": json.dumps({"temperature": 18})}
    ```
