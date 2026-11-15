"""Shared catalogue and demo data for Learning Curator Agent.

All resources are 100% free, linked to official documentation or verified
educational platforms (NPTEL, freeCodeCamp, MIT OCW, Khan Academy, MDN, etc.).
No paid courses and no invented URLs.
"""

def _yt(q: str) -> str:
    return "https://www.youtube.com/results?search_query=" + q.replace(" ", "+")


SKILLS = {
    "dsa": "DSA: arrays and strings",
    "oop": "OOP interview questions",
    "java": "Java fundamentals",
    "python": "Python fundamentals",
    "cpp": "C++ fundamentals",
    "sql": "SQL queries and joins",
    "dbms": "DBMS basics",
    "os": "Operating systems basics",
    "networks": "Computer networks basics",
    "javascript": "JavaScript closures and async",
    "react": "React components and state",
    "html_css": "HTML and CSS layout",
    "node": "Node.js and REST APIs",
    "git": "Git branching",
    "linux": "Linux command line",
    "testing": "Testing basics",
    "excel": "Excel pivot tables",
    "statistics": "Basic statistics",
    "pandas": "Python pandas",
    "ml": "Machine learning basics",
    "cloud": "Cloud basics",
    "aptitude": "Quantitative aptitude",
    "communication": "Communication: self-introduction",
}

SKILL_DISPLAY = {
    "dsa": "DSA",
    "oop": "OOP",
    "java": "Java",
    "python": "Python",
    "cpp": "C++",
    "sql": "SQL",
    "dbms": "DBMS",
    "os": "Operating systems",
    "networks": "Networking",
    "javascript": "JavaScript",
    "react": "React",
    "html_css": "HTML/CSS",
    "node": "Backend APIs",
    "git": "Git",
    "linux": "Linux",
    "testing": "Testing",
    "excel": "Excel",
    "statistics": "Statistics",
    "pandas": "Data analysis",
    "ml": "Machine learning",
    "cloud": "Cloud",
    "aptitude": "Aptitude",
    "communication": "Communication",
}

