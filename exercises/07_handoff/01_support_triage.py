"""
Exercise 07 — Handoff Pattern: Support Triage

A triage agent analyzes customer queries and hands off to specialist agents
(billing, technical, account). Each specialist has focused capabilities.

Key concept: The triage agent produces a STRUCTURED handoff context (a
dataclass with customer query, category, and relevant info). The specialist
does NOT receive the triage agent's internal reasoning — only the structured
handoff object. This is option 2 from the plan (structured handoff).

Scenario: Customer support with dynamic routing to specialists.

How to run:
    python exercises/07_handoff/01_support_triage.py

Pattern: Handoff (dynamic routing)
"""

import json
import sys
import logging
from dataclasses import dataclass, asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import openai
from pydantic import BaseModel, Field

from exercises.commons.llm_client import get_client, get_model
from exercises.commons.agent import Agent, run
from exercises.commons.utils import setup_logging, log_stage, log_handoff, log_context_pass

import importlib
_tools = importlib.import_module("exercises.02_tool_use.tools")
lookup_order = _tools.lookup_order
process_refund = _tools.process_refund
search_faq = _tools.search_faq

logger = logging.getLogger(__name__)


# ── Handoff context ─────────────────────────────────────────────────────────
# This structured object is what gets passed from triage to specialist.
# The specialist does NOT see the triage agent's internal reasoning.


@dataclass
class HandoffContext:
    """Structured context passed from triage agent to specialist."""

    customer_query: str
    category: str  # "billing", "technical", or "account"
    priority: str  # "low", "medium", "high"
    extracted_info: dict  # Any relevant details (order IDs, error codes, etc.)


def _details_to_dict(details: list) -> dict:
    """Convert list of ExtractedDetail to a plain dict."""
    return {d.key: d.value for d in details}


# ── Triage output schema ───────────────────────────────────────────────────


class ExtractedDetail(BaseModel):
    """A single key-value detail extracted from the query."""

    key: str = Field(description="Detail name, e.g. 'order_id', 'error_code'")
    value: str = Field(description="Detail value")


class TriageDecision(BaseModel):
    """Structured output from the triage agent."""

    category: str = Field(description="Category: 'billing', 'technical', or 'account'")
    priority: str = Field(description="Priority: 'low', 'medium', or 'high'")
    reasoning: str = Field(description="Brief explanation of the routing decision")
    extracted_info: list[ExtractedDetail] = Field(
        default_factory=list,
        description="Any relevant details extracted from the query (order IDs, error codes, etc.)",
    )


# ── Agent definitions ───────────────────────────────────────────────────────

TRIAGE_PROMPT = (
    "You are a customer support triage agent. Analyze the customer's message and "
    "determine which specialist should handle it:\n"
    "- 'billing': Payment issues, invoices, refunds, pricing questions\n"
    "- 'technical': Product issues, bugs, errors, how-to questions\n"
    "- 'account': Account access, profile changes, password resets, account settings\n\n"
    "Extract any relevant details (order IDs, error codes, etc.) from the message."
)

BILLING_PROMPT = (
    "You are a billing specialist. You handle payment issues, invoices, refunds, "
    "and pricing questions. You have access to order lookup and refund processing tools. "
    "Be professional and resolve the issue efficiently. Address the specific details "
    "provided in the handoff context."
)

TECHNICAL_PROMPT = (
    "You are a technical support specialist. You handle product issues, bugs, errors, "
    "and how-to questions. You have access to the FAQ knowledge base. "
    "Provide clear technical guidance. Address the specific details "
    "provided in the handoff context."
)

ACCOUNT_PROMPT = (
    "You are an account management specialist. You handle account access issues, "
    "profile changes, password resets, and account settings. You have access to "
    "the FAQ knowledge base. Be helpful and security-conscious."
)


# ── Tool definitions for specialists ────────────────────────────────────────

class LookupOrderParams(BaseModel):
    order_id: str = Field(description="Order ID to look up")


class ProcessRefundParams(BaseModel):
    order_id: str = Field(description="Order ID to refund")
    reason: str = Field(description="Reason for the refund")


class SearchFaqParams(BaseModel):
    question: str = Field(description="Question to search in FAQ")


BILLING_TOOLS = [
    openai.pydantic_function_tool(LookupOrderParams, name="lookup_order", description="Look up order details"),
    openai.pydantic_function_tool(ProcessRefundParams, name="process_refund", description="Process a refund"),
]

TECHNICAL_TOOLS = [
    openai.pydantic_function_tool(SearchFaqParams, name="search_faq", description="Search FAQ knowledge base"),
]

ACCOUNT_TOOLS = [
    openai.pydantic_function_tool(SearchFaqParams, name="search_faq", description="Search FAQ knowledge base"),
]

