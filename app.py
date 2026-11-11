from __future__ import annotations

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from engine import answer
from knowledge import public_catalog

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "campus-nexus"})


@app.get("/api/catalog")
def catalog():
    return jsonify({"domains": public_catalog()})


@app.post("/api/ask")
def ask():
    payload = request.get_json(silent=True) or {}
    query = payload.get("query") or payload.get("message") or ""
    runtime_key = {}
    header_key = request.headers.get("X-Groq-Key")
    if header_key:
        runtime_key["groq"] = header_key
    if payload.get("groqKey"):
        runtime_key["groq"] = payload["groqKey"]
    if payload.get("geminiKey"):
        runtime_key["gemini"] = payload["geminiKey"]
    result = answer(query, runtime_key=runtime_key or None)
    status = 200 if result.get("ok") else 400
    return jsonify(result), status


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
