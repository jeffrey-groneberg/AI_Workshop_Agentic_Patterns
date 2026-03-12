"""
Exercise 04 — Sequential Pattern: Content Pipeline

A 3-agent pipeline: Research Agent → Draft Writer Agent → Editor Agent.
Each agent's output becomes the next agent's input — fresh context per stage.

Key concept: Each agent gets a NEW messages list containing only the previous
agent's output. The Research Agent's internal tool calls and reasoning are NOT
passed to the Draft Writer — only the final research output.

Scenario: Given a topic, produce a polished article through progressive refinement.

How to run:
    python exercises/04_sequential/01_content_pipeline.py

Pattern: Sequential (pipeline)
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from exercises.commons.llm_client import get_client, get_model
from exercises.commons.agent import Agent, run
from exercises.commons.utils import setup_logging, log_stage, log_context_pass

logger = logging.getLogger(__name__)

# ── Agent definitions ───────────────────────────────────────────────────────

RESEARCH_AGENT_PROMPT = (
    "You are a research agent. Given a topic, produce comprehensive research notes "
    "covering key facts, statistics, different perspectives, and interesting angles. "
    "Structure your output as bullet points grouped by subtopic. "
    "Focus on accuracy and breadth. Output ONLY the research notes."
)

DRAFT_WRITER_PROMPT = (
    "You are a skilled draft writer. Given research notes, write a well-structured "
    "article of 300-400 words. Include an engaging introduction, clear sections with "
    "headers, and a conclusion. Write in a professional but accessible tone. "
    "Output ONLY the article draft."
)

EDITOR_PROMPT = (
    "You are a meticulous editor. Review the draft article and improve it: "
    "fix any factual issues, improve flow and readability, strengthen the "
    "introduction and conclusion, ensure consistent tone, and polish the prose. "
    "If the draft is poor quality, explain what's wrong and provide a rewritten version. "
    "Output the final polished article."
)

TOPIC = "The impact of remote work on urban planning and city design"


def main() -> None:
    setup_logging()

    log_stage("Sequential Pattern: Content Pipeline")

    model = get_model()

    # Define the three pipeline agents
    research_agent = Agent(name="Research Agent", system_prompt=RESEARCH_AGENT_PROMPT, model=model)
    draft_agent = Agent(name="Draft Writer", system_prompt=DRAFT_WRITER_PROMPT, model=model)
    editor_agent = Agent(name="Editor Agent", system_prompt=EDITOR_PROMPT, model=model)

    with get_client() as client:
        # ── Stage 1: Research ───────────────────────────────────────────
        log_stage("Stage 1/3: Research")

        research_messages: list[dict] = [
            {"role": "user", "content": f"Research the following topic thoroughly:\n\n{TOPIC}"},
        ]

        logger.info("[Research Agent] Researching topic: %s", TOPIC)
        research_output = run(research_agent, research_messages, client)
        logger.info("[Research Agent] Research complete (%d chars)", len(research_output))
        logger.debug("[Research Agent] Output:\n%s", research_output)

        # ── Stage 2: Draft Writing ─────────────────────────────────────
        log_stage("Stage 2/3: Draft Writing")

        # KEY: Fresh context! The Draft Writer only sees the research output,
        # NOT the Research Agent's internal conversation or system prompt.
        log_context_pass(
            "Research Agent",
            "Draft Writer",
            f"research output only ({len(research_output)} chars, fresh context)",
        )

        draft_messages: list[dict] = [
            {
                "role": "user",
                "content": (
                    "Write a polished article based on these research notes:\n\n"
                    f"{research_output}"
                ),
            },
        ]

        draft_output = run(draft_agent, draft_messages, client)
        logger.info("[Draft Writer] Draft complete (%d chars)", len(draft_output))
        logger.debug("[Draft Writer] Output:\n%s", draft_output)

        # ── Stage 3: Editing ───────────────────────────────────────────
        log_stage("Stage 3/3: Editing")

        log_context_pass(
            "Draft Writer",
            "Editor Agent",
            f"draft article only ({len(draft_output)} chars, fresh context)",
        )

        editor_messages: list[dict] = [
            {
                "role": "user",
                "content": (
                    "Review and polish this article draft:\n\n"
                    f"{draft_output}"
                ),
            },
        ]

        final_article = run(editor_agent, editor_messages, client)

        # ── Final output ───────────────────────────────────────────────
        log_stage("Final Article")
        logger.info("\n%s", final_article)

    log_stage("Takeaway")
    logger.info(
        "Sequential pattern: each agent gets a FRESH context with only the "
        "previous agent's output. The Research Agent's tool calls and internal "
        "reasoning never reach the Draft Writer. This keeps each stage focused "
        "and prevents context window bloat."
    )


if __name__ == "__main__":
    main()