# Specialist agent configurations
SPECIALISTS = {
    "billing": {
        "name": "Billing Specialist",
        "prompt": BILLING_PROMPT,
        "tools": BILLING_TOOLS,
        "tool_functions": {"lookup_order": lookup_order, "process_refund": process_refund},
    },
    "technical": {
        "name": "Technical Specialist",
        "prompt": TECHNICAL_PROMPT,
        "tools": TECHNICAL_TOOLS,
        "tool_functions": {"search_faq": search_faq},
    },
    "account": {
        "name": "Account Specialist",
        "prompt": ACCOUNT_PROMPT,
        "tools": ACCOUNT_TOOLS,
        "tool_functions": {"search_faq": search_faq},
    },
}

# ── Test queries ────────────────────────────────────────────────────────────

CUSTOMER_QUERIES = [
    "I was charged twice for order ORD-1001. I need a refund for the duplicate charge.",
    "I can't log in to my account. I've tried resetting my password but the reset email never arrives.",
    "My new headphones keep disconnecting from bluetooth. How do I fix this?",
]


def triage_query(client, model: str, query: str) -> HandoffContext:
    """Use the triage agent to classify a query and produce a structured handoff."""
    response = client.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": TRIAGE_PROMPT},
            {"role": "user", "content": query},
        ],
        response_format=TriageDecision,
    )

    decision = response.choices[0].message.parsed
    if decision is None:
        # Fallback if structured output fails
        return HandoffContext(
            customer_query=query,
            category="technical",
            priority="medium",
            extracted_info={},
        )

    logger.info("[Triage Agent] Category: %s | Priority: %s", decision.category, decision.priority)
    logger.info("[Triage Agent] Reasoning: %s", decision.reasoning)

    return HandoffContext(
        customer_query=query,
        category=decision.category,
        priority=decision.priority,
        extracted_info=_details_to_dict(decision.extracted_info),
    )


def route_to_specialist(
    client,
    model: str,
    handoff: HandoffContext,
) -> str:
    """Route to the appropriate specialist agent with the handoff context."""
    specialist_config = SPECIALISTS.get(handoff.category)
    if not specialist_config:
        return f"No specialist available for category: {handoff.category}"

    specialist = Agent(
        name=specialist_config["name"],
        system_prompt=specialist_config["prompt"],
        tools=specialist_config["tools"],
        tool_functions=specialist_config["tool_functions"],
        model=model,
    )

    # The specialist gets ONLY the structured handoff context — not the
    # triage agent's internal reasoning or the raw customer message.
    # This keeps the specialist focused on the relevant details.
    handoff_text = (
        f"Customer query: {handoff.customer_query}\n"
        f"Priority: {handoff.priority}\n"
        f"Extracted details: {json.dumps(handoff.extracted_info)}\n\n"
        "Please resolve this customer's issue."
    )

    messages: list[dict] = [
        {"role": "user", "content": handoff_text},
    ]

    return run(specialist, messages, client)


def main() -> None:
    setup_logging()

    log_stage("Handoff Pattern: Support Triage")

    model = get_model()

    with get_client() as client:
        for i, query in enumerate(CUSTOMER_QUERIES, 1):
            log_stage(f"Customer Query {i}/{len(CUSTOMER_QUERIES)}")
            logger.info("Customer: %s", query)

            # ── Step 1: Triage ──────────────────────────────────────────
            log_stage("Triage")
            handoff = triage_query(client, model, query)

            # ── Step 2: Handoff ─────────────────────────────────────────
            specialist_name = SPECIALISTS[handoff.category]["name"]
            log_handoff("Triage Agent", specialist_name, f"category={handoff.category}")
            log_context_pass(
                "Triage Agent",
                specialist_name,
                f"structured HandoffContext (query + category + priority + extracted_info)",
            )

            # ── Step 3: Specialist resolution ───────────────────────────
            resolution = route_to_specialist(client, model, handoff)
            logger.info("[%s] %s", specialist_name, resolution)

            # Alternative context passing strategies (for reference):
            #
            # OPTION 1 — Full history:
            #   Pass the triage agent's entire conversation to the specialist.
            #   Simple but noisy — specialist sees triage reasoning.
            #   specialist_messages = triage_messages.copy()
            #
            # OPTION 3 — Selective history:
            #   Filter to only user/assistant messages (strip tool calls).
            #   specialist_messages = [m for m in messages if m["role"] in ("user", "assistant")]

    log_stage("Takeaway")
    logger.info(
        "Handoff pattern: triage classifies → structured handoff object → specialist resolves. "
        "The specialist gets a clean HandoffContext, not the raw triage conversation. "
        "This keeps specialists focused and prevents context pollution."
    )


if __name__ == "__main__":
    main()
