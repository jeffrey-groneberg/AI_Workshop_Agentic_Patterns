"""
Exercise 05 — Concurrent Pattern: Stock Analysis

Fan-out/fan-in: Given a stock ticker, three analyst agents work in parallel
(fundamental, technical, sentiment). An aggregator synthesizes the results.

Key concept: Each analyst gets the SAME initial input independently — no
shared state between parallel agents. They don't know about each other.
The Aggregator then receives ALL outputs combined.

Scenario: Multi-perspective stock analysis with parallel execution.

How to run:
    python exercises/05_concurrent/01_stock_analysis.py

Pattern: Concurrent (fan-out/fan-in)
"""

import sys
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from exercises.commons.llm_client import get_client, get_model
from exercises.commons.agent import Agent, run
from exercises.commons.utils import setup_logging, log_stage, log_context_pass

logger = logging.getLogger(__name__)

# ── Analyst agent definitions ───────────────────────────────────────────────

FUNDAMENTAL_PROMPT = (
    "You are a fundamental analyst. Analyze the given stock from a fundamentals "
    "perspective: revenue trends, P/E ratio, competitive position, management quality, "
    "and growth prospects. Be concise (150-200 words). Output ONLY your analysis."
)

TECHNICAL_PROMPT = (
    "You are a technical analyst. Analyze the given stock from a technicals "
    "perspective: price trends, support/resistance levels, moving averages, "
    "volume patterns, and momentum indicators. Be concise (150-200 words). "
    "Output ONLY your analysis."
)

SENTIMENT_PROMPT = (
    "You are a market sentiment analyst. Analyze the given stock from a sentiment "
    "perspective: news coverage, social media buzz, analyst ratings, insider trading "
    "activity, and institutional ownership changes. Be concise (150-200 words). "
    "Output ONLY your analysis."
)

AGGREGATOR_PROMPT = (
    "You are a senior investment analyst. You have received three independent analyses "
    "of a stock: fundamental, technical, and sentiment. Synthesize these into a "
    "coherent investment summary with:\n"
    "1. Overall assessment (bullish/bearish/neutral)\n"
    "2. Key supporting points from each analysis\n"
    "3. Risks to watch\n"
    "4. Final recommendation\n"
    "Be balanced and reference specific points from each analyst."
)

STOCK_TICKER = "NVDA"
STOCK_NAME = "NVIDIA Corp."


def run_analyst(
    analyst_name: str,
    system_prompt: str,
    query: str,
    model: str,
) -> tuple[str, str]:
    """
    Run a single analyst agent and return (name, output).

    Each analyst gets its own client and fresh message list — no shared state.
    This function is designed to run in a thread pool.
    """
    from exercises.commons.llm_client import get_client

    agent = Agent(name=analyst_name, system_prompt=system_prompt, model=model)

    # Each analyst gets its own messages list — independent context
    messages: list[dict] = [
        {"role": "user", "content": query},
    ]

    with get_client() as client:
        output = run(agent, messages, client)

    return analyst_name, output


def main() -> None:
    setup_logging()

    log_stage("Concurrent Pattern: Stock Analysis")

    model = get_model()
    query = f"Analyze {STOCK_NAME} ({STOCK_TICKER}) stock."

    analysts = [
        ("Fundamental Analyst", FUNDAMENTAL_PROMPT),
        ("Technical Analyst", TECHNICAL_PROMPT),
        ("Sentiment Analyst", SENTIMENT_PROMPT),
    ]

    # ── Fan-out: Launch analysts in parallel ────────────────────────────
    log_stage("Fan-Out: Launching Parallel Analysts")
    logger.info(
        "[Concurrent] Launching %d analysts in parallel for %s...",
        len(analysts),
        STOCK_TICKER,
    )
    log_context_pass(
        "Orchestrator",
        "All Analysts",
        f"identical input query (no shared state between parallel agents)",
    )

    results: dict[str, str] = {}
    completed_count = 0

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(run_analyst, name, prompt, query, model): name
            for name, prompt in analysts
        }

        for future in as_completed(futures):
            name, output = future.result()
            results[name] = output
            completed_count += 1
            logger.info(
                "[Concurrent] %s complete (%d/%d)",
                name,
                completed_count,
                len(analysts),
            )

    # ── Fan-in: Aggregate results ───────────────────────────────────────
    log_stage("Fan-In: Aggregating Results")

    # Combine all analyst outputs into a single context for the aggregator
    combined_analyses = "\n\n".join(
        f"=== {name} ===\n{output}" for name, output in results.items()
    )

    log_context_pass(
        "All Analysts",
        "Aggregator",
        f"all {len(results)} analyst outputs combined ({len(combined_analyses)} chars)",
    )

    aggregator = Agent(name="Aggregator", system_prompt=AGGREGATOR_PROMPT, model=model)
    aggregator_messages: list[dict] = [
        {
            "role": "user",
            "content": (
                f"Synthesize these independent analyses of {STOCK_NAME} ({STOCK_TICKER}):\n\n"
                f"{combined_analyses}"
            ),
        },
    ]

    with get_client() as client:
        summary = run(aggregator, aggregator_messages, client)

    log_stage("Investment Summary")
    logger.info("\n%s", summary)

    log_stage("Takeaway")
    logger.info(
        "Concurrent pattern: each analyst gets the SAME input independently — "
        "no shared state between parallel agents. Results are combined only at "
        "the aggregation step. This gives diverse perspectives without cross-"
        "contamination and executes faster than sequential."
    )


if __name__ == "__main__":
    main()
