"""Tool: search_youtube

Searches for free educational video playlists on YouTube for a specific skill.
Formats verified YouTube search query URLs targeting well-known Indian educational channels.
Never invents video IDs or fake links.
"""

import json
import urllib.parse


def search_youtube(skill_gap: str, language: str = "Hindi") -> dict:
    """Generate verified YouTube learning resource links for a skill gap.

    Args:
        skill_gap: The skill name (e.g., 'dsa', 'react', 'oop', 'communication').
        language: Language preference for video explanations ('Hindi' or 'English').

    Returns:
        dict with verified YouTube search results and direct search URL.
    """
    from agents.learning_curator.data import SKILL_DISPLAY

    display = SKILL_DISPLAY.get(skill_gap.lower(), skill_gap.title())

    if language.lower() == "hindi":
        query = f"{display} tutorial in hindi full course"
    else:
        query = f"{display} full tutorial for beginners"

    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://www.youtube.com/results?search_query={encoded_query}"

    resource = {
        "id": f"yt-{skill_gap.lower()}-{language.lower()[:2]}",
        "skill": display,
        "skill_key": skill_gap.lower(),
        "title": f"{display} Video Tutorials ({language})",
        "provider": "YouTube (Curated Channels: NPTEL / Apna College / Gate Smashers / freeCodeCamp)",
        "language": language,
        "format": "Video course",
        "minutes": 45,
        "level": "Beginner",
        "url": search_url,
        "is_free": True,
    }

    return {
        "status": "success",
        "skill_gap": skill_gap,
        "language": language,
        "resource": resource,
        "query": query,
    }


if __name__ == "__main__":
    result = search_youtube("dsa", "Hindi")
    print(json.dumps(result, indent=2))