CATALOGUE = [
    # DSA
    {"id": "r1", "skill": "dsa", "title": "Programming, Data Structures and Algorithms using Python", "provider": "NPTEL", "language": "English, Hindi subtitles", "format": "Lecture", "minutes": 95, "level": "Beginner", "url": "https://swayam.gov.in/explorer?searchText=data%20structures%20algorithms%20python", "is_free": True},
    {"id": "r2", "skill": "dsa", "title": "JavaScript Algorithms and Data Structures", "provider": "freeCodeCamp", "language": "English", "format": "Practice", "minutes": 60, "level": "Beginner", "url": "https://www.freecodecamp.org/learn", "is_free": True},
    {"id": "r3", "skill": "dsa", "title": "Arrays and strings explained in Hindi", "provider": "YouTube", "language": "Hindi", "format": "Video course", "minutes": 50, "level": "Beginner", "url": _yt("arrays strings dsa hindi"), "is_free": True},
    {"id": "r4", "skill": "dsa", "title": "Introduction to Algorithms (6.006)", "provider": "MIT OpenCourseWare", "language": "English", "format": "Lecture", "minutes": 80, "level": "Intermediate", "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/", "is_free": True},
    {"id": "r5", "skill": "dsa", "title": "Algorithms on Khan Academy", "provider": "Khan Academy", "language": "English, Hindi", "format": "Video course", "minutes": 45, "level": "Beginner", "url": "https://www.khanacademy.org/computing/computer-science/algorithms", "is_free": True},
    # OOP
    {"id": "r6", "skill": "oop", "title": "Object-oriented programming in Java, explained in Hindi", "provider": "YouTube", "language": "Hindi", "format": "Video course", "minutes": 55, "level": "Beginner", "url": _yt("oops in java hindi"), "is_free": True},
    {"id": "r7", "skill": "oop", "title": "Classes and objects: the official Java tutorial", "provider": "dev.java", "language": "English", "format": "Article", "minutes": 40, "level": "Beginner", "url": "https://dev.java/learn/", "is_free": True},
    {"id": "r8", "skill": "oop", "title": "Classes in Python", "provider": "Python docs", "language": "English", "format": "Article", "minutes": 30, "level": "Beginner", "url": "https://docs.python.org/3/tutorial/classes.html", "is_free": True},
    # Languages
    {"id": "r9", "skill": "java", "title": "Learn Java from the official dev.java path", "provider": "dev.java", "language": "English", "format": "Article", "minutes": 60, "level": "Beginner", "url": "https://dev.java/learn/", "is_free": True},
    {"id": "r10", "skill": "java", "title": "Java full course in Hindi", "provider": "YouTube", "language": "Hindi", "format": "Video course", "minutes": 90, "level": "Beginner", "url": _yt("java full course hindi"), "is_free": True},
    {"id": "r11", "skill": "python", "title": "The Python Tutorial", "provider": "Python docs", "language": "English", "format": "Article", "minutes": 60, "level": "Beginner", "url": "https://docs.python.org/3/tutorial/", "is_free": True},
    {"id": "r12", "skill": "python", "title": "CS50's Introduction to Programming with Python", "provider": "CS50", "language": "English", "format": "Video course", "minutes": 90, "level": "Beginner", "url": "https://cs50.harvard.edu/python/", "is_free": True},
    {"id": "r13", "skill": "cpp", "title": "LearnCpp: C++ from the ground up", "provider": "LearnCpp", "language": "English", "format": "Article", "minutes": 60, "level": "Beginner", "url": "https://www.learncpp.com/", "is_free": True},
    # Databases
    {"id": "r14", "skill": "sql", "title": "SQLBolt: interactive SQL lessons", "provider": "SQLBolt", "language": "English", "format": "Practice", "minutes": 45, "level": "Beginner", "url": "https://sqlbolt.com/", "is_free": True},
    {"id": "r15", "skill": "sql", "title": "SQL joins explained in Hindi", "provider": "YouTube", "language": "Hindi", "format": "Video course", "minutes": 35, "level": "Beginner", "url": _yt("sql joins hindi"), "is_free": True},
    {"id": "r16", "skill": "dbms", "title": "Database Management Systems", "provider": "NPTEL", "language": "English, Hindi subtitles", "format": "Lecture", "minutes": 90, "level": "Beginner", "url": "https://swayam.gov.in/explorer?searchText=database%20management%20system", "is_free": True},
    {"id": "r17", "skill": "dbms", "title": "DBMS for placements in Hindi", "provider": "YouTube", "language": "Hindi", "format": "Video course", "minutes": 60, "level": "Beginner", "url": _yt("dbms placement hindi"), "is_free": True},
    # CS Core
    {"id": "r18", "skill": "os", "title": "Operating Systems: Three Easy Pieces (free book)", "provider": "OSTEP", "language": "English", "format": "Article", "minutes": 60, "level": "Intermediate", "url": "https://pages.cs.wisc.edu/~remzi/OSTEP/", "is_free": True},
    {"id": "r19", "skill": "os", "title": "Operating systems for interviews in Hindi", "provider": "YouTube", "language": "Hindi", "format": "Video course", "minutes": 60, "level": "Beginner", "url": _yt("operating system interview hindi"), "is_free": True},
    {"id": "r20", "skill": "networks", "title": "Computer networks full course", "provider": "YouTube", "language": "English", "format": "Video course", "minutes": 60, "level": "Beginner", "url": _yt("computer networks full course"), "is_free": True},
    # Web
    {"id": "r21", "skill": "javascript", "title": "Asynchronous JavaScript guide", "provider": "MDN", "language": "English", "format": "Article", "minutes": 30, "level": "Intermediate", "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Async_JS", "is_free": True},
    {"id": "r22", "skill": "javascript", "title": "JavaScript closures", "provider": "MDN", "language": "English", "format": "Article", "minutes": 20, "level": "Intermediate", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures", "is_free": True},
    {"id": "r23", "skill": "javascript", "title": "JavaScript in Hindi: promises and async/await", "provider": "YouTube", "language": "Hindi", "format": "Video course", "minutes": 40, "level": "Beginner", "url": _yt("javascript promises async await hindi"), "is_free": True},
    {"id": "r24", "skill": "react", "title": "Learn React (official tutorial)", "provider": "react.dev", "language": "English", "format": "Practice", "minutes": 60, "level": "Beginner", "url": "https://react.dev/learn", "is_free": True},
    {"id": "r25", "skill": "html_css", "title": "Learn CSS", "provider": "web.dev", "language": "English", "format": "Article", "minutes": 45, "level": "Beginner", "url": "https://web.dev/learn/css", "is_free": True},
    {"id": "r26", "skill": "html_css", "title": "Responsive Web Design certification", "provider": "freeCodeCamp", "language": "English", "format": "Practice", "minutes": 60, "level": "Beginner", "url": "https://www.freecodecamp.org/learn", "is_free": True},
    {"id": "r27", "skill": "node", "title": "Learn Node.js", "provider": "Node.js docs", "language": "English", "format": "Article", "minutes": 45, "level": "Beginner", "url": "https://nodejs.org/en/learn", "is_free": True},
    # Tools
    {"id": "r28", "skill": "git", "title": "Learn Git Branching (interactive)", "provider": "learngitbranching", "language": "English, Hindi", "format": "Practice", "minutes": 30, "level": "Beginner", "url": "https://learngitbranching.js.org/", "is_free": True},
    {"id": "r29", "skill": "git", "title": "Pro Git book, chapters 1-3", "provider": "git-scm", "language": "English", "format": "Article", "minutes": 45, "level": "Beginner", "url": "https://git-scm.com/book/en/v2", "is_free": True},
    {"id": "r30", "skill": "linux", "title": "Linux Journey", "provider": "Linux Journey", "language": "English", "format": "Practice", "minutes": 40, "level": "Beginner", "url": "https://linuxjourney.com/", "is_free": True},
    {"id": "r31", "skill": "testing", "title": "Getting started with pytest", "provider": "pytest docs", "language": "English", "format": "Article", "minutes": 25, "level": "Beginner", "url": "https://docs.pytest.org/en/stable/getting-started.html", "is_free": True},
    {"id": "r32", "skill": "cloud", "title": "Docker getting-started guide", "provider": "Docker docs", "language": "English", "format": "Practice", "minutes": 45, "level": "Beginner", "url": "https://docs.docker.com/get-started/", "is_free": True},
    # Data
    {"id": "r33", "skill": "excel", "title": "Excel pivot tables in Hindi", "provider": "YouTube", "language": "Hindi", "format": "Video course", "minutes": 30, "level": "Beginner", "url": _yt("excel pivot table hindi"), "is_free": True},
    {"id": "r34", "skill": "statistics", "title": "Statistics and probability", "provider": "Khan Academy", "language": "English, Hindi", "format": "Video course", "minutes": 60, "level": "Beginner", "url": "https://www.khanacademy.org/math/statistics-probability", "is_free": True},
    {"id": "r35", "skill": "pandas", "title": "pandas getting-started tutorials", "provider": "pandas docs", "language": "English", "format": "Article", "minutes": 45, "level": "Beginner", "url": "https://pandas.pydata.org/docs/getting_started/intro_tutorials/", "is_free": True},
    {"id": "r36", "skill": "ml", "title": "Machine Learning Crash Course", "provider": "Google", "language": "English", "format": "Video course", "minutes": 90, "level": "Intermediate", "url": "https://developers.google.com/machine-learning/crash-course", "is_free": True},
    # Placement
    {"id": "r37", "skill": "aptitude", "title": "Aptitude practice questions", "provider": "IndiaBIX", "language": "English", "format": "Practice", "minutes": 40, "level": "Beginner", "url": "https://www.indiabix.com/aptitude/questions-and-answers/", "is_free": True},
    {"id": "r38", "skill": "aptitude", "title": "Quantitative aptitude tricks in Hindi", "provider": "YouTube", "language": "Hindi", "format": "Video course", "minutes": 45, "level": "Beginner", "url": _yt("quantitative aptitude placement hindi"), "is_free": True},
    {"id": "r39", "skill": "communication", "title": "Structuring answers with the STAR method", "provider": "YouTube", "language": "English", "format": "Video course", "minutes": 20, "level": "Beginner", "url": _yt("STAR method interview answers"), "is_free": True},
    {"id": "r40", "skill": "communication", "title": "Tell me about yourself: a 60-second answer, in Hindi", "provider": "YouTube", "language": "Hindi", "format": "Video course", "minutes": 15, "level": "Beginner", "url": _yt("tell me about yourself fresher hindi"), "is_free": True},
]

DEMO_USER = {
    "name": "Ananya",
    "city": "Hyderabad",
    "languages": ["English", "Hindi"],
    "minutes_per_day": 90,
    "skills": ["java", "sql", "react", "git", "html_css", "javascript"],
    "education": "B.Tech CSE, 2026",
    "projects": 3,
    "psych": {"top": "I"},
    "quiz": {"oop": 40},
    "shortlist": [
        {
            "id": "j1",
            "title": "Associate Software Engineer",
            "company": "Accenture",
            "skills": ["java", "sql", "dsa", "oop", "communication"],
            "round": ["Online assessment", "Technical interview", "HR interview"],
        }
    ],
}
