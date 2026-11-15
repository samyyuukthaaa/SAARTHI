"""Saarathi Prep Planner Agent

Builds, personalizes, and optimizes day-by-day preparation plans
and generates placement readiness quizzes.

Tools:
- get_shortlist
- get_learning_items
- get_constraints
- create_todo_plan
- generate_quiz

Strict Policies:
- Build plans strictly within the student's daily time limit and application deadline.
- Ask before modifying an existing plan.
- Weave learning modules, mock interviews, job applications, and quizzes logically.
"""

import os
import sys
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools.get_shortlist import get_shortlist
from tools.get_learning_items import get_learning_items
from tools.get_constraints import get_constraints
from tools.create_todo_plan import create_todo_plan
from tools.generate_quiz import generate_quiz


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
You are Saarathi's Prep Planner agent.

Your mission is to turn career goals into realistic, achievable daily action plans for students preparing for tech placements and job interviews.

Follow this sequence:
1. Call get_shortlist to identify target job roles, hiring rounds, and deadlines.
2. Call get_learning_items to find the curated study topics the student needs.
3. Call get_constraints to check the student's daily time budget (e.g. 90 minutes).
4. If asked to create or change a plan:
   - Call create_todo_plan to generate the day-by-day schedule.
   - If create_todo_plan returns "requires_confirmation", warn the student that an active plan exists and ask for confirmation before replacing it.
5. If the student asks for practice or a quiz on a topic, call generate_quiz.

Rules:
- Strictly respect daily time budgets. Total task time per day must never exceed the student's limit.
- Prioritize application submission on Day 1 when an upcoming deadline exists.
- Alternate mock interview practice (STAR method, self-introduction, technical basics) across days.
- Never modify an existing plan without checking first.
- Present the schedule in an encouraging, clear daily breakdown.
"""


def main():
    if len(sys.argv) < 2:
        print('Usage: python agent.py "Build a 7-day prep plan for my target jobs"')
        return

    user_prompt = sys.argv[1]

    print("\nSaarathi Prep Planner Agent is starting...\n")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=SYSTEM_PROMPT + "\n\nSTUDENT REQUEST:\n" + user_prompt,
            config=types.GenerateContentConfig(
                tools=[
                    get_shortlist,
                    get_learning_items,
                    get_constraints,
                    create_todo_plan,
                    generate_quiz,
                ],
                temperature=0.2,
            ),
        )

        print("\nSAARATHI PREP PLANNER RESPONSE:\n")
        print(response.text or "No text response returned.")

    except Exception as error:
        print("\nAgent execution failed:")
        print(str(error))


if __name__ == "__main__":
    main()
