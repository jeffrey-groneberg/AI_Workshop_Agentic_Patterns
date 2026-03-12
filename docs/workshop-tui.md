# Workshop TUI

The workshop includes an interactive **Terminal User Interface (TUI)** that lets you browse, run, and inspect all exercises from a single window — no need to type commands manually.

## Launching the TUI

```bash
python workshop.py
```

This opens a full-screen terminal application:

```
┌──────────────────────┬───────────────────────────────────────────────┐
│ ▸ 0 — Setup          │                                               │
│   Connection Test     │  (exercise README / output shown here)        │
│ ▸ 1 — LLM Foundations│                                               │
│   Chat Completion     │                                               │
│   System Prompts      │                                               │
│   Structured Outputs  │                                               │
│ ▸ 2 — Tools & ...     │                                               │
│   ...                 │                                               │
├──────────────────────┼───────────────────────────────────────────────┤
│ Enter to run · F5 re-run                              ✔ PASSED       │
└──────────────────────┴───────────────────────────────────────────────┘
```

## How It Works

| Action | What Happens |
|--------|-------------|
| **Arrow keys** | Navigate the exercise list on the left — the README is shown on the right |
| **Enter** | Run the highlighted exercise |
| **F5** | Re-run the currently selected exercise |
| **q** | Quit the TUI |

When you run an exercise:

1. The TUI launches the exercise as a subprocess (`python exercises/...`)
2. The right panel shows **⏳ Running** while it executes
3. When it finishes, the full output is displayed in the right panel
4. A status badge shows **✔ PASSED** or **✘ FAILED**

## Why a TUI?

During workshops, participants often struggle with:

- Remembering which exercise to run next
- Typing long file paths correctly
- Losing track of which exercises they've already completed

The TUI solves all of these — it shows the full exercise catalog, runs them with one keypress, and tracks pass/fail status.

## Under the Hood

The TUI is built with [Textual](https://textual.textualize.io/), a modern Python TUI framework. Here's what `workshop.py` does:

- **Exercise catalog** — A list of all exercises organized by chapter, defined as a simple Python data structure at the top of the file
- **README display** — When you highlight an exercise, it reads and renders the corresponding `README.md` from the exercise folder
- **Subprocess execution** — Exercises run via `subprocess.run()` in a background thread so the UI stays responsive
- **Output capture** — stdout/stderr are captured and displayed as Markdown in the right panel
- **Status tracking** — Each exercise gets a pass/fail badge that persists while the TUI is open

!!! note "Not required"
    The TUI is a convenience tool. Every exercise can also be run directly from the terminal:
    ```bash
    python exercises/01_llm_basics/01_chat_completion.py
    ```
