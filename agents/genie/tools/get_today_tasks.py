"""Tool: get_today_tasks

Returns today's tasks from the plan.
"""

import json
import sys
from pathlib import Path


def get_today_tasks(language: str = "en") -> dict:
    """Returns today's tasks from the preparation plan.

    Args:
        language: Language code ('en' for English or 'hi' for Hindi). Defaults to 'en'.

    Returns:
        dict containing list of scheduled tasks with estimated minutes and completion state.
    """
    try:
        from agents.genie.data import TODAY_TASKS
    except ImportError:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
        from agents.genie.data import TODAY_TASKS

    lang = "hi" if language and "hi" in language.lower() else "en"
    tasks = TODAY_TASKS.get(lang, TODAY_TASKS["en"])

    return {
        "status": "success",
        "language": lang,
        "total_tasks": len(tasks),
        "total_minutes": sum(t["minutes"] for t in tasks),
        "tasks": tasks,
    }


if __name__ == "__main__":
    result = get_today_tasks()
    print(json.dumps(result, indent=2))
