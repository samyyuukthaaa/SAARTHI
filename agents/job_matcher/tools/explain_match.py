"""Tool: explain_match

Explains why a specific job matches the student's profile.
Uses skill overlap, RIASEC interest alignment, location and recency
to produce a match score and human-readable reasons.

Adapted from backend/app/agents/job_matcher.py.
"""

import json


def _known_skills(profile: dict) -> set:
    """CV skills, minus ones the user failed a quiz on, plus ones they proved."""
    quiz = profile.get("quiz", {})
    have = {s for s in profile.get("skills", []) if quiz.get(s, 100) >= 50}
    return have | {s for s, v in quiz.items() if v >= 70}


def explain_match(profile_json: str, job_json: str) -> dict:
    """Explain why a job matches the student's profile.

    Args:
        profile_json: JSON string of the student profile.
        job_json: JSON string of the job listing.

    Returns:
        dict with match score (0-100), reasons list, and skill gaps.
    """

    from agents.job_matcher.data import SKILLS, RIASEC_SKILLS, INTEREST_TEXT

    try:
        profile = json.loads(profile_json) if isinstance(profile_json, str) else profile_json
        job = json.loads(job_json) if isinstance(job_json, str) else job_json
    except (json.JSONDecodeError, TypeError) as e:
        return {"status": "error", "message": f"Invalid JSON: {e}"}

    req = job.get("skills") or []
    have = _known_skills(profile)
    matched = [s for s in req if s in have]
    gaps = [s for s in req if s not in have]

    # RIASEC interest alignment
    top = profile.get("psych", {}).get("top", "I")
    interest_overlap = len(set(req) & RIASEC_SKILLS.get(top, set()))

    # Location match
    city = (profile.get("city") or "").lower()
    loc = job.get("location", "")
    local = (
        bool(city and city in loc.lower())
        or "remote" in loc.lower()
        or "pan-india" in loc.lower()
    )

    # Compute match score (25–97 range)
    overlap = len(matched) / len(req) if req else 0.3
    score = (
        38
        + 50 * overlap
        + 4 * min(interest_overlap, 2)
        + (4 if local else 0)
        - min(job.get("posted_days_ago", 0), 30) / 10
    )
    score = int(max(25, min(97, round(score))))

    # Build human-readable reasons (max 3)
    reasons = []
    if matched:
        names = [SKILLS.get(s, s) for s in matched[:2]]
        if len(names) > 1:
            reasons.append(f"{names[0]} and {names[1]} from your CV")
        else:
            reasons.append(f"{names[0]} from your CV")

    if job.get("level") == "intern":
        reasons.append("Internship, no experience needed")
    else:
        reasons.append("Open to freshers")

    if interest_overlap:
        reasons.append(INTEREST_TEXT.get(top, ""))

    if local:
        if "remote" in loc.lower():
            reasons.append("Remote role")
        else:
            reasons.append(f"In {loc.split('·')[0].strip()}")

    # Skill gap labels
    gap_labels = [SKILLS.get(g, g) for g in gaps]

    return {
        "status": "success",
        "match_score": score,
        "reasons": [r for r in reasons if r][:3],
        "matched_skills": [SKILLS.get(s, s) for s in matched],
        "skill_gaps": gap_labels,
        "gap_keys": gaps,
        "job_id": job.get("id"),
        "job_title": job.get("title"),
        "company": job.get("company"),
    }


if __name__ == "__main__":
    demo_profile = {
        "skills": ["java", "sql", "react", "git", "html_css", "javascript"],
        "city": "Hyderabad",
        "psych": {"top": "I"},
        "quiz": {"oop": 40},
    }
    demo_job = {
        "id": "j1",
        "title": "Associate Software Engineer",
        "company": "Accenture",
        "location": "Hyderabad",
        "skills": ["java", "sql", "dsa", "oop", "communication"],
        "level": "fresher",
        "posted_days_ago": 2,
    }
    result = explain_match(json.dumps(demo_profile), json.dumps(demo_job))
    print(json.dumps(result, indent=2))
