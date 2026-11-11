# Campus Nexus · Presidency University AI Helpdesk

AI-powered university campus helpdesk built for **TECHNOPIA 2.0 · Build It in 60 Minutes** (Presidency University, School of Computer Science & Engineering).

Students ask campus questions in natural language. Nexus answers only from the official Presidency University sample information. If a fact is not in that data (such as private exam dates, fees, or personal records), it clearly says so instead of inventing details.

---

## 🌟 Key Features

- **Instant Standalone Mode:** Open `Campus Nexus Helpdesk.html` directly in any web browser without installing or running any server.
- **Full-Stack Web App:** Run the Flask backend (`app.py`) for live REST API, rate limiting, and server logging.
- **Presidency University Knowledge Constellation:** Covers Presidency University overview & location, academics & faculty advisors, attendance regulations, examinations & timetables, placements & career training, central library resources, hostel administration, certificates & records, student events (Technopia), and campus facilities.
- **Grounded AI Engine:** Uses word boundary token matching, category ranking, and explicit refusal logic to prevent hallucinations.
- **Optional Live LLM Support:** Easily plug in a free Groq API key (`llama-3.1-8b-instant`), Google Gemini key (`gemini-2.0-flash`), or OpenAI key (`gpt-4o-mini`) via `.env` or directly in the UI.
- **Voice Input:** Built-in speech-to-text input (🎙️) on supported browsers.
- **Cinematic UI:** Responsive design with automatic & manual Dark / Light theme toggle.

---

## 🚀 How to Run

### Option A: Instant Client-Side Mode (No installation required)
Simply double-click or open `Campus Nexus Helpdesk.html` in your favorite web browser (Chrome, Edge, Firefox, Safari).

### Option B: Full-Stack Mode (Flask Server)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   On Windows, simply run:
   ```cmd
   run.bat
   ```
   Or using Python directly:
   ```bash
   python app.py
   ```

3. **Open in browser:**
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 🔑 Optional LLM Configuration (.env)

If you wish to use live LLMs on the backend, copy `.env.example` to `.env` and fill in your keys:

```ini
GROQ_API_KEY=gsk_your_groq_key_here
# Optional alternatives:
# GEMINI_API_KEY=AIza...
# OPENAI_API_KEY=sk-...
```

*Note: Keys can also be entered directly in the web UI for the current browser tab and are never committed or logged.*

---

## 📋 Example Probes & Expected Behaviour

| Question | Expected Behaviour | Status |
| --- | --- | --- |
| Tell me about Presidency University | University overview, location in Rajanukunte, UGC/AICTE approval | Grounded |
| Whom should I contact for academic problems? | Faculty advisor | Grounded |
| Where can I find the examination timetable? | Official university channels & student portal | Grounded |
| Whom should I contact for placement training? | Placement Department (Career Services Center) | Grounded |
| How can I raise a hostel complaint? | Hostel Administration / Chief Warden | Grounded |
| What is the minimum attendance requirement? | Regulations require minimum attendance; tracked on ERP | Grounded |
| What facilities does the Central Library offer? | Textbooks, journals, IEEE digital access | Grounded |
| How do I get a bonafide certificate? | Administrative office / Student Affairs | Grounded |
| What is the exact date of my next examination? | **Unavailable** — explicitly refused, does not invent dates | Unavailable |
| What is the hostel fee? | **Unavailable** — fee balance managed via student finance portal | Unavailable |

---

## 📁 Project Structure

```
├── Campus Nexus Helpdesk.html   # Standalone zero-dependency AI Helpdesk UI
├── app.py                       # Flask web backend & REST API
├── engine.py                    # Grounded retrieval & LLM routing engine
├── knowledge.py                 # Official Presidency University dataset & triggers
├── requirements.txt             # Python dependencies (cross-platform)
├── run.bat                      # Windows launcher (auto-detects Python)
├── Procfile                     # Deployment descriptor (Render / Railway)
├── templates/
│   └── index.html               # Flask template
├── static/
│   ├── style.css                # Helpdesk stylesheets (light/dark theme)
│   └── app.js                   # Client-side chat logic & speech recognition
└── tests/
    └── test_backend.py          # Comprehensive test suite (100% pass)
```

---

## 🧪 Running Tests

To run the automated backend test suite:

```bash
python -m unittest discover tests
```

---

## 🌐 Backend API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/` | GET | Renders the Helpdesk console |
| `/api/health` | GET | Health check service status |
| `/api/catalog` | GET | Returns all knowledge domains |
| `/api/ask` | POST | Accepts `{"query": "..."}` and returns grounded answer, status, and sources |
