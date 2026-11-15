"""Tool: get_profile

Returns the signed-in student's saved profile including skills, projects,
education, interests, preferred languages and preferred city.

Uses a realistic demo profile for offline / smoke-test usage.
"""

import json
from pathlib import Path


def get_profile() -> dict:
    """Return the student's profile.

    Tries to read the profile saved by the Profile Agent first.
    Falls back to the demo profile from data.py.
    """

    # Try loading a saved profile from the Profile Agent's data dir
    saved = Path(__file__).resolve().parent.parent.parent / "profile" / "tools" / "data" / "profile.json"
    if saved.exists():
        try:
            profile = json.loads(saved.read_text(encoding="utf-8"))
            if isinstance(profile, dict) and profile.get("skills"):
                return {
                    "status": "success",
                    "source": "saved_profile",
                    "profile": profile,
                }
        except (json.JSONDecodeError, OSError):
            pass

    # Fall back to demo profile
    from agents.job_matcher.data import DEMO_PROFILE

    return {
        "status": "success",
        "source": "demo",
        "profile": DEMO_PROFILE,
    }


if __name__ == "__main__":
    result = get_profile()
    print(json.dumps(result, indent=2))
