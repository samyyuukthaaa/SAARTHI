"""Tool: next_question

Retrieves the next interview question in the sequence for either an HR or Technical round.
Strictly asks ONE question at a time.
"""

import json
from pathlib import Path


def next_question(
    round_type: str = "hr",
    question_index: int = 0,
    candidate_name: str = "Rahul",
    company_name: str = "Accenture",
) -> dict:
    """Get the next interview question in the sequence.

    Args:
        round_type: "hr" or "technical".
        question_index: Current 0-based question index (0, 1, 2, ...).
        candidate_name: Candidate's first name to personalize greetings.
        company_name: Company name for context.

    Returns:
        dict with question text, index, total questions, and round status.
    """
    from agents.interviewer.data import QUESTIONS

    rnd = round_type.lower().strip()
    bank = QUESTIONS.get(rnd, QUESTIONS["hr"])
    total = len(bank)

    if question_index >= total:
        return {
            "status": "completed",
            "is_done": True,
            "message": "Interview session complete. Thank you for your time! We will review your answers.",
            "question_index": question_index,
            "total_questions": total,
        }

    q_data = bank[question_index]
    formatted_q = q_data["q"].format(name=candidate_name or "there", company=company_name or "our company")

    return {
        "status": "in_progress",
        "is_done": False,
        "round_type": rnd,
        "question_index": question_index,
        "total_questions": total,
        "question_id": q_data["id"],
        "kind": q_data["kind"],
        "question": formatted_q,
        "guidance": "Ask this exact question and wait for the candidate to answer. Do not ask multiple questions at once.",
    }


if __name__ == "__main__":
    result = next_question("hr", 0, "Rahul", "Accenture")
    print(json.dumps(result, indent=2))
