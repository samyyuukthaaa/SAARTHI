"""Realistic demo data and routing metadata for Saarathi Genie Orchestrator Agent.

Connects the 6 specialized sub-agents and provides today's preparation tasks,
bilingual support (Hindi & English), distress support (Tele-MANAS 14416), and routing intents.
"""

# Today's active preparation tasks for first-time job seekers
TODAY_TASKS = {
    "en": [
        {
            "id": "task-1",
            "title": "Revise Arrays & Linked Lists on SWAYAM",
            "minutes": 30,
            "category": "learning",
            "skill": "dsa",
            "done": False,
        },
        {
            "id": "task-2",
            "title": "Practise STAR method for HR behavioral questions",
            "minutes": 20,
            "category": "interview",
            "skill": "communication",
            "done": False,
        },
        {
            "id": "task-3",
            "title": "Review & submit application for Accenture Associate Software Engineer",
            "minutes": 15,
            "category": "jobs",
            "skill": "application",
            "done": False,
        },
    ],
    "hi": [
        {
            "id": "task-1",
            "title": "SWAYAM पर Arrays और Linked Lists का रिवीज़न करें",
            "minutes": 30,
            "category": "learning",
            "skill": "dsa",
            "done": False,
        },
        {
            "id": "task-2",
            "title": "HR राउंड के लिए STAR मेथड से उत्तर अभ्यास करें",
            "minutes": 20,
            "category": "interview",
            "skill": "communication",
            "done": False,
        },
        {
            "id": "task-3",
            "title": "Accenture एसोसिएट सॉफ्टवेयर इंजीनियर पद के लिए आवेदन पूरा करें",
            "minutes": 15,
            "category": "jobs",
            "skill": "application",
            "done": False,
        },
    ],
}

# The 6 registered sub-agents orchestrated by Genie
SUB_AGENTS = {
    "profile": {
        "slug": "profile-agent",
        "name": "Profile",
        "keywords": ["cv", "resume", "profile", "skills", "psychometric", "रिज्यूमे", "बायोडाटा"],
        "description": "Extracts skills, projects, and education from CV; scores psychometric tests.",
    },
    "jobs": {
        "slug": "job-matcher-agent",
        "name": "Job Matcher",
        "keywords": ["job", "jobs", "opening", "openings", "naukri", "company", "vacanc", "नौकरी", "कंपनी"],
        "description": "Finds and ranks matching job opportunities and explains why they fit.",
    },
    "learning": {
        "slug": "learning-curator-agent",
        "name": "Learning Curator",
        "keywords": ["learn", "course", "courses", "lecture", "study", "tutorial", "पढ़", "सीख", "कोर्स"],
        "description": "Curates free lectures from SWAYAM & NPTEL per skill gap.",
    },
    "planning": {
        "slug": "prep-planner-agent",
        "name": "Prep Planner",
        "keywords": ["plan", "plans", "today", "tasks", "schedule", "quiz", "आज", "प्लान", "टास्क", "क्विज़"],
        "description": "Builds daily action plans inside minutes budget and generates practice quizzes.",
    },
    "interviewer": {
        "slug": "interviewer-agent",
        "name": "Interviewer",
        "keywords": ["interview", "mock", "practice", "questions", "round", "इंटरव्यू", "अभ्यास"],
        "description": "Simulates realistic HR and Technical placement interview rounds.",
    },
    "report": {
        "slug": "report-agent",
        "name": "Report",
        "keywords": ["report", "score", "scores", "past", "feedback", "results", "रिपोर्ट", "स्कोर"],
        "description": "Generates post-interview reports with gaze, posture metrics, and fixes linked to lessons.",
    },
}

# Distress helpline info (Tele-MANAS)
TELE_MANAS = {
    "helpline": "14416",
    "name": "Tele-MANAS",
    "description": "National Tele Mental Health Programme of India (toll-free, 24x7, confidential)",
    "en": "I hear you, and it is completely normal to feel overwhelmed during job preparation. Let's take one slow, deep breath together. Please remember you are not alone: Tele-MANAS is a free, confidential mental health helpline available 24/7 across India — call 14416 anytime.",
    "hi": "मैं समझ सकता हूँ, नौकरी की तैयारी के दौरान ऐसा लगना बिल्कुल स्वाभाविक है। पहले एक गहरी और धीमी सांस लीजिए। आप अकेले नहीं हैं: भारत सरकार की Tele-MANAS हेल्पलाइन 14416 पर 24 घंटे मुफ़्त और गोपनीय सहायता उपलब्ध है।",
}
