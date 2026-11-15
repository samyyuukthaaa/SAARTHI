"""Static data and quiz banks for Prep Planner Agent.

Includes offline quiz banks covering fundamental placement topics
and demo constraints for scheduling.
"""

QUIZZES = {
    "dsa": [
        {"q": "What is the time complexity of accessing arr[i] in an array?", "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"], "answer": 0},
        {"q": "Which structure gives O(1) average lookup to check whether a character was seen before?", "options": ["Stack", "Hash set", "Linked list", "Queue"], "answer": 1},
        {"q": "Two pointers moving toward each other is a common way to…", "options": ["Sort a linked list", "Check if a string is a palindrome", "Build a heap", "Hash a string"], "answer": 1},
        {"q": "Reversing a string of length n in place takes…", "options": ["O(1) time", "O(log n) time", "O(n) time", "O(n log n) time"], "answer": 2},
        {"q": "A sliding window is most useful for…", "options": ["Longest substring without repeating characters", "Binary search", "Tree traversal", "Matrix multiplication"], "answer": 0},
    ],
    "oop": [
        {"q": "Hiding internal state and exposing methods is called…", "options": ["Inheritance", "Encapsulation", "Polymorphism", "Abstraction"], "answer": 1},
        {"q": "Method overriding is an example of…", "options": ["Compile-time polymorphism", "Run-time polymorphism", "Encapsulation", "Composition"], "answer": 1},
        {"q": "In Java, a class can extend how many classes?", "options": ["One", "Two", "Any number", "None"], "answer": 0},
        {"q": "An interface in Java mainly defines…", "options": ["Fields with values", "A contract of methods", "A constructor", "A package"], "answer": 1},
        {"q": "\"A Car has an Engine\" describes…", "options": ["Inheritance", "Composition", "Overloading", "Abstraction"], "answer": 1},
    ],
    "sql": [
        {"q": "Which clause filters groups after GROUP BY?", "options": ["WHERE", "HAVING", "ORDER BY", "LIMIT"], "answer": 1},
        {"q": "A LEFT JOIN returns…", "options": ["Only matching rows", "All rows from the left table", "All rows from the right table", "A Cartesian product"], "answer": 1},
        {"q": "Which keyword removes duplicate rows from a result?", "options": ["UNIQUE", "DISTINCT", "DROP", "TRIM"], "answer": 1},
        {"q": "COUNT(*) counts…", "options": ["Non-null values in a column", "All rows", "Distinct rows", "Columns"], "answer": 1},
        {"q": "A primary key must be…", "options": ["Unique and not null", "A number", "Indexed only", "A foreign key"], "answer": 0},
    ],
    "javascript": [
        {"q": "A closure is a function that…", "options": ["Has no name", "Remembers variables from where it was created", "Runs immediately", "Cannot return values"], "answer": 1},
        {"q": "What does `await` do inside an async function?", "options": ["Blocks the whole browser", "Pauses that function until the promise settles", "Creates a thread", "Cancels the promise"], "answer": 1},
        {"q": "`typeof null` returns…", "options": ["\"null\"", "\"object\"", "\"undefined\"", "\"number\""], "answer": 1},
        {"q": "Which runs first?", "options": ["setTimeout(fn, 0)", "A resolved promise's .then", "They run together", "It's random"], "answer": 1},
        {"q": "`===` differs from `==` because it…", "options": ["Is faster only", "Doesn't convert types", "Compares references only", "Works only on strings"], "answer": 1},
    ],
    "git": [
        {"q": "Which command creates a new branch and switches to it?", "options": ["git branch -d x", "git checkout -b x", "git merge x", "git push x"], "answer": 1},
        {"q": "`git pull` is roughly…", "options": ["fetch + merge", "commit + push", "clone + init", "stash + pop"], "answer": 0},
        {"q": "Where do changes go after `git add`?", "options": ["Remote", "Staging area", "Stash", "Another branch"], "answer": 1},
        {"q": "Which is safer for undoing a pushed commit?", "options": ["git reset --hard", "git revert", "git rm", "git clean"], "answer": 1},
    ],
    "aptitude": [
        {"q": "A train covers 120 km in 2 hours. Its speed in m/s is about…", "options": ["16.7", "33.3", "60", "120"], "answer": 0},
        {"q": "If 5 workers finish a job in 12 days, 10 workers finish it in…", "options": ["24 days", "6 days", "10 days", "12 days"], "answer": 1},
        {"q": "20% of 250 is…", "options": ["25", "50", "75", "125"], "answer": 1},
        {"q": "Next in the series 2, 6, 12, 20, …", "options": ["28", "30", "32", "26"], "answer": 1},
    ],
    "communication": [
        {"q": "In STAR, the R stands for…", "options": ["Reason", "Result", "Review", "Role"], "answer": 1},
        {"q": "A good self-introduction for a fresher lasts about…", "options": ["10 seconds", "1 minute", "5 minutes", "As long as needed"], "answer": 1},
        {"q": "When you don't know an answer, the best move is to…", "options": ["Guess confidently", "Stay silent", "Say what you do know and how you'd find out", "Change the topic"], "answer": 2},
        {"q": "Where should you look while answering in a video interview?", "options": ["At your own video", "At the camera / interviewer's face", "At your notes", "Away from the screen"], "answer": 1},
    ],
    "python": [
        {"q": "What does `len([1, [2, 3]])` return?", "options": ["1", "2", "3", "Error"], "answer": 1},
        {"q": "Which is immutable?", "options": ["list", "dict", "tuple", "set"], "answer": 2},
        {"q": "`[x*x for x in range(3)]` gives…", "options": ["[1, 4, 9]", "[0, 1, 4]", "[0, 1, 2]", "[0, 2, 4]"], "answer": 1},
        {"q": "Dictionary lookup by key is on average…", "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"], "answer": 0},
    ],
    "java": [
        {"q": "Which keyword prevents a class from being subclassed?", "options": ["static", "final", "abstract", "private"], "answer": 1},
        {"q": "Strings in Java are…", "options": ["Mutable", "Immutable", "Primitive", "Arrays"], "answer": 1},
        {"q": "Which collection keeps keys unique?", "options": ["ArrayList", "HashMap", "LinkedList", "Array"], "answer": 1},
        {"q": "The JVM runs…", "options": ["Java source code", "Bytecode", "Machine code only", "Python"], "answer": 1},
    ],
}

DEFAULT_CONSTRAINTS = {
    "minutes_per_day": 90,
    "deadline_days": 7,
    "preferred_session_mins": 45,
    "include_mock_interview": True,
    "include_daily_quiz": True,
}

DEMO_SHORTLIST = [
    {
        "id": "j1",
        "title": "Associate Software Engineer",
        "company": "Accenture",
        "location": "Hyderabad",
        "deadline_days": 5,
        "skills": ["java", "sql", "dsa", "oop", "communication"],
        "round": ["Online assessment", "Technical interview", "HR interview"],
    }
]
