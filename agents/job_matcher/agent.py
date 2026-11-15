"""Saarathi Job Matcher Agent

Finds and ranks suitable job opportunities for students and freshers.
Uses the Gemini API, following the same pattern as the Profile Agent.

Tools: get_profile, search_cached_jobs, search_live_jobs, explain_match
"""

import os
import sys
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools.get_profile import get_profile
from tools.search_cached_jobs import search_cached_jobs
from tools.search_live_jobs import search_live_jobs
from tools.explain_match import explain_match


# Load Gemini API key — check agent-local, then project root
load_dotenv(os.path.join(os.path.dirname(__file__), ".env.local"))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "profile", ".env.local"))
load_dotenv(".env.local")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from .env.local")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.5-flash-lite"


SYSTEM_PROMPT = """
You are Saarathi's Job Matcher agent.

Your task is to find and rank suitable job opportunities for students and freshers.

Follow this sequence:
1. Call get_profile to retrieve the student's skills, education, interests and preferred location.
2. Call search_cached_jobs using the student's skills and city.
3. If fewer than 3 suitable cached jobs are found, call search_live_jobs to find additional opportunities.
4. Rank up to 5 relevant jobs based on the student's profile.
5. Call explain_match for each selected job to explain why it fits the student.

Rules:
- Only mention jobs returned by the tools. Never invent job listings, companies, salaries or application links.
- If no suitable jobs are found, explain this honestly and suggest widening the city or job role.
- Keep explanations simple, concise and beginner-friendly.
- Present results as a numbered list with company, title, match score and top reasons.
"""


def main():

    if len(sys.argv) < 2:
        print('Usage: python agent.py "find jobs matching my profile"')
        return

    user_prompt = sys.argv[1]

    print("\nSaarathi Job Matcher Agent is starting...\n")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=SYSTEM_PROMPT + "\n\nSTUDENT REQUEST:\n" + user_prompt,
            config=types.GenerateContentConfig(
                tools=[
                    get_profile,
                    search_cached_jobs,
                    search_live_jobs,
                    explain_match,
                ],
                temperature=0.2,
            ),
        )

        print("\nSAARATHI JOB MATCHER RESPONSE:\n")
        print(response.text or "No text response returned.")

    except Exception as error:
        print("\nAgent execution failed:")
        print(str(error))


if __name__ == "__main__":
    main()
