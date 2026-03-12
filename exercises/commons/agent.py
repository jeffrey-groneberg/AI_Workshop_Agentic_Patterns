"""
Minimal Agent abstraction — a dataclass and a run function.

This is intentionally simple: no framework, no magic. The agent loop is explicit
and visible so participants understand every step of Reason → Act → Observe.
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Callable

import openai
from openai import OpenAI, AzureOpenAI

logger = logging.getLogger(__name__)

# Maximum tool-call iterations to prevent infinite loops
DEFAULT_MAX_ITERATIONS = 10


@dataclass
class Agent:
    """
    A minimal agent definition.

    Attributes:
        name: Human-readable name (used in logging).
        system_prompt: The system/developer message that defines agent behavior.
        tools: List of tool definitions created via openai.pydantic_function_tool().
        tool_functions: Mapping of tool name → callable Python function.
        model: Model name to use (defaults to provider default via get_model()).
        max_iterations: Safety limit on tool-call loop iterations.
    """

    name: str
    system_prompt: str
    tools: list[dict[str, Any]] = field(default_factory=list)
    tool_functions: dict[str, Callable[..., Any]] = field(default_factory=dict)
    model: str = ""
    max_iterations: int = DEFAULT_MAX_ITERATIONS


def run(
    agent: Agent,
    messages: list[dict[str, Any]],
    client: OpenAI | AzureOpenAI,
    model: str | None = None,
) -> str:
    """
    Execute the agent loop: send messages → handle tool calls → repeat until done.

    This is the core agent loop that all exercises build on. It runs synchronously
    and returns the final text response from the model.

    Args:
        agent: The Agent definition (system prompt, tools, tool functions).
        messages: The conversation messages (will be mutated with new messages).
        client: An OpenAI or AzureOpenAI client instance.
        model: Override model name (uses agent.model if not provided).

    Returns:
        The final assistant text response.
    """
    effective_model = model or agent.model
    if not effective_model:
        from exercises.commons.llm_client import get_model

        effective_model = get_model()

    # Ensure system prompt is the first message
    if not messages or messages[0].get("role") != "system":
        messages.insert(0, {"role": "system", "content": agent.system_prompt})

    iteration = 0

    while iteration < agent.max_iterations:
        iteration += 1
        logger.info("[%s] [Loop %d] Sending request to model", agent.name, iteration)

        # Build the API call arguments
        api_kwargs: dict[str, Any] = {
            "model": effective_model,
            "messages": messages,
        }
        if agent.tools:
            api_kwargs["tools"] = agent.tools

        response = client.chat.completions.create(**api_kwargs)
        choice = response.choices[0]
        assistant_message = choice.message

        # Append the assistant message to the conversation
        messages.append(assistant_message.model_dump())

        # If no tool calls, we have a final response
        if not assistant_message.tool_calls:
            logger.info(
                "[%s] [Loop %d] Model produced final response (finish_reason=%s)",
                agent.name,
                iteration,
                choice.finish_reason,
            )
            return assistant_message.content or ""

        # Process each tool call
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            logger.info(
                "[%s] [Loop %d] Model requested tool call → %s(%s)",
                agent.name,
                iteration,
                function_name,
                ", ".join(f"{k}={v!r}" for k, v in arguments.items()),
            )

            # Execute the tool function
            if function_name not in agent.tool_functions:
                error_result = f"Error: Unknown tool '{function_name}'"
                logger.warning("[%s] %s", agent.name, error_result)
                result = error_result
            else:
                result = agent.tool_functions[function_name](**arguments)

            result_str = json.dumps(result) if not isinstance(result, str) else result
            logger.info(
                "[%s] [Tool] %s → %s",
                agent.name,
                function_name,
                result_str[:200] + ("..." if len(result_str) > 200 else ""),
            )

            # Append the tool result to the conversation
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result_str,
                }
            )

    logger.warning(
        "[%s] Reached maximum iterations (%d) — returning last response",
        agent.name,
        agent.max_iterations,
    )
    # Return whatever content we have from the last assistant message
    return messages[-1].get("content", "") if messages else ""
