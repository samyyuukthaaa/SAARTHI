"""Tool: get_constraints

Retrieves the student's time constraints and preparation preferences:
- Daily study budget (e.g. 60 or 90 minutes/day)
- Application deadlines (days until submission)
- Pacing rules (maximum single module duration)
"""

import json
from pathlib import Path


def get_constraints(profile_json: str = "") -> dict:
    """Retrieve preparation constraints for the student.

    Args:
        profile_json: Optional JSON string of student profile.

    Returns:
        dict containing minutes_per_day, deadline_days, and scheduling constraints.
    """
    from agents.prep_planner.data import DEFAULT_CONSTRAINTS

    constraints = dict(DEFAULT_CONSTRAINTS)

    # 1. Try provided profile_json
    if profile_json:
        try:
            p = json.loads(profile_json) if isinstance(profile_json, str) else profile_json
            if p.get("minutes_per_day"):
                constraints["minutes_per_day"] = int(p["minutes_per_day"])
            elif p.get("minutesPerDay"):
                constraints["minutes_per_day"] = int(p["minutesPerDay"])
        except Exception:
            pass

    # 2. Try loading from saved profile
    saved = Path(__file__).resolve().parent.parent.parent / "profile" / "tools" / "data" / "profile.json"
    if saved.exists():
        try:
            p = json.loads(saved.read_text(encoding="utf-8"))
            if p.get("minutes_per_day"):
                constraints["minutes_per_day"] = int(p["minutes_per_day"])
            elif p.get("minutesPerDay"):
                constraints["minutes_per_day"] = int(p["minutesPerDay"])
        except Exception:
            pass

    return {
        "status": "success",
        "constraints": constraints,
    }


if __name__ == "__main__":
    result = get_constraints()
    print(json.dumps(result, indent=2))
