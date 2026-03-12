"""
Exercise 06.2 — Maker-Checker (Reflection / Evaluator-Optimizer)

A code generator agent writes code, a reviewer agent critiques it. The
generator revises based on feedback. Loop until approved or max iterations.

Key concept: Two agents ping-pong on the same conversation thread — a
simplified group chat. This is the reflection/evaluator-optimizer pattern.

Scenario: Generate a Python function, then iteratively improve it based
on code review feedback.

How to run:
    python exercises/06_group_chat/02_maker_checker.py

Pattern: Group Chat → Maker-Checker variant
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from exercises.commons.llm_client import get_client, get_model
from exercises.commons.utils import setup_logging, log_stage

logger = logging.getLogger(__name__)

# ── Agent prompts ───────────────────────────────────────────────────────────

GENERATOR_PROMPT = (
    "You are an expert Python developer. Write clean, well-documented Python code "
    "that follows best practices. When you receive feedback from a reviewer, "
    "carefully address each point and provide an improved version. "
    "Output ONLY the Python code (in a code block) — no extra commentary."
)

REVIEWER_PROMPT = (
    "You are a meticulous code reviewer. Review the provided Python code for:\n"
    "1. Correctness — does it handle edge cases?\n"
    "2. Readability — clear naming, good structure?\n"
    "3. Best practices — type hints, docstrings, error handling?\n"
    "4. Performance — any obvious inefficiencies?\n\n"
    "If the code is good enough, respond with exactly 'APPROVED' as the first word.\n"
    "If it needs improvement, provide specific, actionable feedback points.\n"
    "Be constructive but rigorous."
)

CODING_TASK = (
    "Write a Python function `merge_sorted_lists(list1: list[int], list2: list[int]) -> list[int]` "
    "that merges two already-sorted lists into a single sorted list. "
    "Do NOT use the built-in `sorted()` function — implement the merge algorithm manually. "
    "Include type hints, a docstring, and handle edge cases."
)

MAX_ITERATIONS = 4
APPROVAL_KEYWORD = "APPROVED"


def main() -> None:
    setup_logging()

    log_stage("Maker-Checker: Code Generation + Review")

    model = get_model()

    with get_client() as client:
        # ── Initial code generation ─────────────────────────────────────
        log_stage("Initial Generation")
        logger.info("Task: %s", CODING_TASK)

        # The shared conversation thread — both agents see the full history
        shared_messages: list[dict] = [
            {"role": "user", "content": CODING_TASK},
        ]

        # Generate initial code
        gen_messages = [
            {"role": "system", "content": GENERATOR_PROMPT},
            *shared_messages,
        ]

        response = client.chat.completions.create(
            model=model,
            messages=gen_messages,
            temperature=0.3,
        )

        code = response.choices[0].message.content
        shared_messages.append({"role": "assistant", "content": f"[Generator]: {code}"})
        logger.info("[Generator] Initial code produced")
        logger.debug("[Generator]\n%s", code)

        # ── Review-Revise loop ──────────────────────────────────────────
        for iteration in range(1, MAX_ITERATIONS + 1):
            log_stage(f"Review Iteration {iteration}/{MAX_ITERATIONS}")

            # ── Review step ─────────────────────────────────────────────
            review_messages = [
                {"role": "system", "content": REVIEWER_PROMPT},
                *shared_messages,
                {
                    "role": "user",
                    "content": "Review the code above. Reply APPROVED if it meets all criteria, or provide specific feedback.",
                },
            ]

            response = client.chat.completions.create(
                model=model,
                messages=review_messages,
                temperature=0.2,
            )

            review = response.choices[0].message.content
            shared_messages.append({"role": "assistant", "content": f"[Reviewer]: {review}"})

            # Check for approval
            if review.strip().upper().startswith(APPROVAL_KEYWORD):
                logger.info(
                    "[Maker-Checker] Iteration %d: Reviewer APPROVED the code!",
                    iteration,
                )
                break

            logger.info(
                "[Maker-Checker] Iteration %d: Reviewer rejected → sending feedback to Generator",
                iteration,
            )
            logger.info("[Reviewer] %s", review[:300])

            # ── Revise step ─────────────────────────────────────────────
            revise_messages = [
                {"role": "system", "content": GENERATOR_PROMPT},
                *shared_messages,
                {
                    "role": "user",
                    "content": "Address the reviewer's feedback and provide an improved version.",
                },
            ]

            response = client.chat.completions.create(
                model=model,
                messages=revise_messages,
                temperature=0.3,
            )

            revised_code = response.choices[0].message.content
            shared_messages.append(
                {"role": "assistant", "content": f"[Generator]: {revised_code}"}
            )
            logger.info("[Generator] Revised code (iteration %d)", iteration)
            logger.debug("[Generator]\n%s", revised_code)
        else:
            logger.warning(
                "[Maker-Checker] Reached max iterations (%d) without approval",
                MAX_ITERATIONS,
            )

        # ── Final output ────────────────────────────────────────────────
        log_stage("Final Code")
        # Find the last generator message
        for msg in reversed(shared_messages):
            if msg["content"].startswith("[Generator]:"):
                logger.info("\n%s", msg["content"].removeprefix("[Generator]: "))
                break

    log_stage("Takeaway")
    logger.info(
        "Maker-Checker pattern: two agents iterate on the same thread until "
        "quality criteria are met. The reviewer provides actionable feedback, "
        "the generator addresses it. This is the reflection/evaluator-optimizer "
        "pattern — a constrained group chat with exactly two participants."
    )


if __name__ == "__main__":
    main()
