"""Tool: get_session_metrics

Returns eye contact, pace, filler words and posture scores.
"""

import json
import sys
from pathlib import Path


def get_session_metrics(session_id: str = "demo") -> dict:
    """Returns eye contact, pace, filler words and posture scores.

    Args:
        session_id: ID of the interview session (e.g. 'demo').

    Returns:
        dict containing scores and detailed metrics for eye contact, pace, posture, and filler words.
    """
    try:
        from agents.report.data import DEMO_METRICS
    except ImportError:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
        from agents.report.data import DEMO_METRICS

    key = (session_id or "demo").strip()
    data = DEMO_METRICS.get(key, DEMO_METRICS["demo"])

    return {
        "status": "success",
        "session_id": key,
        "overall": data.get("overall", 64),
        "scores": data.get("scores", {}),
        "metrics": data.get("metrics", {}),
        "gaze_distribution": data.get("gaze_distribution", {}),
        "moments": data.get("moments", []),
    }


if __name__ == "__main__":
    result = get_session_metrics("demo")
    print(json.dumps(result, indent=2))
