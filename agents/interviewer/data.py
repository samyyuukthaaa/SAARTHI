"""Static data, question banks, hints, and fillers for Interviewer Agent.

Follows real Indian campus recruitment and fresher interview patterns.
Hints coach answer structure (STAR method, trade-offs) without giving away solutions.
"""

QUESTIONS = {
    "hr": [
        {
            "id": "hr-1",
            "q": "Hello {name}, please have a seat. To begin, tell me a little about yourself.",
            "kind": "intro",
            "keywords": ["project", "college", "skill", "interest", "learning"],
        },
        {
            "id": "hr-2",
            "q": "Why do you want to start your career with a company like {company}?",
            "kind": "motivation",
            "keywords": ["learn", "grow", "product", "team", "customers", "culture"],
        },
        {
            "id": "hr-3",
            "q": "Tell me about a time a college or personal project did not go to plan. What did you do?",
            "kind": "behavioural",
            "keywords": ["situation", "decided", "result", "learned", "team", "fix"],
        },
        {
            "id": "hr-4",
            "q": "What is one technical or soft skill weakness you are actively working on right now?",
            "kind": "self",
            "keywords": ["working on", "improve", "practice", "feedback", "learning"],
        },
        {
            "id": "hr-5",
            "q": "Where do you see yourself professionally in two to three years?",
            "kind": "future",
            "keywords": ["skills", "responsibility", "lead", "learn", "ownership"],
        },
        {
            "id": "hr-6",
            "q": "Do you have any questions for me about the team, culture, or technology?",
            "kind": "close",
            "keywords": ["team", "role", "training", "expect", "tech stack"],
        },
    ],
    "technical": [
        {
            "id": "tech-1",
            "q": "Let's start with fundamentals. What is the key difference between an array and a linked list in memory and operations?",
            "kind": "concept",
            "keywords": ["contiguous", "memory", "index", "pointer", "insert", "o(1)", "o(n)"],
        },
        {
            "id": "tech-2",
            "q": "How would you find the first repeating character in a string? Walk me through your approach and time complexity.",
            "kind": "problem",
            "keywords": ["hash", "set", "map", "loop", "o(n)", "visited", "array"],
        },
        {
            "id": "tech-3",
            "q": "Explain object-oriented inheritance and polymorphism with an example from a project you built.",
            "kind": "concept",
            "keywords": ["parent", "child", "class", "extends", "reuse", "override", "interface"],
        },
        {
            "id": "tech-4",
            "q": "What is the difference between an INNER JOIN and a LEFT JOIN in SQL? When would you choose one over the other?",
            "kind": "concept",
            "keywords": ["matching", "rows", "null", "left table", "all", "join"],
        },
        {
            "id": "tech-5",
            "q": "Walk me through the hardest bug or technical challenge you debugged recently. How did you isolate and resolve it?",
            "kind": "behavioural",
            "keywords": ["bug", "debug", "log", "cause", "fixed", "test", "root cause"],
        },
    ],
}

HINTS = {
    "intro": "Keep it to about 60–90 seconds: who you are, 1–2 projects you're proud of, key technical skills, and why you're eager for this role.",
    "motivation": "Connect something specific about the company's domain or engineering culture to your own interests. One concrete reason beats several generic ones.",
    "behavioural": "Use the STAR method: one line on the Situation, your specific Task, the Action you personally took, and the final Result with a lesson.",
    "self": "Name a real skill gap that doesn't disqualify you from the job, then state exactly what steps and practice you are doing to overcome it.",
    "future": "Focus on growing technical depth, engineering craftsmanship, and taking greater ownership within the team rather than specific job titles.",
    "close": "Ask thoughtful questions about daily engineering practices, how code reviews happen, or what success looks like in the first 90 days.",
    "concept": "Start with a 1-sentence definition, highlight 2 concrete trade-offs (e.g. time vs space complexity), and give a quick example.",
    "problem": "State your brute force idea first, then explain how you'd optimize using a hash map or pointers. Mention time and space complexity.",
}

FOLLOW_UPS = {
    "short": "Could you elaborate a bit more on that and provide a specific example?",
    "result": "And what was the final outcome or impact of that action?",
    "complexity": "What would be the time and space complexity of that approach?",
    "example": "Can you give me a small code or practical example of that?",
}

FILLERS = [
    "basically",
    "actually",
    "like",
    "you know",
    "um",
    "uh",
    "matlab",
    "so yeah",
    "i mean",
    "kind of",
    "sort of",
]
