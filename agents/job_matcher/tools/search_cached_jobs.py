"""Tool: search_cached_jobs

Searches the cached (seed) job listings by the student's skills and city.
Returns matching jobs sorted by relevance. Never invents job listings.
"""

import json


def search_cached_jobs(skills_json: str, city: str = "") -> dict:
    """Search cached job listings matching the given skills and optional city.

    Args:
        skills_json: JSON array of skill keys, e.g. '["java", "sql", "react"]'
        city: Preferred city name (optional). If empty, all locations match.

    Returns:
        dict with matched jobs list and count.
    """

    from agents.job_matcher.data import SEED_JOBS

    # Parse skills
    try:
        skills = json.loads(skills_json) if isinstance(skills_json, str) else skills_json
        if not isinstance(skills, list):
            skills = []
    except (json.JSONDecodeError, TypeError):
        skills = []

    skills_set = set(s.lower().strip() for s in skills if isinstance(s, str))
    city_lower = (city or "").strip().lower()

    if not skills_set:
        return {
            "status": "error",
            "message": "No skills provided. Pass a JSON array of skill keys.",
            "jobs": [],
            "count": 0,
        }

    # Score each job by overlap with student's skills + location match
    scored = []
    for job in SEED_JOBS:
        job_skills = set(job.get("skills", []))
        overlap = len(skills_set & job_skills)
        if overlap == 0:
            continue

        location_match = False
        loc = job.get("location", "").lower()
        if not city_lower:
            location_match = True
        elif city_lower in loc or "remote" in loc or "pan-india" in loc:
            location_match = True

        # Relevance score: skill overlap is primary, location is secondary
        score = overlap * 10 + (5 if location_match else 0) - job.get("posted_days_ago", 0) * 0.5
        scored.append((score, job))

    # Sort by score descending
    scored.sort(key=lambda x: -x[0])
    matched_jobs = [job for _, job in scored]

    return {
        "status": "success",
        "jobs": matched_jobs,
        "count": len(matched_jobs),
        "searched_skills": list(skills_set),
        "searched_city": city or "(any)",
    }


if __name__ == "__main__":
    # Test with demo skills
    result = search_cached_jobs('["java", "sql", "react", "git"]', "Hyderabad")
    print(json.dumps(result, indent=2))
    print(f"\nFound {result['count']} cached jobs.")
