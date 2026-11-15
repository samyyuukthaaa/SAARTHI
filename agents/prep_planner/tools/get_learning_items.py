"""Tool: get_learning_items

Retrieves the curated free learning items that the student needs to complete.
Checks the Learning Curator's saved curriculum first; falls back to default placement lessons.
"""

import json
from pathlib import Path


def get_learning_items() -> dict:
    """Retrieve learning resources queued for the student's study plan.

    Returns:
        dict with list of learning item objects with duration and skill keys.
    """
    # 1. Try loading from Learning Curator saved output
    saved_items_path = Path(__file__).resolve().parent.parent.parent / "learning_curator" / "tools" / "data" / "learning_items.json"
    if saved_items_path.exists():
        try:
            items = json.loads(saved_items_path.read_text(encoding="utf-8"))
            if isinstance(items, list) and items:
                return {
                    "status": "success",
                    "source": "learning_curator_saved",
                    "items": items,
                    "count": len(items),
                }
        except Exception:
            pass

    # 2. Curated default items across core placement topics
    defaults = [
        {
            "id": "r1",
            "skill": "DSA",
            "skill_key": "dsa",
            "title": "Arrays and strings fundamentals",
            "provider": "NPTEL",
            "language": "English, Hindi subtitles",
            "format": "Lecture",
            "minutes": 45,
            "url": "https://swayam.gov.in/explorer?searchText=data%20structures",
            "is_free": True,
        },
        {
            "id": "r6",
            "skill": "OOP",
            "skill_key": "oop",
            "title": "Object-oriented programming in Java",
            "provider": "YouTube",
            "language": "Hindi",
            "format": "Video course",
            "minutes": 40,
            "url": "https://www.youtube.com/results?search_query=oops+in+java+hindi",
            "is_free": True,
        },
        {
            "id": "r14",
            "skill": "SQL",
            "skill_key": "sql",
            "title": "SQL queries and joins practice",
            "provider": "SQLBolt",
            "language": "English",
            "format": "Practice",
            "minutes": 35,
            "url": "https://sqlbolt.com/",
            "is_free": True,
        },
        {
            "id": "r39",
            "skill": "Communication",
            "skill_key": "communication",
            "title": "Structuring interview answers with STAR method",
            "provider": "YouTube",
            "language": "English",
            "format": "Video course",
            "minutes": 20,
            "url": "https://www.youtube.com/results?search_query=STAR+method+interview+answers",
            "is_free": True,
        },
    ]

    return {
        "status": "success",
        "source": "curated_defaults",
        "items": defaults,
        "count": len(defaults),
    }


if __name__ == "__main__":
    result = get_learning_items()
    print(json.dumps(result, indent=2))
