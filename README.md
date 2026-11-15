# Saarathi — your career copilot

> *Saarathi* (सारथी): the charioteer who steers the journey. The student drives; Saarathi shows the road.

## The problem

Every year, millions of young people in India finish a degree and step into the job market alone.

Many are the **first in their family** to attempt a tech career. They come from tier-2 and tier-3 towns, from colleges with thin placement cells, and from homes where no one has ever sat through a technical interview. Talent is not what they lack. What they lack is **a guide**:

- **They don't know which jobs actually fit them.** Job portals show thousands of listings with no explanation of why one matches and another doesn't, so students apply blindly and are rejected silently.
- **They don't know what to learn next.** The gap between a college syllabus and a job description is real, and the courses that close it are often paid, in English only, or buried among thousands of videos of uneven quality.
- **They have never practised an interview.** Mock interviews and career coaching are a privilege of metro campuses and paid bootcamps. A student's first real interview is often their first interview of any kind, and nerves, eye contact and structure cost them offers they were qualified for.
- **They face it alone, and it wears them down.** Repeated rejection with no feedback turns into self-doubt. Students stop applying, not because they can't do the job, but because nobody told them how close they were.

The result is a quiet waste of potential at national scale: capable people missing opportunities for reasons that have nothing to do with ability and everything to do with access.

## What Saarathi does

Saarathi gives every student the guide that privileged students take for granted, **free, in their own language, on their phone**.

1. **Understands the student.** Reads their CV and a short psychometric test (RIASEC interests, Mini-IPIP personality, situational judgement) to build an honest profile, without inventing skills that aren't there.
2. **Finds jobs that fit, and explains why.** Ranks real listings from official job APIs against the student's skills, quiz scores and interests, and shows the reasons and the skill gaps for each match.
3. **Closes the gaps with free learning.** For each missing skill, recommends at most two free, verified lectures or courses in the student's language, sized to the minutes they have each day.
4. **Turns it into a daily plan.** Builds a day-by-day plan inside the student's time budget and deadlines, mixing lessons, quizzes, applications and mock interviews.
5. **Lets them practise interviews that feel real.** A 3D interview room (or an online call) with an interviewer who asks, follows up and coaches answer structure without giving answers away. Head and eye tracking run entirely in the browser; video never leaves the device.
6. **Gives honest, kind feedback.** After each interview, a report with scores, where they looked, timestamped moments and exactly three fixes, each linked to a real lesson.
7. **Is there when it gets hard.** "Ask Saarathi", a voice assistant in Hindi or English on every page, answers questions, routes them to the right agent, and responds to distress with warmth and the free Tele-MANAS helpline (**14416**).

## Architecture

```
Next.js website (this repo root)  ──REST / WebSocket──▶  FastAPI backend (backend/)
                                                              │
                                                              ▼
                                               Seven agents (agents/, backend/app/agents/)
                                               Profile · Job Matcher · Learning Curator ·
                                               Prep Planner · Interviewer · Report · Genie
```

- **`app/`, `components/`, `lib/`**: the Next.js website.
- **`backend/`**: the FastAPI API the website talks to. See [backend/README.md](backend/README.md) for endpoints and the interview WebSocket protocol.
- **`agents/`**: the seven agents built in **AgentFoundry**, each a standalone Python agent with its own tools.
- **`.codenow/agent-studio/`**: agent manifests, versioned system prompts and smoke evals for every agent.

## The agents

| Agent | Folder | What it does | Tools |
| --- | --- | --- | --- |
| **Genie** (orchestrator) | [agents/genie](agents/genie) | Voice assistant. Replies in Hindi or English in 2–4 short sentences, routes each question to the right specialist, flags distress and shares Tele-MANAS 14416, declines off-topic requests. Falls back to a rule-based pipeline when no API key is set. | `get_today_tasks`, `flag_distress` |
| **Profile** | [agents/profile](agents/profile) | CV text + psychometric answers → structured profile: skills, projects, education, interests, languages. Never guesses skills. | `parse_cv`, `score_psychometric`, `save_profile` |
| **Job Matcher** | [agents/job_matcher](agents/job_matcher) | Ranks cached and live jobs against the profile and explains each match. | `get_profile`, `search_cached_jobs`, `search_live_jobs`, `explain_match` |
| **Learning Curator** | [agents/learning_curator](agents/learning_curator) | At most two free, verified resources per skill gap, matched to language, level and daily time. Never invents links or suggests paid courses. | `get_skill_gaps`, `search_catalogue`, `search_youtube`, `save_learning_items` |
| **Prep Planner** | [agents/prep_planner](agents/prep_planner) | Day-by-day plan within the student's daily time and deadlines; readiness quizzes. | `get_shortlist`, `get_learning_items`, `get_constraints`, `create_todo_plan`, `generate_quiz` |
| **Interviewer** | [agents/interviewer](agents/interviewer) | HR and technical mock interviews. One question at a time, never reveals scores mid-interview, hints coach structure (STAR, definition + trade-offs) but never give answers. | `get_job_requirements`, `get_profile`, `next_question`, `score_answer`, `give_hint` |
| **Report** | [agents/report](agents/report) | Post-interview report: overall score, one line each on answers, eye contact, voice and posture, exactly three fixes linked to lessons, timestamped moments. Never invents numbers. | `get_transcript`, `get_session_metrics`, `get_learning_items`, `write_report` |

