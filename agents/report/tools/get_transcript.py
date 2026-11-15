"""Tool: get_transcript

Returns the interview transcript with timestamps.
"""

import json
import sys
from pathlib import Path


def get_transcript(session_id: str = "demo") -> dict:
    """Returns the interview transcript with timestamps.

    Args:
        session_id: ID of the interview session (e.g. 'demo').

    Returns:
        dict containing interview turns with questions, answers, and timestamps.
    """
    try:
        from agents.report.data import DEMO_TRANSCRIPTS
    except ImportError:
        # Fallback when running tool directly or relative
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
        from agents.report.data import DEMO_TRANSCRIPTS

    key = (session_id or "demo").strip()
    data = DEMO_TRANSCRIPTS.get(key, DEMO_TRANSCRIPTS["demo"])

    return {
        "status": "success",
        "session_id": key,
        "round_type": data.get("round_type", "hr"),
        "candidate_name": data.get("candidate_name", "Candidate"),
        "total_turns": len(data.get("turns", [])),
        "transcript": data.get("turns", []),
    }


if __name__ == "__main__":
    result = get_transcript("demo")
    print(json.dumps(result, indent=2))
