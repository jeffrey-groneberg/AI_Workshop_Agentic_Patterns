"""
Exercise 08 — Magentic Pattern: Incident Response

A Manager agent receives an incident description, builds a task ledger,
and coordinates specialist workers (Diagnostic, Infrastructure, Communication).
The Manager dynamically adapts the plan based on worker findings.

Key concept: The Manager maintains a TASK LEDGER (shared mutable state) that
acts as the coordination memory. Workers get only their TASK-SPECIFIC context —
not the full history and not other workers' outputs (unless the Manager decides
to share). The Manager synthesizes results back into the ledger.

Scenario: Responding to a production incident by coordinating specialists.

How to run:
    python exercises/08_magentic/01_incident_response.py

Pattern: Magentic (adaptive planning with task ledger)
"""

import json
import sys
import logging
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pydantic import BaseModel, Field as PydanticField

from exercises.commons.llm_client import get_client, get_model
from exercises.commons.utils import setup_logging, log_stage, log_context_pass

logger = logging.getLogger(__name__)


# ── Task Ledger ─────────────────────────────────────────────────────────────
# The shared mutable state that the Manager uses to coordinate work.


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    """A single task in the ledger."""

    id: int
    description: str
    assigned_to: str
    status: TaskStatus = TaskStatus.PENDING
    result: str = ""


