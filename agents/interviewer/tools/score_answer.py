"""Tool: score_answer

Scores a candidate's answer across relevance, structure, word length, and filler words.

CRITICAL RULE ENFORCED:
Never reveal scores or numerical metrics to the candidate during the interview.
Scores are logged internally for the post-interview Report Agent.
"""

import json
import re
from pathlib import Path


def _count_fillers(text: str) -> int:
    from agents.interviewer.data import FILLERS
    t = f" {text.lower()} "
    return sum(len(re.findall(rf"\b{re.escape(f)}\b", t)) for f in FILLERS)


def score_answer(
    question_kind: str,
    answer_text: str,
    seconds_taken: float = 30.0,
    question_id: str = "",
) -> dict:
    """Evaluate and silently score candidate's response.

    Args:
        question_kind: Category of question ('intro', 'motivation', 'behavioural', 'concept', 'problem', 'close').
        answer_text: The transcript of what the candidate answered.
        seconds_taken: Duration spent answering in seconds.
        question_id: Optional ID of the question.

    Returns:
        dict containing score (0-100), words count, filler count, and silent logging.
    """
    from agents.interviewer.data import QUESTIONS

    text = (answer_text or "").strip()
    words = len(text.split())

    if not text:
        return {
            "status": "success",
            "score": 35,
            "words": 0,
            "fillers": 0,
            "wpm": 0,
            "has_result": False,
            "has_structure": False,
            "instruction": "DO_NOT_REVEAL_SCORE_TO_CANDIDATE. Acknowledge with: 'Thank you. Let's move on to the next question.'",
        }

    low = text.lower()

    # Find keywords for question kind
    kw = []
    for rnd in ("hr", "technical"):
        for q in QUESTIONS[rnd]:
            if q["kind"] == question_kind or q["id"] == question_id:
                kw = q.get("keywords", [])
                break

    relevance = min(1.0, sum(1 for k in kw if k in low) / max(2, len(kw) / 2)) if kw else 0.6
    length_factor = 1.0 if 40 <= words <= 220 else max(0.25, words / 40) if words < 40 else 0.75

    # Structure check (STAR / examples / causal reasoning)
    structure = 0.0
    if re.search(r"\b(because|for example|for instance|such as|so that|first|then)\b", low):
        structure += 0.5
    has_result = bool(re.search(r"\b(result|in the end|finally|achieved|improved|learned|\d+ ?%|\d+x)\b", low))
    if has_result:
        structure += 0.5

    fillers = _count_fillers(text)
    filler_rate = fillers / max(words, 1)

    raw_score = 100 * (0.30 * length_factor + 0.35 * relevance + 0.20 * structure + 0.15 * max(0.0, 1.0 - filler_rate * 10))
    final_score = int(max(15, min(96, round(raw_score))))
    wpm = round(words / (seconds_taken / 60)) if seconds_taken > 5 else None

    # Silently record score into session state
    data_dir = Path(__file__).resolve().parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    session_file = data_dir / "current_session_scores.json"

    scores_list = []
    if session_file.exists():
        try:
            scores_list = json.loads(session_file.read_text(encoding="utf-8"))
        except Exception:
            scores_list = []

    scores_list.append({
        "question_kind": question_kind,
        "question_id": question_id,
        "score": final_score,
        "words": words,
        "fillers": fillers,
        "seconds": seconds_taken,
        "wpm": wpm,
        "has_result": has_result,
    })
    session_file.write_text(json.dumps(scores_list, indent=2), encoding="utf-8")

    return {
        "status": "success",
        "score": final_score,
        "words": words,
        "fillers": fillers,
        "wpm": wpm,
        "has_result": has_result,
        "has_structure": structure >= 0.5,
        "warning": "DO_NOT_REVEAL_SCORE_TO_CANDIDATE: Keep numerical score strictly internal. Reply conversationally with an encouraging bridge before asking next_question.",
    }


if __name__ == "__main__":
    sample = "In my final year weather project, we encountered an API rate limit issue. For example, requests were failing during testing. I implemented client-side caching using Redis so that redundant calls were eliminated. In the end, response time improved by 40%."
    result = score_answer("behavioural", sample, 45.0, "hr-3")
    print(json.dumps(result, indent=2))
