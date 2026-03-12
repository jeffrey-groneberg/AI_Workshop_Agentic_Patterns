"""
Exercise 01.2 — System Prompts

Shows how system prompts shape agent behavior. The same user query is sent
to two different personas, demonstrating that the system prompt is the
foundation of agent identity.

Scenario: The same travel question answered by a formal advisor vs. a casual friend.

How to run:
    python exercises/01_llm_basics/02_system_prompts.py

Pattern: None (foundational)
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from exercises.commons.llm_client import get_client, get_model
from exercises.commons.utils import setup_logging, log_stage

logger = logging.getLogger(__name__)

# ── Personas ────────────────────────────────────────────────────────────────

FORMAL_ADVISOR_PROMPT = (
    "You are a professional travel consultant with 20 years of industry experience. "
    "You speak formally, use precise language, and provide well-structured recommendations "
    "with practical considerations (budget, visa requirements, health advisories). "
    "Address the user as 'Dear Traveler'."
)

CASUAL_FRIEND_PROMPT = (
    "You are a fun-loving travel buddy who has backpacked across 50+ countries. "
    "You speak casually, use informal language, throw in personal anecdotes, "
    "and focus on hidden gems and off-the-beaten-path experiences. "
    "Address the user as 'dude' or 'mate'."
)

USER_QUERY = "I'm thinking about visiting Portugal for the first time. Any advice?"

PERSONAS = [
    ("Formal Travel Advisor", FORMAL_ADVISOR_PROMPT),
    ("Casual Travel Buddy", CASUAL_FRIEND_PROMPT),
]


def main() -> None:
    setup_logging()

    log_stage("System Prompts: Same Query, Different Personas")

    model = get_model()

    with get_client() as client:
        for persona_name, system_prompt in PERSONAS:
            log_stage(f"Persona: {persona_name}")

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_QUERY},
            ]

            logger.info("System prompt: %s...", system_prompt[:80])
            logger.info("User: %s", USER_QUERY)

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.8,
                max_tokens=400,
            )

            reply = response.choices[0].message.content
            logger.info("[%s] %s", persona_name, reply)

    log_stage("Takeaway")
    logger.info(
        "Same query, same model, different system prompts → different behavior. "
        "The system prompt IS the agent's identity."
    )


if __name__ == "__main__":
    main()
