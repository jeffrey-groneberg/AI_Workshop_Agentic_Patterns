"""
Exercise 01.3 — Structured Outputs

Uses client.chat.completions.parse() with Pydantic models to get structured
JSON responses. This is the modern SDK pattern — NOT raw response_format.

Scenario: Extract structured entities from a product review (sentiment,
keywords, rating).

How to run:
    python exercises/01_llm_basics/03_structured_outputs.py

Pattern: None (foundational)
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pydantic import BaseModel
from exercises.commons.llm_client import get_client, get_model
from exercises.commons.utils import setup_logging, log_stage

logger = logging.getLogger(__name__)

# ── Pydantic model for structured output ────────────────────────────────────


class ReviewAnalysis(BaseModel):
    """Structured analysis of a product review."""

    sentiment: str  # "positive", "negative", or "mixed"
    rating: int  # 1-5 stars
    keywords: list[str]  # Key topics mentioned
    summary: str  # One-sentence summary
    recommended: bool  # Would the reviewer recommend this?


# ── Sample reviews ──────────────────────────────────────────────────────────

REVIEWS = [
    (
        "Just got back from using this travel backpack on a 3-week trip through Southeast Asia. "
        "The laptop compartment is perfectly padded, and the water bottle pockets actually hold "
        "a full Nalgene. My only gripe is the hip belt — it's too thin for heavy loads over 15kg. "
        "Still, for the price point, it's hard to beat. Would definitely buy again."
    ),
    (
        "Absolutely terrible experience. The zippers broke after two uses, the shoulder straps "
        "started fraying on day one, and the 'waterproof' claim is a complete lie — my clothes "
        "were soaked after light rain. Returned immediately. Save your money."
    ),
]

SYSTEM_PROMPT = (
    "You are a product review analyst. Extract structured information from "
    "product reviews. Be precise and objective in your analysis."
)


def main() -> None:
    setup_logging()

    log_stage("Structured Outputs with Pydantic")

    model = get_model()

    with get_client() as client:
        for i, review in enumerate(REVIEWS, 1):
            log_stage(f"Review {i}")
            logger.info("Review text: %s...", review[:100])

            # ── The modern pattern: client.chat.completions.parse() ─────
            #
            # Instead of manually specifying response_format={"type": "json_object"}
            # and hoping the model returns valid JSON, we use .parse() with a
            # Pydantic model. The SDK:
            #   1. Sends the JSON schema derived from the Pydantic model
            #   2. Constrains the model's output to match the schema (strict mode)
            #   3. Parses the response into a Pydantic instance automatically
            #
            # The result is in response.choices[0].message.parsed — a fully
            # validated Pydantic object, not a raw string.
            # ────────────────────────────────────────────────────────────

            response = client.chat.completions.parse(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Analyze this product review:\n\n{review}"},
                ],
                response_format=ReviewAnalysis,
            )

            analysis = response.choices[0].message.parsed
            if analysis is None:
                logger.warning("Model did not return structured output")
                continue

            logger.info("Sentiment:   %s", analysis.sentiment)
            logger.info("Rating:      %s/5", analysis.rating)
            logger.info("Keywords:    %s", ", ".join(analysis.keywords))
            logger.info("Summary:     %s", analysis.summary)
            logger.info("Recommended: %s", "Yes" if analysis.recommended else "No")

    log_stage("Takeaway")
    logger.info(
        "client.chat.completions.parse() + Pydantic = type-safe structured outputs. "
        "No manual JSON parsing needed."
    )


if __name__ == "__main__":
    main()
