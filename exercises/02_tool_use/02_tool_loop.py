"""
Exercise 02.2 — The Tool Loop (Agent Loop)

Implements the full agent loop: send messages → check for tool_calls →
execute tools → append results → re-send → repeat until the model produces
a final text response (finish_reason="stop").

This is the core loop that ALL later exercises build on.

Scenario: A multi-step research assistant that can search a database,
get stock prices, and do calculations.

How to run:
    python exercises/02_tool_use/02_tool_loop.py

Pattern: Agent loop (Reason → Act → Observe)
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
from exercises.02_tool_use.tools import search_database, get_stock_price, calculate

logger = logging.getLogger(__name__)

# ── Tool parameter schemas ──────────────────────────────────────────────────


class SearchDatabaseParams(BaseModel):
    """Parameters for searching the product database."""

    query: str = Field(description="Search query for product names")
    category: str = Field(
        default="all",
        description="Filter by category: 'electronics', 'sports', 'kitchen', or 'all'",
    )


class GetStockPriceParams(BaseModel):
    """Parameters for getting a stock price."""

    ticker: str = Field(description="Stock ticker symbol (e.g., 'AAPL', 'MSFT')")


class CalculateParams(BaseModel):
    """Parameters for evaluating a math expression."""

    expression: str = Field(description="Math expression to evaluate (e.g., '79.99 * 0.9')")


# ── Tool definitions and function map ───────────────────────────────────────

TOOLS = [
    openai.pydantic_function_tool(
        SearchDatabaseParams,
        name="search_database",
        description="Search the product database by name and optional category",
    ),
    openai.pydantic_function_tool(
        GetStockPriceParams,
        name="get_stock_price",
        description="Get the current stock price for a ticker symbol",
    ),
    openai.pydantic_function_tool(
        CalculateParams,
        name="calculate",
        description="Evaluate a math expression",
    ),
]

TOOL_FUNCTIONS = {
    "search_database": search_database,
    "get_stock_price": get_stock_price,
    "calculate": calculate,
}

MAX_ITERATIONS = 10

SYSTEM_PROMPT = (
    "You are a helpful research assistant with access to a product database, "
    "stock prices, and a calculator. Use your tools to answer the user's "
    "questions thoroughly. You may need multiple tool calls to fully answer."
)

USER_QUERY = (
    "I'm looking for electronics under $50 in the product database. "
    "Also, what's Apple's current stock price? "
    "If I bought 10 shares at the current price, what would that cost?"
)


def main() -> None:
    setup_logging()

    log_stage("The Agent Loop (Tool Loop)")

    model = get_model()
    logger.info("Using model: %s", model)

    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_QUERY},
    ]

    logger.info("User: %s", USER_QUERY)

    with get_client() as client:
        iteration = 0

        # ── The Agent Loop ──────────────────────────────────────────────
        # This is the core pattern:
        #   1. Send messages to model (with tools available)
        #   2. If model returns tool_calls → execute them, append results
        #   3. Re-send with updated messages
        #   4. Repeat until model produces text (no tool_calls)
        #
        # This loop is exactly what commons/agent.py encapsulates in the
        # `run()` function — here we show it explicitly.
        # ────────────────────────────────────────────────────────────────

        while iteration < MAX_ITERATIONS:
            iteration += 1
            logger.info("[Loop %d] Sending request to model...", iteration)

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=TOOLS,
            )

            choice = response.choices[0]
            assistant_message = choice.message

            # Append the assistant's message to the conversation
            messages.append(assistant_message.model_dump())

            # ── Check: Does the model want to call tools? ──────────────
            if not assistant_message.tool_calls:
                # No tool calls → the model is done reasoning
                logger.info(
                    "[Loop %d] Model produced final response (finish_reason=%s)",
                    iteration,
                    choice.finish_reason,
                )
                logger.info("Assistant: %s", assistant_message.content)
                break

            # ── Process each tool call ─────────────────────────────────
            logger.info(
                "[Loop %d] Model requested %d tool call(s)",
                iteration,
                len(assistant_message.tool_calls),
            )

            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                logger.info(
                    "[Loop %d] Tool call → %s(%s)",
                    iteration,
                    function_name,
                    ", ".join(f"{k}={v!r}" for k, v in arguments.items()),
                )

                # Execute the tool
                if function_name in TOOL_FUNCTIONS:
                    result = TOOL_FUNCTIONS[function_name](**arguments)
                else:
                    result = {"error": f"Unknown tool: {function_name}"}

                result_str = json.dumps(result)
                logger.info(
                    "[Loop %d] [Tool] %s → %s",
                    iteration,
                    function_name,
                    result_str[:200] + ("..." if len(result_str) > 200 else ""),
                )

                # Append tool result (role="tool", NOT deprecated role="function")
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result_str,
                    }
                )
        else:
            logger.warning(
                "Reached maximum iterations (%d) without a final response",
                MAX_ITERATIONS,
            )

    log_stage("Takeaway")
    logger.info(
        "The agent loop runs until the model stops requesting tools. "
        "Each iteration: model reasons → requests tool(s) → we execute → "
        "model observes results → decides what to do next. "
        "This Reason-Act-Observe cycle IS the agent."
    )


if __name__ == "__main__":
    main()