## Setup

### Prerequisites

- **Node.js 18.17 or later** (for Next.js 14)
- **Python 3.10 or later** (developed on 3.12)
- **Chrome or Edge** (camera, microphone and face tracking in the interview room)
- Optional API keys (the app runs without any of them, see step 3)

### 1. Clone and install the website

```bash
git clone https://github.com/samyyuukthaaa/SAARTHI-Your-Career-Co-Pilot..git saarathi
cd saarathi
npm install
```

### 2. Install the backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\pip install -r requirements.txt
# macOS / Linux
.venv/bin/pip install -r requirements.txt

cd ..
```

### 3. Configure environment

```bash
cp .env.example .env.local            # website
cp backend/.env.example backend/.env  # backend
```

In **`.env.local`** set `NEXT_PUBLIC_USE_MOCKS=false` to use the real backend. Leave it `true` to run the website alone on demo data from `lib/mock.ts`. `NEXT_PUBLIC_API_URL` and `NEXT_PUBLIC_WS_URL` can stay empty: the website then calls port 8000 on whatever host it is served from (`localhost` or `127.0.0.1`).

In **`backend/.env`** every key is optional. Without keys, the agents use built-in rules, jobs come from Remotive and Arbeitnow (free, no key) plus seeded demo listings, and notifications are logged instead of sent.

| Key | What it turns on |
| --- | --- |
| `ANTHROPIC_API_KEY`, `SAARATHI_MODEL` | LLM-powered CV parsing, interviewer follow-ups, Genie replies and report summaries |
| `ADZUNA_APP_ID`, `ADZUNA_APP_KEY` | Extra live job listings from Adzuna |
| `YOUTUBE_API_KEY` | Live lecture search when the catalogue has nothing in the student's language |
| `N8N_WEBHOOK_URL` | Email / WhatsApp notifications via n8n |
| `CRON_SECRET` | Protects `POST /cron/daily` (daily job refresh and today's steps) |
| `CORS_ORIGINS` | Extra allowed origins; `localhost` and `127.0.0.1` on any port are already allowed |

### 4. Run everything

From the repo root, one command starts both servers with prefixed logs:

```bash
npm run dev:all
```

- Website: http://localhost:3000
- API: http://127.0.0.1:8000 (interactive docs at http://127.0.0.1:8000/docs)

`dev:all` uses `backend/.venv` automatically if it exists. Press `Ctrl+C` to stop both.

To run them separately, use `npm run dev:frontend` and `npm run dev:backend` in two terminals. `dev:backend` uses the `python` on your PATH, so activate `backend/.venv` first.

### 5. Try it

1. Open http://localhost:3000 and start onboarding: upload a CV PDF, pick languages and daily time, take the short test.
2. Check **Jobs**, **Learn** and **Plan**.
3. Go to **Interview**, allow camera and microphone, and do a round in the 3D room or the online call.
4. Read the report that opens when the interview ends.
5. Tap **Ask Saarathi** on any page and ask something in Hindi or English.

Camera and microphone need **HTTPS** or `localhost`.

### Tests and checks

```bash
cd backend && .venv/Scripts/python -m pytest -q   # macOS/Linux: .venv/bin/python
npm run typecheck
npm run lint
```

### Run an agent on its own (optional)

The standalone agents in `agents/` use the Gemini API (`gemini-3.5-flash-lite`). Put your key in `agents/profile/.env.local` (the other agents read it from there too) or in a `.env.local` next to the agent:

```
GEMINI_API_KEY=...
```

Then run an agent from its folder with a prompt:

```bash
cd agents/job_matcher
pip install -r requirements.txt
python agent.py "find jobs matching my profile"

