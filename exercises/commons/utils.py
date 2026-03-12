"""
Logging and utility helpers for the workshop exercises.

Provides structured, readable console output that narrates what's happening
in each exercise. The logging IS the learning experience — participants
understand agent behavior by reading the console output.
"""

import logging
import sys
from typing import Any


# ── ANSI color codes for terminal output ────────────────────────────────────

class _Colors:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


# ── Custom formatter ────────────────────────────────────────────────────────

class WorkshopFormatter(logging.Formatter):
    """Custom formatter that adds colors and a clean layout for workshop exercises."""

    LEVEL_COLORS = {
        logging.DEBUG: _Colors.DIM,
        logging.INFO: _Colors.RESET,
        logging.WARNING: _Colors.YELLOW,
        logging.ERROR: _Colors.RED,
        logging.CRITICAL: _Colors.RED + _Colors.BOLD,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.LEVEL_COLORS.get(record.levelno, _Colors.RESET)
        reset = _Colors.RESET

        # Timestamp + level + message
        timestamp = self.formatTime(record, "%H:%M:%S")
        level = record.levelname[0]  # Single char: I, D, W, E
        message = record.getMessage()

        return f"{_Colors.DIM}{timestamp}{reset} {color}{level} {message}{reset}"


# ── Setup function ──────────────────────────────────────────────────────────

def setup_logging(level: str | None = None) -> None:
    """
    Configure logging for workshop exercises.

    Sets up a single stream handler with the WorkshopFormatter.
    Call this once at the start of each exercise.

    Args:
        level: Log level string ("DEBUG", "INFO", etc.).
               Defaults to LOG_LEVEL env var, or "INFO".
    """
    import os

    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO").upper()

    root_logger = logging.getLogger()

    # Remove existing handlers to avoid duplicate output
    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(WorkshopFormatter())
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, level, logging.INFO))


# ── Logging helpers ─────────────────────────────────────────────────────────

def log_tool_call(
    agent_name: str,
    tool_name: str,
    arguments: dict[str, Any],
    result: Any,
) -> None:
    """Log a tool call with arguments and result."""
    logger = logging.getLogger(agent_name)
    args_str = ", ".join(f"{k}={v!r}" for k, v in arguments.items())
    result_str = str(result)
    if len(result_str) > 200:
        result_str = result_str[:200] + "..."
    logger.info("[%s] [Tool] %s(%s) → %s", agent_name, tool_name, args_str, result_str)


def log_handoff(
    from_agent: str,
    to_agent: str,
    reason: str,
) -> None:
    """Log a handoff between agents."""
    logger = logging.getLogger(from_agent)
    logger.info(
        "%s[Handoff]%s %s → %s (reason: %s)",
        _Colors.CYAN,
        _Colors.RESET,
        from_agent,
        to_agent,
        reason,
    )


def log_context_pass(
    from_agent: str,
    to_agent: str,
    context_description: str,
) -> None:
    """Log what context is being passed between agents."""
    logger = logging.getLogger(from_agent)
    logger.info(
        "%s[Context]%s Passing %s to %s",
        _Colors.MAGENTA,
        _Colors.RESET,
        context_description,
        to_agent,
    )


def log_loop_iteration(
    agent_name: str,
    iteration: int,
    description: str,
) -> None:
    """Log an agent loop iteration."""
    logger = logging.getLogger(agent_name)
    logger.info("[%s] [Loop %d] %s", agent_name, iteration, description)


def log_stage(stage_name: str) -> None:
    """Print a visual separator for a new pipeline stage or phase."""
    logger = logging.getLogger("workshop")
    separator = f"{'═' * 20} {stage_name} {'═' * 20}"
    logger.info(
        "\n%s%s%s%s",
        _Colors.BOLD,
        _Colors.CYAN,
        separator,
        _Colors.RESET,
    )


def log_message(agent_name: str, message: str) -> None:
    """Log a general message prefixed with the agent name."""
    logger = logging.getLogger(agent_name)
    logger.info("[%s] %s", agent_name, message)
