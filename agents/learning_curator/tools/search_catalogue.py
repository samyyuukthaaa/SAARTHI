"""Tool: search_catalogue

Searches the verified, curated catalogue of free educational resources
for a given skill gap.

Rules enforced:
- Maximum 2 free resources per skill gap.
- All courses are verified free (NPTEL, freeCodeCamp, MDN, Khan Academy, Python docs, etc.).
- Never invent URLs or recommend paid courses.
"""

import json


def search_catalogue(
    skill_gap: str,
    languages_json: str = '["English", "Hindi"]',
    max_minutes: int = 90,
) -> dict:
    """Find the top 2 free curated resources for a skill gap.

    Args:
        skill_gap: Skill identifier key (e.g. 'oop', 'dsa', 'communication').
        languages_json: JSON array of preferred languages, e.g. '["English", "Hindi"]'.
        max_minutes: Daily study time limit in minutes (default 90).

    Returns:
        dict containing at most two verified free resources ranked for the user.
    """
    from agents.learning_curator.data import CATALOGUE, SKILL_DISPLAY

    try:
        langs = json.loads(languages_json) if isinstance(languages_json, str) else languages_json
        if not isinstance(langs, list):
            langs = ["English"]
    except Exception:
        langs = ["English"]

    skill_key = skill_gap.lower().strip()
    langs_lower = [l.lower() for l in langs]

    # Find matching resources in catalogue
    candidates = [c for c in CATALOGUE if c["skill"] == skill_key]
    if not candidates:
        return {
            "status": "not_found",
            "message": f"No catalogue resources found for '{skill_gap}'. Use search_youtube as fallback.",
            "resources": [],
            "count": 0,
        }

    def rank_score(item: dict) -> float:
        score = 0.0
        item_lang = item["language"].lower()

        # Language preference scoring
        if "hindi" in langs_lower and "hindi" in item_lang:
            score += 3.0
        if "english" in langs_lower and "english" in item_lang:
            score += 1.5

        # Format and level preferences
        if item.get("level") == "Beginner":
            score += 1.5
        if item.get("minutes", 60) <= max_minutes:
            score += 1.0

        return score

    ranked = sorted(candidates, key=rank_score, reverse=True)

    # Strictly enforce: AT MOST TWO resources per skill gap
    picked = ranked[:2]

    # Format output items clearly
    results = []
    for r in picked:
        results.append({
            "id": r["id"],
            "skill": SKILL_DISPLAY.get(r["skill"], r["skill"]),
            "skill_key": r["skill"],
            "title": r["title"],
            "provider": r["provider"],
            "language": r["language"],
            "format": r["format"],
            "minutes": r["minutes"],
            "level": r["level"],
            "url": r["url"],
            "is_free": True,
        })

    return {
        "status": "success",
        "skill_gap": skill_gap,
        "resources": results,
        "count": len(results),
        "note": "Maximum 2 free resources returned as per strict policy.",
    }


if __name__ == "__main__":
    result = search_catalogue("oop", '["Hindi", "English"]', 90)
    print(json.dumps(result, indent=2))