cd ../genie
python agent.py "आज मुझे क्या करना है?"
```

Genie and Report fall back to built-in rules without a key and record traces to `.codenow/agent-studio/traces/`. Smoke evals for every agent are in `.codenow/agent-studio/evals/`.

### Troubleshooting

- **"Failed to fetch" on a page:** the backend isn't running, or `NEXT_PUBLIC_USE_MOCKS` is `false` while only the website is up. Start it with `npm run dev:all`.
- **Port already in use:** stop whatever is using port 3000 or 8000, or change the port in `package.json`.
- **`python` not found on Windows:** install Python from python.org and tick "Add to PATH", or create `backend/.venv` so `dev:all` finds it.
- **Camera does not start:** open the site on `localhost` (not a LAN IP over plain HTTP) and allow camera access in the browser.

## Pages

| Route | What it is | Agent behind it |
| --- | --- | --- |
| `/` | Landing page | — |
| `/onboarding` | CV upload → languages and daily time → psychometric test | Profile |
| `/home` | Today's steps on the path, readiness score, new matches | Prep Planner, Job Matcher |
| `/jobs` | Ranked jobs with reasons, skill gaps, shortlist, apply link-out | Job Matcher |
| `/learn` | Free lectures and courses per skill gap, mark done, quiz | Learning Curator |
| `/plan` | The week's plan | Prep Planner |
| `/interview` | Choose round (HR / technical) and setting (in-person room / online call) | — |
| `/interview/room` | 3D in-person room: knock and walk in, head-coupled camera, eye contact, calibration, interviewer reactions | Interviewer |
| `/interview/online` | Meet-style video interview with a 2D interviewer | Interviewer |
| `/report/[id]` | Scores vs last time, where you looked, moments, fixes linked to lessons | Report |
| Floating button | "Ask Saarathi" voice assistant on every app page | Genie |

## Where things live

```
app/                     routes (App Router)
  (app)/                 pages inside the app shell (rail + mobile tab bar)
  interview/room         3D room page
  interview/online       online call page
components/
  AppShell.tsx           navigation, language toggle
  Genie.tsx              "Ask Saarathi" assistant panel
  PathThread.tsx         today's steps on the marigold path (signature element)
  interview/Room3D.tsx   React Three Fiber room, interviewer, head-coupled camera rig
  interview/useInterviewSession.ts  interview session state
lib/
  tracking/useTracking.ts  MediaPipe Face Landmarker: head position, rotation, gaze, eye contact, calibration
  tracking/oneEuro.ts      smoothing filter
  api.ts                   REST + WebSocket client with mock fallbacks
  mock.ts                  demo data shaped like the API contract
  store.ts                 per-device preferences (language, shortlist, done items)
  i18n.ts                  English / Hindi strings for the shell
scripts/dev.mjs          runs backend + frontend together (npm run dev:all)
backend/                 FastAPI app, agent wrappers, SQLite store, tests
agents/                  standalone AgentFoundry agents and their tools
.codenow/agent-studio/   agent manifests, system prompts, smoke evals
```

## Privacy and safety

- Camera video is processed in the browser. Only numbers (eye contact, head angle, posture) are sent to the backend.
- Jobs come only from official APIs, never scraping. Learning resources are linked, never re-hosted.
- Students can delete their profile at any time (`DELETE /profile`).
- Genie watches for signs of distress and points to Tele-MANAS 14416, India's free, confidential mental-health helpline.

## Tuning the tracking

`useTracking` exposes a 5 Hz `snapshot` for UI and a per-frame `live` ref for the 3D scene. If eye contact feels too strict or loose, change `eyeContactThreshold` (default 0.2). If yaw or pitch signs look inverted on a device, flip them in `useTracking.ts`.

## Design

- Colours: paper `#F4F6F5`, ink `#14212B`, peacock `#0F5C6E` (primary), marigold `#E9A23B` (only for "your next step"), leaf `#3E8E63`, brick `#B4473A`.
- Type: Anek Latin (headings, using its width axis) and Mukta (body), both by Ek Type with matching Devanagari, Telugu and Tamil families.
- Mark: a chariot wheel. A saarathi steers the journey; the marigold hub is the user.

## Licence

MIT. Learning resources are linked, never re-hosted.
