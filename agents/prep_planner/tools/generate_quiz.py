"""Tool: generate_quiz

Generates a 5-question multiple choice quiz for a specific technical or placement topic
to test retention and benchmark student readiness.
"""

import json
import random


def generate_quiz(skill: str) -> dict:
    """Generate a 5-question MCQ quiz for a skill.

    Args:
        skill: Skill topic key (e.g. 'dsa', 'oop', 'sql', 'javascript', 'python', 'java', 'aptitude', 'communication').

    Returns:
        dict containing the quiz questions with options and answer keys.
    """
    from agents.prep_planner.data import QUIZZES

    skill_key = skill.lower().strip()
    bank = QUIZZES.get(skill_key)

    if not bank:
        # Generic fallback questions if skill is not in static bank
        bank = [
            {"q": f"What is the primary benefit of understanding {skill.title()}?", "options": ["Better problem solving", "Decreases hardware speed", "Obsoletes databases", "Prevents compilation"], "answer": 0},
            {"q": f"Which design principle is most critical when writing clean {skill.title()} code?", "options": ["Single responsibility", "Global state usage", "Hardcoding values", "Ignoring unit tests"], "answer": 0},
            {"q": f"In a placement interview, explaining your approach in {skill.title()} requires…", "options": ["Clear logic and trade-offs", "Memorizing without examples", "Avoiding time complexity discussion", "Speaking rapidly"], "answer": 0},
            {"q": f"How do you test your {skill.title()} implementation?", "options": ["Edge cases and boundary inputs", "Run once on happy path", "Skip testing", "Rely on user feedback in production"], "answer": 0},
        ]

    # Sample and format questions
    questions = []
    for idx, item in enumerate(bank[:5]):
        questions.append({
            "id": f"{skill_key}-{idx + 1}",
            "question": item["q"],
            "options": item["options"],
            "correct_answer_index": item["answer"],
        })

    return {
        "status": "success",
        "skill": skill,
        "question_count": len(questions),
        "questions": questions,
    }


if __name__ == "__main__":
    result = generate_quiz("dsa")
    print(json.dumps(result, indent=2))
