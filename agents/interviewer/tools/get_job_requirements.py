"""Tool: get_job_requirements

Retrieves job requirements (role, company, tech stack, round type)
for the mock interview session.
"""

import json
from pathlib import Path


def get_job_requirements(job_id: str = "") -> dict:
    """Retrieve job requirements for the interview.

    Args:
        job_id: Optional ID of shortlisted job (e.g. 'j1').

    Returns:
        dict containing title, company, location, required skills, and rounds.
    """
    # 1. Try loading from saved shortlist / profile
    saved = Path(__file__).resolve().parent.parent.parent / "prep_planner" / "data" / "todo_plan.json"
    if saved.exists():
        try:
            plan = json.loads(saved.read_text(encoding="utf-8"))
            if plan.get("target_job"):
                parts = plan["target_job"].split(" at ")
                return {
                    "status": "success",
                    "job_id": job_id or "j1",
                    "title": parts[0].strip(),
                    "company": parts[1].strip() if len(parts) > 1 else "Accenture",
                    "skills": ["java", "sql", "dsa", "oop", "communication"],
                    "rounds": ["Technical Round", "HR Round"],
                }
        except Exception:
            pass

    # 2. Default target role
    return {
        "status": "success",
        "job_id": job_id or "j1",
        "title": "Associate Software Engineer",
        "company": "Accenture",
        "location": "Hyderabad",
        "skills": ["java", "sql", "dsa", "oop", "communication"],
        "rounds": ["Technical Round", "HR Round"],
        "experience_level": "Fresher",
    }


if __name__ == "__main__":
    result = get_job_requirements()
    print(json.dumps(result, indent=2))
