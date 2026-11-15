
import json
from pathlib import Path


def save_profile(profile_json: str) -> dict:

    try:
        profile = json.loads(profile_json)

        if not isinstance(profile, dict):
            raise ValueError("Profile must be a JSON object")

        required_fields = [
            "skills",
            "projects",
            "education",
            "interests",
            "preferred_languages"
        ]

        for field in required_fields:
            profile.setdefault(field, [] if field != "education" else "")

        # Save profile locally
        data_dir = Path(__file__).resolve().parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        profile_path = data_dir / "profile.json"

        profile_path.write_text(
            json.dumps(profile, indent=2),
            encoding="utf-8"
        )

        return {
            "status": "success",
            "message": "Student profile saved successfully",
            "profile": profile,
            "saved_to": str(profile_path)
        }

    except (json.JSONDecodeError, ValueError) as error:
        return {
            "status": "error",
            "message": str(error)
        }


if __name__ == "__main__":

    sample = {
        "skills": ["Python", "Java"],
        "projects": ["Weather App"],
        "education": "B.Tech CSE",
        "interests": ["Technology"],
        "preferred_languages": ["English", "Hindi"]
    }

    print(json.dumps(
        save_profile(json.dumps(sample)),
        indent=2
    ))
