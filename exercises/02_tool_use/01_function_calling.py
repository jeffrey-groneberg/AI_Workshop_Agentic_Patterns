"""
Exercise 02.1 — Function Calling

Defines tools using openai.pydantic_function_tool() with Pydantic models for
strict-mode schemas. Sends to the model, parses tool_calls, executes locally,
and returns results with the `tool` role.

Scenario: A weather lookup + temperature converter.

How to run:
    python exercises/02_tool_use/01_function_calling.py

Pattern: None (foundational — introduces function calling)
"""

import json
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import openai
from pydantic import BaseModel, Field

from exercises.commons.llm_client import get_client, get_model
from exercises.commons.utils import setup_logging, log_stage
from exercises.02_tool_use.tools import get_weather, convert_temperature

logger = logging.getLogger(__name__)

# ── Pydantic models for tool parameter schemas ──────────────────────────────
# These models define the tool's input schema. The SDK converts them to
# JSON Schema and sends them to the model with strict mode enabled.


class GetWeatherParams(BaseModel):
    """Parameters for the get_weather tool."""

    city: str = Field(description="City name to get weather for")
    unit: str = Field(
        default="celsius",
        description="Temperature unit: 'celsius' or 'fahrenheit'",
    )


class ConvertTemperatureParams(BaseModel):
    """Parameters for the convert_temperature tool."""

    value: float = Field(description="Temperature value to convert")
    from_unit: str = Field(description="Source unit: 'celsius' or 'fahrenheit'")
    to_unit: str = Field(description="Target unit: 'celsius' or 'fahrenheit'")


# ── Tool definitions ────────────────────────────────────────────────────────
# openai.pydantic_function_tool() creates a tool definition from a Pydantic
# model. This is the modern pattern — NOT the deprecated `functions` parameter.

TOOLS = [
    openai.pydantic_function_tool(GetWeatherParams, name="get_weather", description="Get current weather for a city"),
    openai.pydantic_function_tool(
        ConvertTemperatureParams,
        name="convert_temperature",
        description="Convert temperature between Celsius and Fahrenheit",
    ),
]

# Map tool names to their Python implementations
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "convert_temperature": convert_temperature,
}

USER_QUERY = "What's the weather in Berlin and Tokyo? Also, convert 18°C to Fahrenheit."


def main() -> None:
    setup_logging()

    log_stage("Function Calling with Pydantic Tool Definitions")

    model = get_model()
    logger.info("Using model: %s", model)

    with get_client() as client:
        messages = [
            {"role": "system", "content": "You are a helpful weather assistant."},
            {"role": "user", "content": USER_QUERY},
        ]

        logger.info("User: %s", USER_QUERY)
        logger.info("Sending request with %d tool definitions...", len(TOOLS))

        # ── Step 1: Send the request with tools ────────────────────────
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,  # Modern `tools` parameter (NOT deprecated `functions`)
        )

        choice = response.choices[0]
        assistant_message = choice.message

        # ── Step 2: Check for tool calls ───────────────────────────────
        if not assistant_message.tool_calls:
            logger.info("Model did not request any tools: %s", assistant_message.content)
            return

        logger.info("Model requested %d tool call(s)", len(assistant_message.tool_calls))

        # Append the assistant message (with tool_calls) to the conversation
        messages.append(assistant_message.model_dump())

        # ── Step 3: Execute each tool and return results ───────────────
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            logger.info(
                "[Tool Call] %s(%s)",
                function_name,
                ", ".join(f"{k}={v!r}" for k, v in arguments.items()),
            )

            # Execute the matching Python function
            if function_name in TOOL_FUNCTIONS:
                result = TOOL_FUNCTIONS[function_name](**arguments)
            else:
                result = {"error": f"Unknown tool: {function_name}"}

            result_str = json.dumps(result)
            logger.info("[Tool Result] %s → %s", function_name, result_str)

            # Append the tool result with the `tool` role (NOT deprecated `function` role)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result_str,
                }
            )

        # ── Step 4: Send tool results back for final response ──────────
        logger.info("Sending tool results back to model...")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
        )

        final_reply = response.choices[0].message.content
        logger.info("Assistant: %s", final_reply)

    log_stage("Takeaway")
    logger.info(
        "Tools are defined with openai.pydantic_function_tool() → "
        "model returns tool_calls → we execute locally → "
        "return results with 'tool' role → model composes final answer."
    )


if __name__ == "__main__":
    main()
