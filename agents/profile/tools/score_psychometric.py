
import json


def score_psychometric(answers_json: str) -> dict:

    try:
        answers = json.loads(answers_json)

        if not isinstance(answers, (dict, list)):
            raise ValueError("Answers must be a JSON object or list")

    except (json.JSONDecodeError, ValueError):
        return {"error": "Invalid answers JSON"}

    numeric_scores = {}

    items = answers.items() if isinstance(answers, dict) else enumerate(answers)

    for key, value in items:

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if 1 <= value <= 5:
                numeric_scores[str(key)] = value

        elif isinstance(value, dict):
            score = value.get("score", value.get("answer"))

            if isinstance(score, (int, float)) and not isinstance(score, bool):
                if 1 <= score <= 5:
                    numeric_scores[str(key)] = score

    if not numeric_scores:
        return {
            "error": "No valid numerical answers found",
            "interests": [],
            "personality_traits": [],
            "scores": {}
        }

    average = sum(numeric_scores.values()) / len(numeric_scores)

    high_items = [
        key for key, value in numeric_scores.items()
        if value >= 4
    ]

    low_items = [
        key for key, value in numeric_scores.items()
        if value <= 2
    ]

    interests = []
    personality_traits = []

    values = answers.values() if isinstance(answers, dict) else answers

    for item in values:
        if isinstance(item, dict):
            category = item.get("category")
            label = item.get(
                "label",
                item.get("interest", item.get("trait"))
            )

            if label and category == "interest":
                interests.append(label)

            elif label and category == "personality":
                personality_traits.append(label)

    return {
        "scores": numeric_scores,
        "average_score": round(average, 2),
        "high_scoring_items": high_items,
        "low_scoring_items": low_items,
        "interests": interests,
        "personality_traits": personality_traits,
        "note": "Traits are not inferred from numerical answers alone."
    }


if __name__ == "__main__":

    sample = {
        "q1": 5,
        "q2": 4,
        "q3": 2,
        "q4": {
            "score": 5,
            "category": "interest",
            "label": "Technology"
        }
    }

    print(json.dumps(
        score_psychometric(json.dumps(sample)),
        indent=2
    ))
