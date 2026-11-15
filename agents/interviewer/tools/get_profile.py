"""Tool: get_profile

Retrieves the candidate's profile (name, skills, projects, degree)
to personalize questions and interview dialogue.
"""

import json
from pathlib import Path


def get_profile() -> dict:
    """Retrieve the candidate's profile.

    Returns:
        dict containing candidate's name, degree, skills, projects, and preferred languages.
    """
    # 1. Try reading Profile Agent's saved data
    saved = Path(__file__).resolve().parent.parent.parent / "profile" / "tools" / "data" / "profile.json"
    if saved.exists():
        try:
            p = json.loads(saved.read_text(encoding="utf-8"))
            if isinstance(p, dict) and p.get("name"):
                return {
                    "status": "success",
                    "source": "saved_profile",
                    "profile": {
                        "name": p.get("name", "Rahul"),
                        "education": p.get("education", "B.Tech CSE"),
                        "skills": p.get("skills", ["Java", "Python", "SQL", "React"]),
                        "projects": p.get("projects", ["Weather App", "Student Management"]),
                        "preferred_languages": p.get("preferred_languages", ["English", "Hindi"]),
                    },
                }
        except Exception:
            pass

    # 2. Realistic demo profile fallback
    return {
        "status": "success",
        "source": "demo_profile",
        "profile": {
            "name": "Ananya",
            "education": "B.Tech CSE, 2026",
            "skills": ["Java", "SQL", "React", "Git", "DSA"],
            "projects": ["Campus Portal", "E-commerce Frontend"],
            "preferred_languages": ["English", "Hindi"],
        },
    }


if __name__ == "__main__":
    result = get_profile()
    print(json.dumps(result, indent=2))
