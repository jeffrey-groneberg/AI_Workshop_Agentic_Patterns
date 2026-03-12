#!/usr/bin/env python3
"""Agentic AI Workshop — Interactive TUI Runner.

Launch with:  python workshop.py
"""

import subprocess
import sys
from pathlib import Path

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
    Markdown,
    Static,
)

ROOT = Path(__file__).resolve().parent
EXERCISES_DIR = ROOT / "exercises"

# ── Exercise catalogue ──────────────────────────────────────────────────────

CHAPTERS = [
    {
        "title": "0 — Setup",
        "exercises": [
            ("00_setup", "01_test_connection.py", "Connection Test"),
        ],
    },
    {
        "title": "1 — LLM Foundations",
        "exercises": [
            ("01_llm_basics", "01_chat_completion.py", "Chat Completion"),
            ("01_llm_basics", "02_system_prompts.py", "System Prompts"),
            ("01_llm_basics", "03_structured_outputs.py", "Structured Outputs"),
        ],
    },
    {
        "title": "2 — Tools & Function Calling",
        "exercises": [
            ("02_tool_use", "01_function_calling.py", "Function Calling"),
            ("02_tool_use", "02_tool_loop.py", "Tool Loop"),
        ],
    },
    {
        "title": "3 — Single Agent",
        "exercises": [
            ("03_single_agent", "01_customer_support_agent.py", "Customer Support Agent"),
        ],
    },
    {
        "title": "4 — Sequential Pattern",
        "exercises": [
            ("04_sequential", "01_content_pipeline.py", "Content Pipeline"),
        ],
    },
    {
        "title": "5 — Concurrent Pattern",
        "exercises": [
            ("05_concurrent", "01_stock_analysis.py", "Stock Analysis"),
        ],
    },
    {
        "title": "6 — Group Chat Pattern",
        "exercises": [
            ("06_group_chat", "01_brainstorm.py", "Brainstorm"),
            ("06_group_chat", "02_maker_checker.py", "Maker-Checker"),
        ],
    },
    {
        "title": "7 — Handoff Pattern",
        "exercises": [
            ("07_handoff", "01_support_triage.py", "Support Triage"),
        ],
    },
    {
        "title": "8 — Magentic Pattern",
        "exercises": [
            ("08_magentic", "01_incident_response.py", "Incident Response"),
        ],
    },
]


def _build_flat_list():
    """Return a flat list of (chapter_title, folder, file, label) tuples."""
    items = []
    for ch in CHAPTERS:
        for folder, file, label in ch["exercises"]:
            items.append((ch["title"], folder, file, label))
    return items


FLAT = _build_flat_list()


def _read_readme(folder: str) -> str:
    path = EXERCISES_DIR / folder / "README.md"
    if path.exists():
        return path.read_text()
    return f"*No README found for `{folder}`.*"


# ── Widgets ──────────────────────────────────────────────────────────────────


class ExerciseList(ListView):
    """Left-side list of exercises."""

    def compose(self) -> ComposeResult:
        current_chapter = None
        for i, (ch_title, folder, file, label) in enumerate(FLAT):
            if ch_title != current_chapter:
                current_chapter = ch_title
                yield ListItem(
                    Label(f"[bold cyan]▸ {ch_title}[/]", markup=True),
                    disabled=True,
                )
            yield ListItem(
                Label(f"  {label}", markup=True),
                id=f"ex-{i}",
            )


class StatusBadge(Static):
    """Shows run status for the selected exercise."""

    def __init__(self, **kwargs):
        super().__init__("", **kwargs)
        self._statuses: dict[int, str] = {}

    def set_status(self, idx: int, status: str):
        self._statuses[idx] = status

    def show_for(self, idx: int):
        status = self._statuses.get(idx)
        if status == "success":
            self.update("[bold green]✔ PASSED[/]")
        elif status == "failed":
            self.update("[bold red]✘ FAILED[/]")
        elif status == "running":
            self.update("[bold yellow]⏳ RUNNING…[/]")
        else:
            self.update("[dim]Not yet run[/]")


# ── App ──────────────────────────────────────────────────────────────────────


