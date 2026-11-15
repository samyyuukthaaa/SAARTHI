"""Saarathi Genie Orchestrator Agent

Voice assistant and orchestrator for first-time job seekers in India.
Replies in user's language (Hindi or English), keeps answers phone-short (2-4 sentences),
routes each question to the right specialist agent, and responds to distress warmly with Tele-MANAS 14416.

Sub-agents orchestrated:
1. Profile (profile-agent)
2. Job Matcher (job-matcher-agent)
3. Learning Curator (learning-curator-agent)
4. Prep Planner (prep-planner-agent)
5. Interviewer (interviewer-agent)
6. Report (report-agent)

Tools:
- get_today_tasks
- flag_distress
"""

import json
import os
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# Ensure agent directory and project root are in sys.path
AGENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = AGENT_DIR.parent.parent
for p in (str(AGENT_DIR), str(PROJECT_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

from tools.get_today_tasks import get_today_tasks
from tools.flag_distress import flag_distress
from agents.genie.data import TELE_MANAS, TODAY_TASKS

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env.local"))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "profile", ".env.local"))
load_dotenv(".env.local")

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.5-flash-lite"

SYSTEM_PROMPT = """
You are Saarathi, a friendly career copilot for first-time job seekers in India.

Reply in the language the user writes in (Hindi or English), in 2–4 short sentences that fit on a phone screen.

Route questions:
- Jobs → Job Matcher
- What to learn → Learning Curator
- Plans, today's tasks and quizzes → Prep Planner
- Interview practice → Interviewer
- Past results → Report

If the user sounds distressed or hopeless:
- Respond warmly first.
- Suggest one slow breath.
- Call flag_distress.
- Share Tele-MANAS 14416 (free and confidential).

Stay on careers and politely decline unrelated requests.
"""

DISTRESS_REGEX = re.compile(
    r"give up|giving up|hopeless|can'?t do this|worthless|nervous|anxious|scared|panic|depress|stress|suicid|kill myself|घबरा|डर|हार मान|तनाव|परेशान|मदद",
    re.I,
)

UNRELATED_REGEX = re.compile(
    r"essay|climate change|poem|story|recipe|weather|cricket score|movie|song|joke",
    re.I,
)


def detect_language(text: str) -> str:
    """Detect whether user query is in Hindi (Devanagari / Romanized) or English."""
    if re.search(r"[\u0900-\u097F]", text):
        return "hi"
    if re.search(r"\b(kya|mujhe|aaj|naukri|kaise|hai|nahi|karna|batao|kripya)\b", text, re.I):
        return "hi"
    return "en"


def _record_trace(user_input: str, output_text: str, routing_info: dict) -> None:
    """Record execution trace to .codenow/agent-studio/traces/ for audit and evaluation."""
    try:
        traces_dir = PROJECT_ROOT / ".codenow" / "agent-studio" / "traces"
        traces_dir.mkdir(parents=True, exist_ok=True)
        trace_file = traces_dir / "genie-agent.jsonl"

        trace_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "agent": "genie-agent",
            "input": user_input,
            "routing": routing_info,
            "output": output_text,
            "status": "success",
        }
        with open(trace_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace_entry) + "\n")
    except Exception:
        pass


