"""Saarathi Learning Curator Agent

Recommends free lectures and practice courses for each skill gap,
matched to the student's language, level, and daily study time.

Tools:
- get_skill_gaps
- search_catalogue
- search_youtube
- save_learning_items

Strict Policies:
- Recommend at most TWO free resources per skill gap.
- Never invent links or recommend paid courses.
- Only free and verified resources.
"""

import os
import sys
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools.get_skill_gaps import get_skill_gaps
from tools.search_catalogue import search_catalogue
from tools.search_youtube import search_youtube
from tools.save_learning_items import save_learning_items


# Load Gemini API key from local or sibling agent env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env.local"))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "profile", ".env.local"))
load_dotenv(".env.local")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from .env.local")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.5-flash-lite"


SYSTEM_PROMPT = """
You are Saarathi's Learning Curator agent.

Your mission is to curate the best free learning resources for students and freshers to bridge their interview and placement skill gaps.

Follow this workflow:
1. Call get_skill_gaps to identify the student's missing skills or weak quiz areas.
2. For each identified skill gap:
   a. Call search_catalogue to find matching free lectures, practice platforms, or articles.
   b. If Hindi or video tutorials are preferred and not found, call search_youtube.
   c. Select AT MOST TWO free resources per skill gap.
3. Call save_learning_items to save the curated resources for the student's study plan.
4. Provide a supportive, concise summary of the curated roadmap with clickable links, estimated study time, and language.

Strict Rules:
- NEVER recommend paid courses or resources that require subscription fees.
- Recommend AT MOST TWO free resources per skill gap.
- NEVER invent course links or URLs. Only use URLs returned by the tools.
- Highlight why each resource was chosen (e.g., in Hindi, matches daily time, practical exercises).
"""


def main():
    if len(sys.argv) < 2:
        print('Usage: python agent.py "Curate free learning resources for my skill gaps"')
        return

    user_prompt = sys.argv[1]

    print("\nSaarathi Learning Curator Agent is starting...\n")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=SYSTEM_PROMPT + "\n\nSTUDENT REQUEST:\n" + user_prompt,
            config=types.GenerateContentConfig(
                tools=[
                    get_skill_gaps,
                    search_catalogue,
                    search_youtube,
                    save_learning_items,
                ],
                temperature=0.2,
            ),
        )

        print("\nSAARATHI LEARNING CURATOR RESPONSE:\n")
        print(response.text or "No text response returned.")

    except Exception as error:
        print("\nAgent execution failed:")
        print(str(error))


if __name__ == "__main__":
    main()
