"""Tool: write_report

Saves the finished report.
"""

import json
import time
from pathlib import Path
from typing import Union


def write_report(report_json: Union[str, dict] = '{"overall":64}') -> dict:
    """Saves the finished report.

    Args:
        report_json: JSON string or dict containing the final structured report.

    Returns:
        dict with status, report_id, and confirmation details.
    """
    if isinstance(report_json, dict):
        report_data = report_json
    else:
        try:
            report_data = json.loads(report_json)
        except Exception:
            report_data = {"raw_content": str(report_json), "overall": 64}

    # Ensure output directory exists
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    report_file = data_dir / "saved_report.json"

    report_id = report_data.get("id") or f"rep-{int(time.time())}"
    report_data["id"] = report_id
    report_data["saved_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

    try:
        report_file.write_text(json.dumps(report_data, indent=2), encoding="utf-8")
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to write report: {str(e)}",
            "report_id": report_id,
        }

    return {
        "status": "success",
        "message": "Report saved successfully.",
        "report_id": report_id,
        "overall": report_data.get("overall", 64),
    }


if __name__ == "__main__":
    result = write_report('{"overall":64}')
    print(json.dumps(result, indent=2))
