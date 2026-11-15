"""Realistic demo data for Saarathi Report Agent.

Provides session transcripts, behavioral & tracking metrics, and curated learning items.
"""

# Demo interview session transcript with timestamps
DEMO_TRANSCRIPTS = {
    "demo": {
        "session_id": "demo",
        "candidate_name": "Rahul Verma",
        "round_type": "hr",
        "mode": "online",
        "turns": [
            {
                "timestamp": "0:15",
                "question": "Could you briefly introduce yourself and share what inspired you to pursue computer science?",
                "answer": "I am a final year computer science student at JNTU Hyderabad. I built an expense tracker in React and Flask because my hostel mates kept losing track of expenses, and in the end 40 students used it regularly.",
                "duration_seconds": 28,
                "words": 38,
                "fillers": 0,
                "score": 75,
            },
            {
                "timestamp": "1:05",
                "question": "Tell me about a challenging technical bug you encountered in a team project and how you resolved it.",
                "answer": "Basically, we had a state synchronization loop in our React frontend where the API was getting called multiple times per second. I investigated using DevTools and resolved it by fixing the useEffect dependency array.",
                "duration_seconds": 32,
                "words": 37,
                "fillers": 1,
                "score": 68,
            },
            {
                "timestamp": "1:55",
                "question": "Why do you want to join our engineering graduate program specifically?",
                "answer": "Basically like I think, you know, your team works on large-scale distributed systems and high-throughput APIs. I want to learn solid design patterns, contribute to production code, and collaborate in cross-functional teams.",
                "duration_seconds": 34,
                "words": 35,
                "fillers": 4,
                "score": 60,
            },
            {
                "timestamp": "2:45",
                "question": "Where do you see your technical career progressing over the next 2 to 3 years?",
                "answer": "I aim to grow into an independent software engineer who can own microservices from architecture to deployment, and mentor junior interns as they onboard.",
                "duration_seconds": 25,
                "words": 25,
                "fillers": 2,
                "score": 65,
            },
        ],
    }
}

# Tracking and behavioral metrics for the session
DEMO_METRICS = {
    "demo": {
        "session_id": "demo",
        "overall": 64,
        "scores": {
            "answer_quality": 68,
            "eye_contact": 58,
            "voice_and_pace": 62,
            "posture": 70,
            "confidence": 64,
        },
        "metrics": {
            "eye_contact_percentage": 58,
            "words_per_minute": 135,
            "filler_words_count": 7,
            "filler_words_used": ["basically", "like", "you know"],
            "posture_score": 70,
            "slouch_detected_seconds": 18,
            "total_duration_seconds": 210,
        },
        "gaze_distribution": {
            "interviewer": 58,
            "notes_on_desk": 22,
            "floor": 12,
            "away": 8,
        },
        "moments": [
            {
                "timestamp": "0:15",
                "type": "good",
                "text": "Clear, structured self-introduction with measurable impact (40 active users).",
            },
            {
                "timestamp": "1:22",
                "type": "fix",
                "text": "Looked away at desk notes for 6 seconds while recalling React lifecycle.",
            },
            {
                "timestamp": "2:10",
                "type": "fix",
                "text": "Used 4 filler words ('basically', 'like', 'you know') in 30 seconds.",
            },
        ],
    }
}

# Curated free lessons from NPTEL, SWAYAM, and IIT open courses
LEARNING_ITEMS = [
    {
        "id": "lesson-comm-eye",
        "skill": "eye_contact",
        "title": "Holding Eye Contact in Virtual & In-Person Interviews",
        "duration_minutes": 12,
        "platform": "SWAYAM",
        "language": "English / Hindi",
        "url": "https://swayam.gov.in/courses/interview-presence",
        "fix_category": "eye_contact",
        "description": "Techniques for natural gaze, focal positioning with webcams, and eye contact resets.",
    },
    {
        "id": "lesson-comm-fillers",
        "skill": "voice_and_pace",
        "title": "Pausing vs. Filler Words: The Power of Intentional Silence",
        "duration_minutes": 10,
        "platform": "NPTEL",
        "language": "English",
        "url": "https://onlinecourses.nptel.ac.in/noc24_hs01",
        "fix_category": "voice_and_pace",
        "description": "How to replace 'like', 'basically', and verbal hesitations with controlled 2-second breaths.",
    },
    {
        "id": "lesson-comm-star",
        "skill": "answer_quality",
        "title": "Structuring Behavioral Answers with STAR: Situation to Result",
        "duration_minutes": 15,
        "platform": "NPTEL",
        "language": "English",
        "url": "https://nptel.ac.in/courses/109/104/109104031/",
        "fix_category": "answer_quality",
        "description": "Framework to structure concise, punchy answers that quantify business or technical results.",
    },
    {
        "id": "lesson-posture",
        "skill": "posture",
        "title": "Interview Body Language: Confident Posture and Seating",
        "duration_minutes": 8,
        "platform": "SWAYAM",
        "language": "English / Hindi",
        "url": "https://swayam.gov.in/courses/body-language",
        "fix_category": "posture",
        "description": "Ergonomics, camera alignment, and open posture during online and room interviews.",
    },
    {
        "id": "lesson-dsa-explain",
        "skill": "technical_explanation",
        "title": "Explaining Code & Algorithmic Complexity Clearly Under Pressure",
        "duration_minutes": 20,
        "platform": "NPTEL",
        "language": "English",
        "url": "https://onlinecourses.nptel.ac.in/noc24_cs42",
        "fix_category": "answer_quality",
        "description": "Communication patterns for whiteboarding and technical problem solving.",
    },
]
