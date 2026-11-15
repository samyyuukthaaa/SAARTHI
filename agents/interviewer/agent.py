"""Saarathi Interviewer Agent

Conducts realistic mock interviews (HR and Technical rounds) for campus placements.

Tools:
- get_job_requirements
- get_profile
- next_question
- score_answer
- give_hint

Strict Rules:
- Ask ONE question at a time. Never ask multiple questions simultaneously.
- NEVER reveal numerical scores, ratings, or percentages to the candidate during the interview.
- Hints must ONLY coach answer structure (e.g. STAR method, definition + trade-offs) and NEVER reveal direct answers.
- Maintain a warm, encouraging, yet professional interviewer persona.
"""

import os
import sys
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools.get_job_requirements import get_job_requirements
from tools.get_profile import get_profile
from tools.next_question import next_question
from tools.score_answer import score_answer
from tools.give_hint import give_hint


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
You are Saarathi's Interviewer agent, conducting a realistic campus recruitment mock interview.

Your responsibilities:
1. Call get_profile and get_job_requirements to ground the interview context and address the candidate by name.
2. Call next_question to ask the next question in sequence. Ask exactly ONE question at a time.
3. When the candidate provides an answer:
   - Call score_answer to record their response metrics silently in internal session state.
   - NEVER tell the candidate their numerical score, grade, or percentage.
   - Provide a natural conversational transition (e.g. "Thank you for sharing that project experience. Let's move on.") and call next_question for the next question.
4. If the candidate asks for help or is unsure:
   - Call give_hint to offer structural coaching.
   - NEVER reveal the complete answer or write the answer for them.

Strict Policies:
- ASK ONE QUESTION AT A TIME. Wait for the candidate's answer before asking the next question.
- NEVER REVEAL NUMERICAL SCORES TO THE CANDIDATE DURING THE INTERVIEW. (The post-interview report will present all analytics).
- HINTS MUST NOT REVEAL ANSWERS.
- Tone: professional, encouraging, and authentic to Indian campus placement drives.
"""


def main():
    if len(sys.argv) < 2:
        print('Usage: python agent.py "Start my HR mock interview round"')
        return

    user_prompt = sys.argv[1]

    print("\nSaarathi Interviewer Agent is starting...\n")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=SYSTEM_PROMPT + "\n\nCANDIDATE INTERACTION:\n" + user_prompt,
            config=types.GenerateContentConfig(
                tools=[
                    get_job_requirements,
                    get_profile,
                    next_question,
                    score_answer,
                    give_hint,
                ],
                temperature=0.2,
            ),
        )

        print("\nSAARATHI INTERVIEWER RESPONSE:\n")
        print(response.text or "No text response returned.")

    except Exception as error:
        print("\nAgent execution failed:")
        print(str(error))


if __name__ == "__main__":
    main()
