"""Tool: get_skill_gaps

Identifies and ranks the student's skill gaps by comparing their known skills
(CV skills minus failed quizzes) against their shortlisted/target jobs, plus quiz weaknesses.
Always prioritizes failed quiz topics and includes communication.
"""

import json
from pathlib import Path


def _load_profile(profile_json: str | None = None) -> dict:
    if profile_json:
        try:
            return json.loads(profile_json) if isinstance(profile_json, str) else profile_json
        except Exception:
            pass

    # Check for saved profile from Profile Agent
    saved = Path(__file__).resolve().parent.parent.parent / "profile" / "tools" / "data" / "profile.json"
    if saved.exists():
        try:
            return json.loads(saved.read_text(encoding="utf-8"))
        except Exception:
            pass

    from agents.learning_curator.data import DEMO_USER
    return DEMO_USER


def get_skill_gaps(profile_json: str = "") -> dict:
    """Identify and rank skill gaps for the student.

    Args:
        profile_json: Optional JSON string of the student profile.
                      If empty or invalid, uses the saved profile or demo data.

    Returns:
        dict with list of skill gap objects, each containing:
        - skill_key (e.g. 'dsa')
        - display_name (e.g. 'DSA: arrays and strings')
        - reason (e.g. 'Quiz score < 60%' or 'Required for Accenture')
        - priority ('high' or 'normal')
    """
    from agents.learning_curator.data import SKILLS, SKILL_DISPLAY, DEMO_USER

    user = _load_profile(profile_json)

    cv_skills = set(s.lower().strip() for s in user.get("skills", []))
    quiz = user.get("quiz", {})
    # CV skills where quiz >= 50, plus quiz skills >= 70
    known = {s for s in cv_skills if quiz.get(s, 100) >= 50} | {s for s, v in quiz.items() if v >= 70}

    gaps = []
    seen = set()

    # 1. Failed quiz topics (< 60) take top priority
    for s, v in sorted(quiz.items(), key=lambda kv: kv[1]):
        s_clean = s.lower().strip()
        if v < 60 and s_clean not in seen:
            seen.add(s_clean)
            gaps.append({
                "skill_key": s_clean,
                "display_name": SKILL_DISPLAY.get(s_clean, s_clean.upper()),
                "full_title": SKILLS.get(s_clean, s_clean),
                "reason": f"Quiz score was {v}%, need to revise fundamentals.",
                "priority": "high",
            })

    # 2. Check shortlisted jobs or default target jobs for required skills missing from known
    shortlist = user.get("shortlist", DEMO_USER.get("shortlist", []))
    for job in shortlist:
        job_title = job.get("title", "Target Role")
        company = job.get("company", "Target Company")
        req_skills = [s.lower().strip() for s in job.get("skills", [])]
        for s in req_skills:
            if s not in known and s not in seen:
                seen.add(s)
                gaps.append({
                    "skill_key": s,
                    "display_name": SKILL_DISPLAY.get(s, s.upper()),
                    "full_title": SKILLS.get(s, s),
                    "reason": f"Required for {job_title} at {company}.",
                    "priority": "normal",
                })

    # 3. Always ensure communication is included for interview readiness
    if "communication" not in seen:
        seen.add("communication")
        gaps.append({
            "skill_key": "communication",
            "display_name": "Communication",
            "full_title": SKILLS.get("communication", "Communication: self-introduction"),
            "reason": "Essential for interview round self-introduction and STAR storytelling.",
            "priority": "normal",
        })

    return {
        "status": "success",
        "gaps": gaps,
        "count": len(gaps),
    }


if __name__ == "__main__":
    result = get_skill_gaps()
    print(json.dumps(result, indent=2))
