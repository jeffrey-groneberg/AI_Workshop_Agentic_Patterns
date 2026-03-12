"""
Exercise 06.1 — Group Chat: Brainstorm

Three agents debate a product idea in a shared conversation thread. A chat
manager determines speaking order and termination.

Key concept: ALL agents share ONE conversation thread — every agent's response
is appended to the same `messages` list, so each agent sees everything that
was said before. This is the "shared memory" pattern.

Scenario: A product brainstorm session with a Product Manager, Designer, and Engineer.

How to run:
    python exercises/06_group_chat/01_brainstorm.py

Pattern: Group Chat (shared conversation)
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from exercises.commons.llm_client import get_client, get_model
from exercises.commons.utils import setup_logging, log_stage

logger = logging.getLogger(__name__)

# ── Agent personas ──────────────────────────────────────────────────────────

AGENTS = {
    "Product Manager": (
        "You are an experienced Product Manager in a brainstorm session. "
        "Focus on market fit, user needs, business viability, and competitive "
        "landscape. Challenge ideas constructively. Build on others' points. "
        "Keep contributions to 2-3 sentences."
    ),
    "Designer": (
        "You are a creative UX Designer in a brainstorm session. "
        "Focus on user experience, interface design, accessibility, and "
        "user delight. Propose concrete design ideas. React to and build on "
        "what others say. Keep contributions to 2-3 sentences."
    ),
    "Engineer": (
        "You are a pragmatic Senior Engineer in a brainstorm session. "
        "Focus on technical feasibility, architecture, scalability, and "
        "implementation complexity. Be honest about trade-offs. Build on "
        "others' points. Keep contributions to 2-3 sentences."
    ),
}

# Round-robin speaking order
SPEAKING_ORDER = ["Product Manager", "Designer", "Engineer"]
MAX_ROUNDS = 3
TOPIC = "A mobile app that helps people reduce food waste at home"


def main() -> None:
    setup_logging()

    log_stage("Group Chat: Product Brainstorm")

    model = get_model()
    total_turns = MAX_ROUNDS * len(SPEAKING_ORDER)

    # ── Shared conversation ─────────────────────────────────────────────
    # This single messages list is shared by all agents. Every agent sees
    # the full conversation history — this is the core of the group chat
    # pattern. The context window grows with every contribution.
    shared_messages: list[dict] = [
        {
            "role": "user",
            "content": (
                f"Brainstorm session topic: {TOPIC}\n\n"
                "Each participant should contribute their perspective, "
                "build on others' ideas, and help shape the concept. "
                "Be specific and constructive."
            ),
        },
    ]

    logger.info("Topic: %s", TOPIC)
    logger.info("Participants: %s", ", ".join(SPEAKING_ORDER))
    logger.info("Rounds: %d (%d total turns)", MAX_ROUNDS, total_turns)

    with get_client() as client:
        turn = 0

        for round_num in range(1, MAX_ROUNDS + 1):
            log_stage(f"Round {round_num}/{MAX_ROUNDS}")

            for agent_name in SPEAKING_ORDER:
                turn += 1

                # Temporarily swap the system prompt for the current speaker
                # Each agent uses the shared messages but with its own persona
                agent_messages = [
                    {"role": "system", "content": AGENTS[agent_name]},
                    *shared_messages,
                ]

                logger.info(
                    "[Group Chat] Turn %d/%d → %s speaking",
                    turn,
                    total_turns,
                    agent_name,
                )
                logger.info(
                    "[Context] Shared conversation: %d messages (all agents see full history)",
                    len(shared_messages),
                )

                response = client.chat.completions.create(
                    model=model,
                    messages=agent_messages,
                    temperature=0.8,
                    max_tokens=200,
                )

                reply = response.choices[0].message.content

                # Append to the SHARED conversation — all agents will see this
                shared_messages.append(
                    {
                        "role": "assistant",
                        "content": f"[{agent_name}]: {reply}",
                    }
                )

                logger.info("[%s] %s", agent_name, reply)

    # ── Summary ─────────────────────────────────────────────────────────
    log_stage("Brainstorm Summary")
    logger.info("Total turns: %d", turn)
    logger.info("Final shared conversation: %d messages", len(shared_messages))

    log_stage("Takeaway")
    logger.info(
        "Group Chat pattern: ALL agents share ONE conversation thread. "
        "Every agent sees everything — powerful for collaboration, but the "
        "context window fills fast. A chat manager controls who speaks and when "
        "to stop. Compare with handoff (routed) and sequential (staged)."
    )


if __name__ == "__main__":
    main()
