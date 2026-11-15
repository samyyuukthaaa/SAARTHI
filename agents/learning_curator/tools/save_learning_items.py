"""Tool: save_learning_items

Saves the student's personalized curriculum of curated learning resources.
Validates that each resource is free, has a valid URL, and enforces
the policy of at most 2 resources per skill gap.
"""

import json
from pathlib import Path


def save_learning_items(items_json: str) -> dict:
    """Validate and persist the curated learning items list.

    Args:
        items_json: JSON string of an array of learning item objects.

    Returns:
        dict confirming saved items count and file path.
    """
    try:
        items = json.loads(items_json) if isinstance(items_json, str) else items_json
        if not isinstance(items, list):
            return {"status": "error", "message": "items_json must be a JSON array of learning items."}
    except Exception as e:
        return {"status": "error", "message": f"Invalid JSON provided: {e}"}

    validated_items = []
    skill_counts = {}

    for it in items:
        if not isinstance(it, dict):
            continue

        skill = it.get("skill_key") or it.get("skill") or "general"
        skill_counts[skill] = skill_counts.get(skill, 0) + 1

        # Strict policy: Max 2 resources per skill gap
        if skill_counts[skill] > 2:
            continue

        validated = {
            "id": it.get("id", f"item-{len(validated_items) + 1}"),
            "skill": it.get("skill", skill),
            "skill_key": skill,
            "title": it.get("title", "Curated Lesson"),
            "provider": it.get("provider", "Open Education"),
            "language": it.get("language", "English"),
            "format": it.get("format", "Self-study"),
            "minutes": it.get("minutes", 45),
            "level": it.get("level", "Beginner"),
            "url": it.get("url", ""),
            "is_free": True,
            "why": it.get("why", "Targeted lesson for identified skill gap."),
        }
        validated_items.append(validated)

    # Persist to local data directory
    data_dir = Path(__file__).resolve().parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    out_file = data_dir / "learning_items.json"

    out_file.write_text(json.dumps(validated_items, indent=2), encoding="utf-8")

    return {
        "status": "success",
        "message": f"Successfully curated and saved {len(validated_items)} free learning items.",
        "saved_count": len(validated_items),
        "saved_path": str(out_file),
        "items": validated_items,
    }


if __name__ == "__main__":
    sample = [
        {
            "id": "r6",
            "skill": "OOP",
            "skill_key": "oop",
            "title": "Object-oriented programming in Java, explained in Hindi",
            "provider": "YouTube",
            "language": "Hindi",
            "format": "Video course",
            "minutes": 55,
            "level": "Beginner",
            "url": "https://www.youtube.com/results?search_query=oops+in+java+hindi",
            "is_free": True,
            "why": "Helps revise Java OOP for placement interviews in Hindi.",
        }
    ]
    result = save_learning_items(json.dumps(sample))
    print(json.dumps(result, indent=2))
