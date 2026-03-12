# Reliability

Agents make LLM calls and execute tools — both can fail. Building reliable agents means handling failures gracefully and preventing runaway behavior.

## Common Failure Modes

| Failure | Cause | Symptom |
|---------|-------|---------|
| **API timeout** | Network issues, rate limiting | `openai.APITimeoutError` |
| **Rate limiting** | Too many requests per minute | `openai.RateLimitError` (HTTP 429) |
| **Invalid tool args** | Model produces bad function arguments | `json.JSONDecodeError`, missing keys |
| **Infinite loops** | Model keeps calling tools without converging | Agent runs forever |
| **Context overflow** | Conversation exceeds token limit | `openai.BadRequestError` |
| **Refusal** | Model declines to answer | Empty response or safety refusal |

## Max Iterations: The Essential Guardrail

Every agent loop **must** have a maximum iteration limit:

```python
@dataclass
class Agent:
    max_iterations: int = 10  # Never remove this

def run(agent, messages, client):
    for i in range(agent.max_iterations):
        response = client.chat.completions.create(...)
        if response.choices[0].finish_reason == "stop":
            return response.choices[0].message.content
        # ... handle tool calls
    return "Max iterations reached"
```

Without this, a confused model can loop forever. This is the single most important reliability measure.

## Retry with Exponential Backoff

For transient API errors, retry with increasing delays:

```python
import time
from openai import APITimeoutError, RateLimitError

def call_with_retry(fn, max_retries=3):
    """Retry a function call with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return fn()
        except (APITimeoutError, RateLimitError) as e:
            if attempt == max_retries - 1:
                raise
            delay = 2 ** attempt  # 1s, 2s, 4s
            logging.warning("Retry %d/%d after %ds: %s", attempt + 1, max_retries, delay, e)
            time.sleep(delay)
```

!!! tip "Don't retry everything"
    Only retry **transient** errors (timeouts, rate limits). Don't retry **permanent** errors like invalid API keys or malformed requests.

## Tool Execution Safety

Tools execute arbitrary code. Guard against unexpected inputs:

```python
def execute_tool(name: str, args: dict, tool_functions: dict) -> str:
    """Safely execute a tool function."""
    fn = tool_functions.get(name)
    if fn is None:
        return json.dumps({"error": f"Unknown tool: {name}"})

    try:
        result = fn(**args)
        return json.dumps(result) if not isinstance(result, str) else result
    except Exception as e:
        return json.dumps({"error": str(e)})
```

Return error messages as tool results rather than crashing — the model can often recover from a tool error by trying a different approach.

## Timeout Patterns

Set timeouts at multiple levels:

```python
# Per-request timeout
response = client.chat.completions.create(
    model=model,
    messages=messages,
    timeout=30.0,  # 30-second timeout
)

# Per-agent timeout (wall clock)
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Agent execution timed out")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(120)  # 2-minute total timeout
try:
    result = run(agent, messages, client)
finally:
    signal.alarm(0)  # Cancel alarm
```

## Circuit Breaker Pattern

For systems with multiple agents, a circuit breaker prevents cascading failures:

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=60):
        self.failures = 0
        self.threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure = 0

    def call(self, fn):
        if self.failures >= self.threshold:
            elapsed = time.time() - self.last_failure
            if elapsed < self.reset_timeout:
                raise RuntimeError("Circuit breaker open — too many failures")
            self.failures = 0  # Reset after timeout

        try:
            result = fn()
            self.failures = 0
            return result
        except Exception:
            self.failures += 1
            self.last_failure = time.time()
            raise
```

## Graceful Degradation

When a specialist agent fails, the system should still produce useful output:

```python
try:
    result = run_worker(client, model, worker_name, task)
except Exception as e:
    logger.warning("[%s] Worker failed: %s — using fallback", worker_name, e)
    result = f"Unable to complete task: {task.description}. Error: {e}"
    # The manager can still synthesize a report from partial results
```

## Key Takeaways

1. **Max iterations** is non-negotiable — every agent loop needs a hard limit
2. **Retry transient errors** (timeouts, rate limits) with exponential backoff
3. **Return errors as tool results** — let the model recover gracefully
4. **Set timeouts** at both request and agent levels
5. **Design for partial failure** — a multi-agent system should degrade gracefully

## References

- [OpenAI Error Handling Guide](https://platform.openai.com/docs/guides/error-codes)
- [OpenAI Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
