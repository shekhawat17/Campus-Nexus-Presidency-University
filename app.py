from __future__ import annotations

import logging
import os
import time
from collections import defaultdict, deque

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

from engine import answer  # noqa: E402
from knowledge import public_catalog  # noqa: E402

app = Flask(__name__, static_folder="static", template_folder="templates")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("campus-nexus")

MAX_QUERY_CHARS = 500
RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MIN", "30"))
_hits: dict[str, deque] = defaultdict(deque)


def _rate_limited(ip: str) -> bool:
    now = time.time()
    q = _hits[ip]
    while q and now - q[0] > 60:
        q.popleft()
    if len(q) >= RATE_LIMIT:
        return True
    q.append(now)
    return False


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "campus-nexus", "campus": "Presidency University"})


@app.get("/api/catalog")
def catalog():
    return jsonify({"domains": public_catalog()})


@app.post("/api/ask")
def ask():
    if _rate_limited(request.remote_addr or "unknown"):
        return jsonify({"ok": False, "error": "Too many questions. Wait a minute and try again."}), 429

    payload = request.get_json(silent=True) or {}
    query = str(payload.get("query") or payload.get("message") or "").strip()

    if not query:
        return jsonify({"ok": False, "error": "Please enter a campus question to begin."}), 400

    if len(query) > MAX_QUERY_CHARS:
        return jsonify({"ok": False, "error": f"Keep questions under {MAX_QUERY_CHARS} characters."}), 400

    runtime_key = {}
    for header, name in (("X-Groq-Key", "groq"), ("X-Gemini-Key", "gemini"), ("X-OpenAI-Key", "openai")):
        val = request.headers.get(header)
        if val:
            runtime_key[name] = val

    for field, name in (("groqKey", "groq"), ("geminiKey", "gemini"), ("openaiKey", "openai")):
        val = payload.get(field)
        if val:
            runtime_key[name] = str(val)

    result = answer(query, runtime_key=runtime_key or None)
    log.info("ask status=%s model=%s", result.get("status"), result.get("model"))
    return jsonify(result), (200 if result.get("ok") else 400)


@app.errorhandler(404)
def not_found(_):
    return jsonify({"ok": False, "error": "Endpoint not found."}), 404


@app.errorhandler(500)
def server_error(exc):
    log.exception("server error: %s", exc)
    return jsonify({"ok": False, "error": "Server error. Check the terminal for details."}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    host = os.getenv("HOST", "127.0.0.1")
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