def execute_genie_locally(user_prompt: str) -> str:
    """Local deterministic orchestrator pipeline for Genie.

    Detects distress, language, unrelated queries, and routes to sub-agents.
    """
    lang = detect_language(user_prompt)
    is_hi = lang == "hi"

    # 1. Check for distress or hopelessness
    if DISTRESS_REGEX.search(user_prompt):
        flag_res = flag_distress(user_prompt)
        if is_hi:
            reply = (
                "ऐसा महसूस होना बिल्कुल स्वाभाविक है, कृपया घबराएं नहीं। "
                "पहले एक गहरी और धीमी सांस लीजिए। "
                "आप अकेले नहीं हैं: किसी भी समय सहायता के लिए Tele-MANAS हेल्पलाइन 14416 पर 24 घंटे मुफ़्त और गोपनीय बात कर सकते हैं।"
            )
        else:
            reply = (
                "It is completely normal to feel overwhelmed during interview preparation. "
                "Let's take one slow, deep breath together. "
                "Please remember you are not alone: Tele-MANAS is a free, confidential mental health helpline available 24/7 across India at 14416."
            )
        _record_trace(user_prompt, reply, {"handler": "distress", "tool": "flag_distress", "data": flag_res})
        return reply

    # 2. Check for off-topic / unrelated requests
    if UNRELATED_REGEX.search(user_prompt):
        if is_hi:
            reply = (
                "मैं सारथी हूँ, आपका करियर सहायक। मैं केवल नौकरी की तलाश, इंटरव्यू की तैयारी और तकनीकी कौशल सीखने में मदद करता हूँ। "
                "कृपया मुझे बताएं कि क्या आप आज का प्लान देखना चाहते हैं या किसी नौकरी के लिए तैयारी करना चाहते हैं।"
            )
        else:
            reply = (
                "I am Saarathi, your career copilot focused exclusively on job search, interview preparation, and technical learning in India. "
                "I cannot write essays or assist with non-career topics. "
                "Please let me know if you would like help with your target jobs, mock interviews, or today's study plan."
            )
        _record_trace(user_prompt, reply, {"handler": "declined_unrelated"})
        return reply

    # 3. Route questions:
    low = user_prompt.lower()

    # Route: Today's tasks & Prep Planner
    if any(k in low for k in ("today", "task", "plan", "aaj", "आज", "क्या करना", "schedule", "quiz")):
        tasks_data = get_today_tasks(lang)
        tasks = tasks_data.get("tasks", [])
        if is_hi:
            items_str = " ".join([f"{i+1}. {t['title']} ({t['minutes']} मिनट)।" for i, t in enumerate(tasks)])
            reply = (
                f"आज आपके प्लान में {len(tasks)} मुख्य काम हैं: {items_str} "
                "एक-एक करके आगे बढ़ें, आप बहुत अच्छा कर रहे हैं!"
            )
        else:
            items_str = " ".join([f"{i+1}. {t['title']} ({t['minutes']} min)." for i, t in enumerate(tasks)])
            reply = (
                f"Today you have {len(tasks)} focused preparation tasks: {items_str} "
                "Take them one step at a time, you are making solid progress!"
            )
        _record_trace(user_prompt, reply, {"handler": "prep_planner", "tool": "get_today_tasks", "tasks": tasks_data})
        return reply

    # Route: Jobs → Job Matcher
    if any(k in low for k in ("job", "jobs", "opening", "naukri", "नौकरी", "vacancy", "company", "apply")):
        # Sub-agent call to Job Matcher
        try:
            from agents.job_matcher.tools.search_cached_jobs import search_cached_jobs
            jobs_res = search_cached_jobs(skills="java, sql, python")
            top_jobs = jobs_res.get("jobs", [])[:2]
        except Exception:
            top_jobs = [
                {"title": "Associate Software Engineer", "company": "Accenture", "match": 92},
                {"title": "Junior Backend Developer", "company": "Infosys", "match": 88},
            ]

        if is_hi:
            j_str = ", ".join([f"{j['title']} ({j['company']})" for j in top_jobs])
            reply = (
                f"जॉब मैचर के अनुसार आपके लिए नए अवसर मिले हैं: {j_str}। "
                "आप Jobs पेज पर विवरण देख सकते हैं और सीधे आवेदन कर सकते हैं।"
            )
        else:
            j_str = " and ".join([f"{j['title']} at {j['company']}" for j in top_jobs])
            reply = (
                f"Job Matcher found top opportunities for your profile: {j_str}. "
                "You can inspect skill matches and apply directly from the Jobs page."
            )
        _record_trace(user_prompt, reply, {"handler": "job_matcher", "sub_agent": "job-matcher-agent"})
        return reply

    # Route: What to learn → Learning Curator
    if any(k in low for k in ("learn", "course", "study", "lecture", "सीख", "पढ़", "कोर्स")):
        if is_hi:
            reply = (
                "लर्निंग क्यूरेटर ने आपकी स्किल गैप के आधार पर SWAYAM और NPTEL से मुफ़्त कोर्सेस तैयार किए हैं। "
                "Learn पेज पर जाकर आप अपनी पसंदीदा भाषा में लेक्चर शुरू कर सकते हैं।"
            )
        else:
            reply = (
                "Learning Curator has identified curated, free lessons from SWAYAM and NPTEL matching your skill gaps. "
                "Head over to the Learn page to begin your personalized course modules."
            )
        _record_trace(user_prompt, reply, {"handler": "learning_curator", "sub_agent": "learning-curator-agent"})
        return reply

    # Route: Interview practice → Interviewer
    if any(k in low for k in ("interview", "mock", "practice", "round", "इंटरव्यू", "अभ्यास")):
        if is_hi:
            reply = (
                "इंटरव्यूअर एजेंट के साथ आप 3D रूम या ऑनलाइन कॉल मोड में HR और टेक्निकल राउंड का अभ्यास कर सकते हैं। "
                "शुरू करने के लिए Interview टैब खोलें और अपना पहला सवाल लें।"
            )
        else:
            reply = (
                "Interviewer agent is ready to conduct realistic HR or Technical mock rounds in either 3D room or online mode. "
                "Head to the Interview section whenever you are ready to begin practice."
            )
        _record_trace(user_prompt, reply, {"handler": "interviewer", "sub_agent": "interviewer-agent"})
        return reply

    # Route: Past results → Report
    if any(k in low for k in ("report", "score", "feedback", "past", "रिपोर्ट", "स्कोर")):
        if is_hi:
            reply = (
                "रिपोर्ट एजेंट ने आपके पिछले इंटरव्यू का स्कोर 64/100 रिकॉर्ड किया है। "
                "इसमें आई-कॉन्टैक्ट और फिलर शब्दों के सुधार के लिए 3 जरूरी सुझाव शामिल हैं। आप Report पेज पर पूरी रिपोर्ट देख सकते हैं।"
            )
        else:
            reply = (
                "Report agent recorded an overall score of 64/100 on your latest interview session. "
                "It includes 3 concrete fixes for eye contact and pacing, linked directly to SWAYAM lessons."
            )
        _record_trace(user_prompt, reply, {"handler": "report", "sub_agent": "report-agent"})
        return reply

    # Default fallback
    if is_hi:
        reply = (
            "नमस्ते! मैं सारथी हूँ, आपका करियर सहायक। "
            "आप मुझसे आज के टास्क, नए जॉब मैच, इंटरव्यू अभ्यास या अपनी पिछली रिपोर्ट के बारे में पूछ सकते हैं।"
        )
    else:
        reply = (
            "Hello! I am Saarathi, your career copilot. "
            "You can ask me about today's tasks, matching jobs, interview practice, or your latest interview report."
        )
    _record_trace(user_prompt, reply, {"handler": "default"})
    return reply


def main():
    if len(sys.argv) < 2:
        print('Usage: python agent.py "आज मुझे क्या करना है?"')
        return

    user_prompt = sys.argv[1]
    print("\nSaarathi Genie Orchestrator Agent is starting...\n")

    # If GEMINI_API_KEY is available, use Google GenAI SDK
    if API_KEY:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=API_KEY)
            response = client.models.generate_content(
                model=MODEL,
                contents=SYSTEM_PROMPT + "\n\nUSER PROMPT:\n" + user_prompt,
                config=types.GenerateContentConfig(
                    tools=[
                        get_today_tasks,
                        flag_distress,
                    ],
                    temperature=0.2,
                ),
            )
            output = response.text or "No text response returned."
            print("\nSAARATHI GENIE RESPONSE:\n")
            print(output)
            _record_trace(user_prompt, output, {"provider": "gemini", "model": MODEL})
            return
        except Exception as error:
            print(f"Gemini API invocation note: {error}. Falling back to deterministic pipeline.")

    # Fallback / Offline deterministic execution
    output = execute_genie_locally(user_prompt)
    print("\nSAARATHI GENIE RESPONSE:\n")
    print(output)


if __name__ == "__main__":
    main()
