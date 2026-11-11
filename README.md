# Campus Nexus

AI-powered university campus helpdesk built for **TECHNOPIA 2.0 · Build It in 60 Minutes** (Presidency University, School of Computer Science & Engineering).

Students ask campus questions in natural language. Nexus answers only from the official sample university information. If a fact is not in that data, it says so instead of inventing details.

## Features

- Cinematic chat helpdesk (desktop + mobile)
- Knowledge constellation for academics, attendance, exams, placements, library, hostel, administration, events
- Grounded AI answers with source lock panel
- Explicit unknown-query handling (example: exact exam date)
- Optional live LLM via Groq / Gemini / OpenAI
- Voice input where the browser supports it

## AI integration

1. **Grounding retriever** maps the student question onto the sample campus knowledge.
2. **Live model (preferred):** Groq `llama-3.1-8b-instant` (or Gemini / OpenAI if those keys are set). The model is instructed to answer *only* from the supplied sample information.
3. **Fallback engine:** if no API key is configured, Nexus still classifies the question and generates a grounded reply or a clear refusal. This is not a static FAQ list — answers are composed from retrieved facts and unsupported intents are rejected.

Keys are read from `.env` or pasted in the UI for the current browser tab. They are never committed.

## Run

```bash
py -3 -m pip install -r requirements.txt
py -3 app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

Optional `.env`:

```
GROQ_API_KEY=gsk_...
```

## Example probes

| Question | Expected behaviour |
| --- | --- |
| Whom should I contact for academic problems? | Faculty advisor |
| Where can I find the examination timetable? | Official university channels |
| Whom should I contact for placement training? | Placement Department |
| How can I raise a hostel complaint? | Hostel Administration |
| What is the exact date of my next examination? | Unavailable — do not invent a date |

## Stack

Python, Flask, HTML/CSS/JS. No database and no login, as allowed by the problem statement.

## Screenshots

Place UI captures in `screenshots/` before GitHub submission.