@dataclass
class TaskLedger:
    """The Manager's coordination state — the central artifact of the Magentic pattern."""

    incident_description: str
    tasks: list[Task] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)
    next_task_id: int = 1

    def add_task(self, description: str, assigned_to: str) -> Task:
        task = Task(
            id=self.next_task_id,
            description=description,
            assigned_to=assigned_to,
        )
        self.tasks.append(task)
        self.next_task_id += 1
        logger.info(
            "[Task Ledger] Added task #%d: '%s' (assigned to: %s)",
            task.id,
            description,
            assigned_to,
        )
        return task

    def complete_task(self, task_id: int, result: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED
                task.result = result
                logger.info(
                    "[Task Ledger] Task #%d completed by %s",
                    task_id,
                    task.assigned_to,
                )
                return

    def add_finding(self, finding: str) -> None:
        self.findings.append(finding)
        logger.info("[Task Ledger] New finding: %s", finding)

    @property
    def pending_tasks(self) -> list[Task]:
        return [t for t in self.tasks if t.status == TaskStatus.PENDING]

    @property
    def completed_tasks(self) -> list[Task]:
        return [t for t in self.tasks if t.status == TaskStatus.COMPLETED]

    def summary(self) -> str:
        lines = [
            f"Incident: {self.incident_description}",
            f"Total tasks: {len(self.tasks)}",
            f"Completed: {len(self.completed_tasks)}",
            f"Pending: {len(self.pending_tasks)}",
            f"Findings: {len(self.findings)}",
        ]
        return "\n".join(lines)


# ── Plan schema (Manager's structured output) ──────────────────────────────


class PlannedTask(BaseModel):
    """A task the Manager wants to create."""

    description: str = PydanticField(description="What needs to be done")
    assigned_to: str = PydanticField(
        description="Worker to assign: 'Diagnostic Agent', 'Infrastructure Agent', or 'Communication Agent'"
    )


class IncidentPlan(BaseModel):
    """The Manager's initial plan for handling the incident."""

    assessment: str = PydanticField(description="Brief assessment of the incident severity and scope")
    tasks: list[PlannedTask] = PydanticField(description="List of tasks to execute")


class AdaptedPlan(BaseModel):
    """The Manager's adapted plan after reviewing worker findings."""

    analysis: str = PydanticField(description="Analysis of findings so far")
    new_tasks: list[PlannedTask] = PydanticField(
        default_factory=list,
        description="Additional tasks needed based on findings (empty if none needed)",
    )
    ready_for_report: bool = PydanticField(
        description="True if we have enough information to write the final incident report"
    )


# ── Agent prompts ───────────────────────────────────────────────────────────

MANAGER_PLAN_PROMPT = (
    "You are an Incident Manager. Given an incident description, create an action plan. "
    "You have three specialist workers available:\n"
    "- 'Diagnostic Agent': Investigates root causes, checks logs, analyzes errors\n"
    "- 'Infrastructure Agent': Checks system health, capacity, network, deployment status\n"
    "- 'Communication Agent': Drafts customer communications, status page updates, internal notices\n\n"
    "Create 3-5 initial tasks assigned to the appropriate workers."
)

MANAGER_ADAPT_PROMPT = (
    "You are an Incident Manager reviewing progress. Based on the findings from "
    "completed tasks, decide if you need additional tasks or if you have enough "
    "information to write the final report. Consider:\n"
    "- Are there unanswered questions from the diagnostics?\n"
    "- Does infrastructure need changes?\n"
    "- Is customer communication needed?\n"
    "Add new tasks only if genuinely needed."
)

DIAGNOSTIC_PROMPT = (
    "You are a Diagnostic Agent investigating a production incident. "
    "Given a specific diagnostic task, provide detailed technical findings. "
    "Include: what you checked, what you found, potential root causes. "
    "Be specific and concise (100-150 words). Output ONLY your findings."
)

INFRASTRUCTURE_PROMPT = (
    "You are an Infrastructure Agent checking system health during an incident. "
    "Given a specific infrastructure task, provide your assessment. "
    "Include: current system state, any anomalies, recommended actions. "
    "Be specific and concise (100-150 words). Output ONLY your findings."
)

COMMUNICATION_PROMPT = (
    "You are a Communication Agent drafting incident communications. "
    "Given a specific communication task, provide the draft. "
    "Be clear, professional, and appropriately transparent about the issue. "
    "Output ONLY the draft communication (100-150 words)."
)

WORKER_PROMPTS = {
    "Diagnostic Agent": DIAGNOSTIC_PROMPT,
    "Infrastructure Agent": INFRASTRUCTURE_PROMPT,
    "Communication Agent": COMMUNICATION_PROMPT,
}

FINAL_REPORT_PROMPT = (
    "You are an Incident Manager writing the final incident report. "
    "Based on all findings and completed tasks, write a structured report with:\n"
    "1. Incident Summary\n"
    "2. Root Cause\n"
    "3. Impact\n"
    "4. Resolution Steps Taken\n"
    "5. Prevention Recommendations\n"
    "Be concise but thorough."
)

# ── Incident scenario ──────────────────────────────────────────────────────

INCIDENT = (
    "CRITICAL: The checkout service is returning 500 errors for approximately 30% "
    "of payment processing requests. Started at 14:30 UTC. Customer complaints "
    "are increasing. The error rate spiked after the 14:00 deployment of v2.3.1. "
    "Database connection pool metrics show elevated wait times."
)


def run_worker(client, model: str, worker_name: str, task: Task) -> str:
    """Execute a single worker task and return findings."""
    prompt = WORKER_PROMPTS.get(worker_name, DIAGNOSTIC_PROMPT)

    # Workers get ONLY their task-specific context — not the full ledger,
    # not other workers' outputs. The Manager decides what they need to know.
    log_context_pass(
        "Manager",
        worker_name,
        "task-specific context only (not full ledger)",
    )

    messages: list[dict] = [
        {"role": "system", "content": prompt},
        {
            "role": "user",
            "content": (
                f"Incident context: {INCIDENT}\n\n"
                f"Your task: {task.description}"
            ),
        },
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
        max_tokens=300,
    )

    return response.choices[0].message.content or ""


def main() -> None:
    setup_logging()

    log_stage("Magentic Pattern: Incident Response")

    model = get_model()
    ledger = TaskLedger(incident_description=INCIDENT)

    logger.info("Incident: %s", INCIDENT)

    with get_client() as client:

        # ── Phase 1: Manager creates initial plan ───────────────────────
        log_stage("Phase 1: Initial Planning")

        response = client.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": MANAGER_PLAN_PROMPT},
                {"role": "user", "content": f"Incident:\n{INCIDENT}"},
            ],
            response_format=IncidentPlan,
        )

        plan = response.choices[0].message.parsed
        if not plan:
            logger.error("Manager failed to produce a plan")
            return

        logger.info("[Manager] Assessment: %s", plan.assessment)

        for planned_task in plan.tasks:
            ledger.add_task(planned_task.description, planned_task.assigned_to)

        # ── Phase 2: Execute tasks ──────────────────────────────────────
        log_stage("Phase 2: Executing Tasks")

        for task in ledger.tasks:
            task.status = TaskStatus.IN_PROGRESS
            logger.info(
                "[Manager] Dispatching task #%d to %s: '%s'",
                task.id,
                task.assigned_to,
                task.description,
            )

            result = run_worker(client, model, task.assigned_to, task)
            ledger.complete_task(task.id, result)
            ledger.add_finding(f"[{task.assigned_to}] {result[:200]}")

            logger.info("[%s] %s", task.assigned_to, result[:300])

        # ── Phase 3: Manager adapts plan ────────────────────────────────
        log_stage("Phase 3: Plan Adaptation")

        findings_summary = "\n\n".join(
            f"Task #{t.id} ({t.assigned_to}): {t.result}"
            for t in ledger.completed_tasks
        )

        logger.info("[Task Ledger] %s", ledger.summary())

        response = client.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": MANAGER_ADAPT_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Incident: {INCIDENT}\n\n"
                        f"Completed task findings:\n{findings_summary}\n\n"
                        "Do you need additional tasks, or are we ready for the final report?"
                    ),
                },
            ],
            response_format=AdaptedPlan,
        )

        adaptation = response.choices[0].message.parsed
        if adaptation:
            logger.info("[Manager] Analysis: %s", adaptation.analysis)

            if adaptation.new_tasks:
                log_stage("Phase 3b: Additional Tasks")
                for planned_task in adaptation.new_tasks:
                    task = ledger.add_task(planned_task.description, planned_task.assigned_to)
                    task.status = TaskStatus.IN_PROGRESS

                    result = run_worker(client, model, task.assigned_to, task)
                    ledger.complete_task(task.id, result)
                    ledger.add_finding(f"[{task.assigned_to}] {result[:200]}")

                    logger.info("[%s] %s", task.assigned_to, result[:300])

        # ── Phase 4: Final report ───────────────────────────────────────
        log_stage("Phase 4: Final Incident Report")

        all_findings = "\n\n".join(
            f"Task #{t.id} ({t.assigned_to}): {t.description}\nResult: {t.result}"
            for t in ledger.completed_tasks
        )

        report_messages: list[dict] = [
            {"role": "system", "content": FINAL_REPORT_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Incident: {INCIDENT}\n\n"
                    f"All findings:\n{all_findings}"
                ),
            },
        ]

        response = client.chat.completions.create(
            model=model,
            messages=report_messages,
            temperature=0.3,
        )

        report = response.choices[0].message.content
        logger.info("\n%s", report)

        # ── Summary ─────────────────────────────────────────────────────
        log_stage("Ledger Summary")
        logger.info("[Task Ledger] %s", ledger.summary())

    log_stage("Takeaway")
    logger.info(
        "Magentic pattern: the Manager maintains a TASK LEDGER as shared "
        "mutable state. Workers receive only task-specific context — not the "
        "full ledger. The Manager synthesizes results and can dynamically "
        "adapt the plan by adding new tasks. This enables adaptive, "
        "goal-directed multi-agent coordination."
    )


if __name__ == "__main__":
    main()
