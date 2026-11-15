
import os
import sys
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools.parse_cv import parse_cv
from tools.score_psychometric import score_psychometric
from tools.save_profile import save_profile


# Load Gemini API key
load_dotenv(".env.local")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from .env.local")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.5-flash-lite"


SYSTEM_PROMPT = """
You are Saarathi's Profile Agent.

Your responsibility is to create a structured student profile.

Follow this workflow:

1. Read the student's CV text.
2. Call parse_cv to extract skills, projects and education.
3. If psychometric answers are provided, call
   score_psychometric to process them.
4. Combine the extracted information into a structured profile.
5. Call save_profile to save the final profile.

Rules:
- Never invent skills, projects or education.
- Only use information explicitly present in the CV.
- Do not infer personality traits from numerical scores alone.
- Do not invent missing information.
- Use empty lists or empty strings for unavailable fields.
- Save the profile only after gathering the available information.

The final profile must contain:
skills, projects, education, interests,
personality_traits and preferred_languages.
"""


def main():

    if len(sys.argv) < 2:
        print("Usage: python agent.py \"your CV and test answers\"")
        return

    user_prompt = sys.argv[1]

    print("\nSaarathi Profile Agent is starting...\n")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=SYSTEM_PROMPT + "\n\nSTUDENT DATA:\n" + user_prompt,
            config=types.GenerateContentConfig(
                tools=[
                    parse_cv,
                    score_psychometric,
                    save_profile
                ],
                temperature=0.2
            )
        )

        print("\nSAARATHI PROFILE AGENT RESPONSE:\n")
        print(response.text or "No text response returned.")

    except Exception as error:
        print("\nAgent execution failed:")
        print(str(error))


if __name__ == "__main__":
    main()
