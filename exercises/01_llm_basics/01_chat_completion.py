"""
Exercise 01.1 — Basic Chat Completion

Demonstrates the fundamentals of the Chat Completions API: the messages list,
roles (system, user, assistant), temperature, and max_tokens.

Scenario: A travel assistant that answers questions about destinations.

How to run:
    python exercises/01_llm_basics/01_chat_completion.py

Pattern: None (foundational)
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from exercises.commons.llm_client import get_client, get_model
from exercises.commons.utils import setup_logging, log_stage

logger = logging.getLogger(__name__)

# ── Constants ───────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a friendly and knowledgeable travel assistant. "
    "You help users plan trips by providing information about destinations, "
    "local customs, best times to visit, and practical travel tips. "
    "Keep your answers concise but informative."
)

QUESTIONS = [
    "What's the best time of year to visit Japan?",
    "Can you suggest a 3-day itinerary for Tokyo?",
]


def main() -> None:
    setup_logging()

    log_stage("Chat Completion Basics")

    model = get_model()
    logger.info("Using model: %s", model)

    with get_client() as client:
        # ── Single-turn conversation ────────────────────────────────────
        log_stage("Part 1: Single-Turn Request")

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": QUESTIONS[0]},
        ]

        logger.info("Sending single-turn request...")
        logger.debug("Messages: %s", messages)

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,  # Controls randomness: 0 = deterministic, 2 = very random
            max_tokens=300,   # Limits the response length
        )

        reply = response.choices[0].message.content
        logger.info("Assistant: %s", reply)
        logger.info(
            "Usage — prompt: %d tokens, completion: %d tokens, total: %d tokens",
            response.usage.prompt_tokens,
            response.usage.completion_tokens,
            response.usage.total_tokens,
        )

        # ── Multi-turn conversation ────────────────────────────────────
        log_stage("Part 2: Multi-Turn Conversation")

        # Build on the previous conversation by appending the assistant's
        # reply and a follow-up question. This is how conversation history
        # works — the full messages list is sent with each request.
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": QUESTIONS[1]})

        logger.info("Sending multi-turn request (conversation has %d messages)...", len(messages))
        logger.debug("Full conversation: %s", messages)

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )

        reply = response.choices[0].message.content
        logger.info("Assistant: %s", reply)
        logger.info(
            "Usage — prompt: %d tokens, completion: %d tokens, total: %d tokens",
            response.usage.prompt_tokens,
            response.usage.completion_tokens,
            response.usage.total_tokens,
        )


if __name__ == "__main__":
    main()
