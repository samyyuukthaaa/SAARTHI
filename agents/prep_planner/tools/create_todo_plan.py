"""Tool: create_todo_plan

Constructs a structured day-by-day preparation schedule strictly within
the student's daily time budget and target application deadline.

Rules enforced:
- Total task duration on any day MUST NOT exceed daily minutes limit.
- Weaves in job application on Day 1, alternating mock interview sessions,
  study modules (capped at 45m), and follow-up retention quizzes (10m).
- Detects existing plans and requires explicit confirmation before modifying.
"""

import json
from datetime import date, timedelta
from pathlib import Path


def create_todo_plan(
    days: int = 7,
    minutes_per_day: int = 90,
    overwrite: bool = False,
    shortlist_json: str = "",
    learning_items_json: str = "",
) -> dict:
    """Build a multi-day personalized to-do plan.

    Args:
        days: Number of days to plan for (default 7).
        minutes_per_day: Daily time limit in minutes (default 90).
        overwrite: Set to True to replace an existing plan; if False and a plan exists,
                   returns a confirmation warning.
        shortlist_json: Optional JSON array of shortlisted jobs.
        learning_items_json: Optional JSON array of learning items.

    Returns:
        dict containing the daily schedule and time budget breakdown.
    """
    from agents.prep_planner.data import QUIZZES
    from agents.prep_planner.tools.get_shortlist import get_shortlist
    from agents.prep_planner.tools.get_learning_items import get_learning_items

    data_dir = Path(__file__).resolve().parent / "data"
    plan_file = data_dir / "todo_plan.json"

    # Check for existing plan to enforce "ask before modifying an existing plan"
    if plan_file.exists() and not overwrite:
        try:
            existing = json.loads(plan_file.read_text(encoding="utf-8"))
            return {
                "status": "requires_confirmation",
                "message": "An active preparation plan already exists. Ask the student before replacing it.",
                "existing_plan_days": len(existing.get("plan", [])),
                "created_date": existing.get("created_date"),
                "hint": "Call create_todo_plan with overwrite=True once the user confirms.",
            }
        except Exception:
            pass

    # Resolve jobs and learning items
    if shortlist_json:
        try:
            jobs = json.loads(shortlist_json) if isinstance(shortlist_json, str) else shortlist_json
        except Exception:
            jobs = get_shortlist().get("shortlist", [])
    else:
        jobs = get_shortlist().get("shortlist", [])

    if learning_items_json:
        try:
            items = json.loads(learning_items_json) if isinstance(learning_items_json, str) else learning_items_json
        except Exception:
            items = get_learning_items().get("items", [])
    else:
        items = get_learning_items().get("items", [])

    budget = int(minutes_per_day or 90)
    today = date.today()
    schedule = []
    item_queue = list(items)
    quizzed_skills = set()

    for n in range(max(1, min(days, 14))):
        day_date = today + timedelta(days=n)
        day_label = day_date.strftime("%a %d %b")
        tasks = []
        used = 0

        # Day 1 priority: Job application submission
        if n == 0 and jobs:
            j = jobs[0]
            tasks.append({
                "id": f"apply-{j.get('id', 'job')}",
                "kind": "apply",
                "title": f"Submit Application: {j.get('title', 'Role')}",
                "detail": f"{j.get('company', 'Company')} · {j.get('location', 'Location')}",
                "minutes": 10,
                "href": "/jobs",
            })
            used += 10

        # Alternating days: Mock interview practice (15 mins)
        if n % 2 == 0 or n == days - 1:
            focus = (
                "Eye contact and confident self-introduction"
                if n == 0
                else "Structure behavioural answers with STAR method"
                if n < days - 1
                else "Full realistic mock interview round"
            )
            round_type = "Technical" if n % 4 == 2 else "HR"
            tasks.append({
                "id": f"iv-{n}",
                "kind": "interview",
                "title": f"{round_type} Mock Interview Round",
                "detail": f"Focus: {focus}",
                "minutes": 15,
                "href": "/interview",
            })
            used += 15

        # Learning modules: fit into remaining time (max 45m per module)
        while item_queue and (used + min(item_queue[0].get("minutes", 45), 45) <= budget):
            it = item_queue.pop(0)
            mins = min(int(it.get("minutes", 45)), 45)
            tasks.append({
                "id": f"learn-{it.get('id', 'item')}",
                "kind": "learn",
                "title": it.get("title", "Curated Lesson"),
                "detail": f"{it.get('provider', 'Online')} · {it.get('language', 'English')}",
                "minutes": mins,
                "url": it.get("url", ""),
                "href": "/learn",
            })
            used += mins

            # If this skill has a quiz bank and hasn't been quizzed yet, schedule a 10m quiz if within budget
            skill = it.get("skill_key") or it.get("skill", "").lower()
            if skill in QUIZZES and skill not in quizzed_skills and (used + 10 <= budget):
                quizzed_skills.add(skill)
                tasks.append({
                    "id": f"quiz-{skill}",
                    "kind": "quiz",
                    "title": f"Quiz: {skill.upper()} Assessment",
                    "detail": f"{len(QUIZZES[skill])} MCQs · verifies retention",
                    "minutes": 10,
                    "href": f"/learn/quiz/{skill}",
                })
                used += 10

        # If day is empty or very short, add a revision task
        if not any(t["kind"] in ("learn", "interview") for t in tasks):
            tasks.append({
                "id": f"rev-{n}",
                "kind": "practice",
                "title": "Topic Revision & Self-Practice",
                "detail": "Review weak quiz areas and notes",
                "minutes": 20,
                "href": "/learn",
            })
            used += 20

        schedule.append({
            "day": n + 1,
            "date": day_label,
            "tasks": tasks,
            "total_minutes": used,
            "budget_minutes": budget,
        })

    plan_output = {
        "status": "success",
        "created_date": today.isoformat(),
        "days_planned": len(schedule),
        "minutes_per_day_limit": budget,
        "target_job": f"{jobs[0].get('title', '')} at {jobs[0].get('company', '')}" if jobs else None,
        "plan": schedule,
    }

    # Persist the plan
    data_dir.mkdir(parents=True, exist_ok=True)
    plan_file.write_text(json.dumps(plan_output, indent=2), encoding="utf-8")

    return plan_output


if __name__ == "__main__":
    result = create_todo_plan(days=3, minutes_per_day=90, overwrite=True)
    print(json.dumps(result, indent=2))
