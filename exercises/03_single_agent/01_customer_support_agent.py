"""
Exercise 03 — Single Agent with Multiple Tools

A complete customer support agent with tools for order lookup, FAQ search,
and refund processing. Demonstrates when a single agent is sufficient and
how context grows over a multi-turn conversation.

This uses the shared Agent abstraction from commons/agent.py.

Scenario: A customer support chatbot handling various request types.

How to run:
    python exercises/03_single_agent/01_customer_support_agent.py

Pattern: Single Agent
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import openai
from pydantic import BaseModel, Field

from exercises.commons.llm_client import get_client, get_model
from exercises.commons.agent import Agent, run
from exercises.commons.utils import setup_logging, log_stage
from exercises.02_tool_use.tools import lookup_order, search_faq, process_refund

logger = logging.getLogger(__name__)

# ── Tool parameter schemas ──────────────────────────────────────────────────


class LookupOrderParams(BaseModel):
    """Parameters for looking up an order."""

    order_id: str = Field(description="Order ID to look up (e.g., 'ORD-1001')")


class SearchFaqParams(BaseModel):
    """Parameters for searching the FAQ."""

    question: str = Field(description="The customer's question to search FAQs for")


class ProcessRefundParams(BaseModel):
    """Parameters for processing a refund."""

    order_id: str = Field(description="Order ID to refund")
    reason: str = Field(description="Reason for the refund")


# ── Agent setup ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a friendly customer support agent for an online store. "
    "You can look up orders, search the FAQ, and process refunds. "
    "Always greet the customer, identify their issue, use the appropriate "
    "tools to help, and provide a clear resolution. "
    "Be empathetic and professional."
)

TOOLS = [
    openai.pydantic_function_tool(
        LookupOrderParams,
        name="lookup_order",
        description="Look up order details by order ID",
    ),
    openai.pydantic_function_tool(
        SearchFaqParams,
        name="search_faq",
        description="Search the FAQ knowledge base for answers",
    ),
    openai.pydantic_function_tool(
        ProcessRefundParams,
        name="process_refund",
        description="Process a refund for an order (requires order ID and reason)",
    ),
]

TOOL_FUNCTIONS = {
    "lookup_order": lookup_order,
    "search_faq": search_faq,
    "process_refund": process_refund,
}

# Simulated multi-turn customer conversation
CUSTOMER_MESSAGES = [
    "Hi, I need help with my order ORD-1001. Can you tell me the status?",
    "I'm not happy with the headphones I received. What's your return policy?",
    "I'd like to return them and get a refund, please. The sound quality is poor.",
]


def main() -> None:
    setup_logging()

    log_stage("Single Agent: Customer Support")

    model = get_model()

    agent = Agent(
        name="Support Agent",
        system_prompt=SYSTEM_PROMPT,
        tools=TOOLS,
        tool_functions=TOOL_FUNCTIONS,
        model=model,
    )

    # The messages list persists across turns — this IS the agent's memory.
    # As the conversation grows, so does the context window usage.
    messages: list[dict] = []

    with get_client() as client:
        for turn, customer_msg in enumerate(CUSTOMER_MESSAGES, 1):
            log_stage(f"Turn {turn}")
            logger.info("Customer: %s", customer_msg)

            messages.append({"role": "user", "content": customer_msg})

            # The run() function handles the full agent loop internally
            response = run(agent, messages, client)

            logger.info("[Support Agent] %s", response)
            logger.info(
                "[Context] Conversation now has %d messages", len(messages)
            )

    log_stage("Takeaway")
    logger.info(
        "A single agent with multiple tools handles varied requests in one "
        "conversation. The messages list grows with each turn — this is the "
        "simplest form of agent memory. When tasks become too diverse or "
        "complex for one agent, it's time to consider orchestration patterns."
    )


if __name__ == "__main__":
    main()
