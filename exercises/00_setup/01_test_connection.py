"""
Exercise 00 — Test Connection

Verifies that your environment is configured correctly and can communicate
with your chosen LLM provider (OpenAI, Azure OpenAI, or GitHub Models).

How to run:
    python exercises/00_setup/01_test_connection.py

Expected output:
    Provider info, model name, and a greeting from the model.
"""

import sys
import logging
from pathlib import Path

# Add project root to path so we can import shared modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from exercises.commons.llm_client import get_client, get_model, get_provider
from exercises.commons.utils import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()

    provider = get_provider()
    model = get_model()

    logger.info("Provider: %s", provider)
    logger.info("Model: %s", model)
    logger.info("Connecting...")

    # ── Context managers explained ──────────────────────────────────────
    #
    # The `with` statement below is a context manager. It ensures that the
    # OpenAI client's underlying HTTP connection pool is properly closed
    # when we're done, even if an exception occurs.
    #
    # Why this matters:
    #
    # - File descriptors: Every open network connection or file uses a
    #   "file descriptor" — a small integer the OS assigns to track it.
    #   Each process has a limited number (typically 256 on macOS, 1024 on
    #   Linux). If you don't close connections, you eventually run out and
    #   get "Too many open files" errors.
    #
    # - Sockets: Network connections use a specific type of file descriptor
    #   called a socket. The OpenAI SDK's httpx client maintains a pool of
    #   TCP sockets for performance (connection reuse / keep-alive).
    #   `with client:` ensures this pool is properly drained and closed.
    #
    # - The pattern: __enter__ sets up the resource, __exit__ tears it
    #   down — no matter what happens in between (even exceptions).
    #
    # In later exercises we use `with` without this explanation — but the
    # principle is the same: always clean up resources when you're done.
    # ────────────────────────────────────────────────────────────────────

    with get_client() as client:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello and confirm you are working. Keep it brief."},
            ],
            max_tokens=100,
        )

        reply = response.choices[0].message.content
        logger.info("Model response: %s", reply)
        logger.info("Connection test successful!")


if __name__ == "__main__":
    main()
