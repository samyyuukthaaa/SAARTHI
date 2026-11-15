"""Tool: get_learning_items

Returns available lessons to link fixes to.
"""

import json
import sys
from pathlib import Path


def get_learning_items() -> dict:
    """Returns available lessons to link fixes to.

    Returns:
        dict containing list of curated, free learning resources.
    """
    try:
        from agents.report.data import LEARNING_ITEMS
    except ImportError:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
        from agents.report.data import LEARNING_ITEMS

    return {
        "status": "success",
        "total_lessons": len(LEARNING_ITEMS),
        "lessons": LEARNING_ITEMS,
    }


if __name__ == "__main__":
    result = get_learning_items()
    print(json.dumps(result, indent=2))
