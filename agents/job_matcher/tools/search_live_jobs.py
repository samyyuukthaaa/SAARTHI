"""Tool: search_live_jobs

Simulates a live job search when fewer than three cached jobs match.
In production this would call Adzuna / Remotive / Arbeitnow APIs.
For demo/offline mode, it returns additional seed jobs that weren't
in the cached results.

Never invents job listings — only returns entries from the seed data.
"""

import json


def search_live_jobs(skills_json: str, city: str = "", exclude_ids_json: str = "[]") -> dict:
    """Search for live job listings (simulated with seed data for demo).

    Args:
        skills_json: JSON array of skill keys, e.g. '["java", "sql"]'
        city: Preferred city (optional).
        exclude_ids_json: JSON array of job IDs already found in cached search,
                          to avoid duplicates.

    Returns:
        dict with additional jobs found.
    """

    from agents.job_matcher.data import SEED_JOBS

    # Parse inputs
    try:
        skills = json.loads(skills_json) if isinstance(skills_json, str) else skills_json
        if not isinstance(skills, list):
            skills = []
    except (json.JSONDecodeError, TypeError):
        skills = []

    try:
        exclude_ids = json.loads(exclude_ids_json) if isinstance(exclude_ids_json, str) else exclude_ids_json
        if not isinstance(exclude_ids, list):
            exclude_ids = []
    except (json.JSONDecodeError, TypeError):
        exclude_ids = []

    skills_set = set(s.lower().strip() for s in skills if isinstance(s, str))
    exclude_set = set(exclude_ids)
    city_lower = (city or "").strip().lower()

    if not skills_set:
        return {
            "status": "error",
            "message": "No skills provided.",
            "jobs": [],
            "count": 0,
        }

    # Find jobs not already returned by cached search, with at least
    # a weak skill overlap (even 1 matching skill counts for live search)
    results = []
    for job in SEED_JOBS:
        if job["id"] in exclude_set:
            continue

        job_skills = set(job.get("skills", []))
        overlap = len(skills_set & job_skills)
        if overlap == 0:
            continue

        # For live search, also consider broader location matching
        loc = job.get("location", "").lower()
        location_ok = (
            not city_lower
            or city_lower in loc
            or "remote" in loc
            or "pan-india" in loc
        )

        results.append({
            "job": job,
            "overlap": overlap,
            "location_ok": location_ok,
        })

    # Sort: location match first, then overlap
    results.sort(key=lambda r: (-int(r["location_ok"]), -r["overlap"]))
    jobs = [r["job"] for r in results]

    return {
        "status": "success",
        "source": "live_search_simulated",
        "jobs": jobs,
        "count": len(jobs),
        "note": "In production, this calls Adzuna, Remotive and Arbeitnow APIs.",
    }


if __name__ == "__main__":
    # Simulate: cached search found j1 and j2, now search live for more
    result = search_live_jobs(
        '["java", "sql", "javascript"]',
        "Hyderabad",
        '["j1", "j2"]'
    )
    print(json.dumps(result, indent=2))
    print(f"\nFound {result['count']} additional live jobs.")
