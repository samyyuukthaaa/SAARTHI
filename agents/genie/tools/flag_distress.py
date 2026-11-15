"""Tool: flag_distress

Records that the user may need support and returns emergency mental health resources.
"""

import json
import sys
import time
from pathlib import Path


def flag_distress(message: str) -> dict:
    """Records that the user may need emotional or psychological support.

    Args:
        message: The statement or message expressed by the user indicating distress.

    Returns:
        dict containing recording confirmation, Tele-MANAS helpline details, and support protocol.
    """
    try:
        from agents.genie.data import TELE_MANAS
    except ImportError:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
        from agents.genie.data import TELE_MANAS

    msg = (message or "").strip()

    # Log to internal session audit without blocking user
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_message": msg,
        "action": "flagged_distress",
        "helpline_offered": TELE_MANAS.get("helpline", "14416"),
    }

    try:
        data_dir = Path(__file__).resolve().parent.parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        log_file = data_dir / "distress_flags.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass

    return {
        "status": "recorded",
        "flagged": True,
        "helpline": TELE_MANAS.get("helpline", "14416"),
        "helpline_name": TELE_MANAS.get("name", "Tele-MANAS"),
        "helpline_toll_free": True,
        "message": "User distress recorded. Respond warmly, suggest one slow breath, and share Tele-MANAS 14416.",
    }


if __name__ == "__main__":
    result = flag_distress("I feel like giving up")
    print(json.dumps(result, indent=2))
