"""Tool: get_shortlist

Retrieves the student's shortlisted job listings, including application deadlines,
required skills, and hiring rounds to anchor the preparation schedule.
"""

import json
from pathlib import Path


def get_shortlist(profile_json: str = "") -> dict:
    """Get the student's shortlisted jobs.

    Args:
        profile_json: Optional JSON string of the student profile.

    Returns:
        dict containing shortlisted jobs with skill requirements and deadlines.
    """
    from agents.prep_planner.data import DEMO_SHORTLIST

    shortlist = []

    # 1. Try provided profile_json
    if profile_json:
        try:
            p = json.loads(profile_json) if isinstance(profile_json, str) else profile_json
            if p.get("shortlist"):
                shortlist = p["shortlist"]
        except Exception:
            pass

    # 2. Try loading from saved profile
    if not shortlist:
        saved = Path(__file__).resolve().parent.parent.parent / "profile" / "tools" / "data" / "profile.json"
        if saved.exists():
            try:
                p = json.loads(saved.read_text(encoding="utf-8"))
                if p.get("shortlist"):
                    shortlist = p["shortlist"]
            except Exception:
                pass

    # 3. Fall back to realistic demo shortlist
    if not shortlist:
        shortlist = DEMO_SHORTLIST

    # Ensure each job has structured fields
    normalized = []
    for j in shortlist:
        if isinstance(j, str):
            # If it's just a job ID like "j1"
            normalized.append(DEMO_SHORTLIST[0])
        elif isinstance(j, dict):
            normalized.append({
                "id": j.get("id", "j1"),
                "title": j.get("title", "Associate Software Engineer"),
                "company": j.get("company", "Accenture"),
                "location": j.get("location", "Hyderabad"),
                "deadline_days": j.get("deadline_days", 7),
                "skills": j.get("skills", ["java", "sql", "dsa", "oop", "communication"]),
                "round": j.get("round", ["Online assessment", "Technical interview", "HR interview"]),
            })

    return {
        "status": "success",
        "shortlist": normalized,
        "count": len(normalized),
    }


if __name__ == "__main__":
    result = get_shortlist()
    print(json.dumps(result, indent=2))