class WorkshopApp(App):
    """Agentic AI Workshop TUI."""

    CSS = """
    Screen {
        layout: horizontal;
    }
    #sidebar {
        width: 36;
        border-right: solid $primary;
        background: $surface;
    }
    #sidebar ExerciseList {
        height: 1fr;
    }
    #main {
        width: 1fr;
    }
    #detail {
        height: 1fr;
        padding: 1 2;
    }
    #bottom-bar {
        height: 3;
        padding: 0 2;
        background: $surface;
        border-top: solid $primary;
    }
    #status-badge {
        width: 1fr;
        content-align: right middle;
    }
    #run-hint {
        width: 1fr;
        content-align: left middle;
    }
    """

    TITLE = "🤖 Agentic AI Workshop"
    BINDINGS = [
        Binding("enter", "run_exercise", "Run Exercise", show=True),
        Binding("r", "run_exercise", "Run", show=False),
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(self):
        super().__init__()
        self._selected_idx: int | None = None
        self._running = False

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield ExerciseList()
            with Vertical(id="main"):
                with VerticalScroll(id="detail"):
                    yield Markdown("Select an exercise from the sidebar to begin.", id="readme")
                with Horizontal(id="bottom-bar"):
                    yield Static("[bold]Enter[/] to run", id="run-hint", markup=True)
                    yield StatusBadge(id="status-badge")
        yield Footer()

    def _get_exercise_index(self, item: ListItem) -> int | None:
        if item.id and item.id.startswith("ex-"):
            return int(item.id.split("-")[1])
        return None

    @on(ListView.Selected)
    def on_list_selected(self, event: ListView.Selected) -> None:
        idx = self._get_exercise_index(event.item)
        if idx is None:
            return
        self._selected_idx = idx
        ch_title, folder, file, label = FLAT[idx]
        readme_md = _read_readme(folder)
        self.query_one("#readme", Markdown).update(readme_md)
        self.query_one(StatusBadge).show_for(idx)

    @on(ListView.Highlighted)
    def on_list_highlighted(self, event: ListView.Highlighted) -> None:
        if event.item is None:
            return
        idx = self._get_exercise_index(event.item)
        if idx is None:
            return
        self._selected_idx = idx
        ch_title, folder, file, label = FLAT[idx]
        readme_md = _read_readme(folder)
        self.query_one("#readme", Markdown).update(readme_md)
        self.query_one(StatusBadge).show_for(idx)

    def action_run_exercise(self) -> None:
        if self._selected_idx is None or self._running:
            return
        self._run_exercise(self._selected_idx)

    @work(thread=True)
    def _run_exercise(self, idx: int) -> None:
        self._running = True
        _, folder, file, label = FLAT[idx]
        script = EXERCISES_DIR / folder / file
        badge = self.query_one(StatusBadge)

        self.call_from_thread(badge.set_status, idx, "running")
        self.call_from_thread(badge.show_for, idx)

        self.call_from_thread(
            self.query_one("#readme", Markdown).update,
            f"## ⏳ Running: {label}\n\n```\npython {script.relative_to(ROOT)}\n```\n\nCheck your terminal for output…",
        )

        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode == 0:
                self.call_from_thread(badge.set_status, idx, "success")
                output_md = (
                    f"## ✅ {label} — Passed\n\n"
                    f"```\n{result.stdout[-3000:] if result.stdout else '(no output)'}\n```"
                )
            else:
                self.call_from_thread(badge.set_status, idx, "failed")
                stderr = result.stderr[-2000:] if result.stderr else ""
                stdout = result.stdout[-1000:] if result.stdout else ""
                output_md = (
                    f"## ❌ {label} — Failed (exit code {result.returncode})\n\n"
                    f"**stderr:**\n```\n{stderr}\n```\n\n"
                    f"**stdout:**\n```\n{stdout}\n```"
                )
        except subprocess.TimeoutExpired:
            self.call_from_thread(badge.set_status, idx, "failed")
            output_md = f"## ⏰ {label} — Timed out after 120s"
        except Exception as e:
            self.call_from_thread(badge.set_status, idx, "failed")
            output_md = f"## 💥 {label} — Error\n\n```\n{e}\n```"

        self.call_from_thread(badge.show_for, idx)
        self.call_from_thread(self.query_one("#readme", Markdown).update, output_md)
        self._running = False


if __name__ == "__main__":
    WorkshopApp().run()
