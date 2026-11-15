"""Tool: give_hint

Provides structural guidance and coaching for the current interview question.

STRICT RULE ENFORCED:
Hints must coach the structure of an answer (e.g. STAR method, definition + trade-offs)
and NEVER reveal the complete answer or code solution.
"""

import json


def give_hint(question_kind: str) -> dict:
    """Provide structured answer guidance without giving away the direct answer.

    Args:
        question_kind: Category of question ('intro', 'motivation', 'behavioural', 'concept', 'problem', 'close').

    Returns:
        dict containing coaching hint on how to structure the response.
    """
    from agents.interviewer.data import HINTS

    kind = (question_kind or "concept").lower().strip()
    hint_text = HINTS.get(kind, HINTS["concept"])

    return {
        "status": "success",
        "question_kind": kind,
        "hint": hint_text,
        "rule_verification": "Coaches answer structure only; does not disclose the answer or technical solution.",
    }


if __name__ == "__main__":
    result = give_hint("behavioural")
    print(json.dumps(result, indent=2))
