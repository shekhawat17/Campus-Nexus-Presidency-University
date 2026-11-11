"""Grounded campus helpdesk engine for Presidency University.

Uses an LLM when an API key is available. Always retrieves against the
Presidency University knowledge only, and refuses facts that are not in that set.
"""

from __future__ import annotations

import os
import re
from typing import Any

import httpx

from knowledge import KNOWLEDGE, UNSUPPORTED_INTENTS, knowledge_block

SYSTEM_PROMPT = """You are CAMPUS NEXUS, the official AI helpdesk for Presidency University (Bengaluru, Karnataka).

STRICT GROUNDING RULES:
- Answer ONLY using the PRESIDENCY UNIVERSITY SAMPLE INFORMATION below.
- If the student asks for a fact that is not explicitly present (exact individual exam dates, personal fees, phone numbers, personal schedules, specific library opening/closing hours, room numbers, marks, CGPA), say clearly that this is not available in the supplied campus data. Do not invent it.
- Be warm, concise, and useful. Prefer 2-4 short sentences.
- Name the relevant office or channel (Faculty Advisor, Placement Department, Hostel Administration, Controller of Examinations, Student Affairs).
- State that this is official sample competition data for Presidency University TECHNOPIA 2.0.

PRESIDENCY UNIVERSITY INFORMATION:
{knowledge}
"""


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", text.lower())


def retrieve(query: str, limit: int = 3) -> list[dict[str, Any]]:
    q = _normalize(query)
    scored: list[tuple[float, dict]] = []
    for item in KNOWLEDGE:
        score = 0.0
        if re.search(rf"\b{re.escape(item['id'])}\b", q) or re.search(rf"\b{re.escape(item['label'].lower())}\b", q):
            score += 5.0
        for trigger in item["triggers"]:
            if re.search(rf"\b{re.escape(trigger)}\b", q):
                score += 3.2 if " " in trigger else 1.6
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    if not scored:
        return []
    top = scored[0][0]
    hits = []
    for score, item in scored[:limit]:
        if score < top * 0.45:
            continue
        hits.append(
            {
                "id": item["id"],
                "label": item["label"],
                "facts": item["facts"],
                "score": round(score, 2),
            }
        )
    return hits


def looks_unsupported(query: str) -> bool:
    q = query.lower()
    return any(phrase in q for phrase in UNSUPPORTED_INTENTS)


def local_answer(query: str, hits: list[dict[str, Any]]) -> tuple[str, str]:
    """Deterministic grounded fallback if no LLM key is configured."""
    if looks_unsupported(query) or not hits:
        return (
            "That specific detail is not in the supplied campus data, so I will not invent it. "
            "I can guide you using the official sample information for academics, examinations, "
            "placements, hostel, library, administration, attendance, events, and campus facilities. "
            "For personal dates, fee balances, or unpublished numbers, please use official university channels and the student portal.",
            "unavailable",
        )

    top = hits[0]
    facts = " ".join(top["facts"])
    label = top["label"]

    if top["id"] == "academics":
        text = (
            f"For academic concerns, contact your faculty advisor - that is the path given in the campus sample data. {facts}"
        )
    elif top["id"] == "examinations":
        text = (
            "Examination timetables and notifications are published through official university channels. "
            "I do not have a personal exam date in this dataset."
        )
    elif top["id"] == "placements":
        text = (
            "Reach the Placement Department for training and placement-related information. "
            f"{facts}"
        )
    elif top["id"] == "hostel":
        text = (
            "Hostel-related complaints should be submitted to the Hostel Administration. "
            f"{facts}"
        )
    elif top["id"] == "library":
        text = (
            "You may access library resources according to the library's timings and regulations. "
            "Exact opening hours are not included in the sample data."
        )
    elif top["id"] == "administration":
        text = (
            "For certificates and student records, contact the respective administrative office. "
            f"{facts}"
        )
    elif top["id"] == "attendance":
        text = (
            "Follow the minimum attendance requirement prescribed by university regulations. "
            "A numeric cutoff is not provided in the sample information."
        )
    elif top["id"] == "events":
        text = (
            "University event announcements are shared through official communication channels. "
            f"{facts}"
        )
    elif top["id"] == "about":
        text = (
            f"Presidency University overview: {facts}"
        )
    elif top["id"] == "campus":
        text = (
            f"Presidency University campus facilities: {facts}"
        )
    else:
        text = facts

    return (text, label)


def _groq_chat(query: str, api_key: str) -> str:
    payload = {
        "model": os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        "temperature": 0.2,
        "max_tokens": 280,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT.format(knowledge=knowledge_block())},
            {"role": "user", "content": query},
        ],
    }
    with httpx.Client(timeout=25) as client:
        response = client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()


def _gemini_chat(query: str, api_key: str) -> str:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')}:generateContent"
    )
    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT.format(knowledge=knowledge_block())}]},
        "contents": [{"role": "user", "parts": [{"text": query}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 280},
    }
    with httpx.Client(timeout=25) as client:
        response = client.post(url, params={"key": api_key}, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def _openai_chat(query: str, api_key: str) -> str:
    payload = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "temperature": 0.2,
        "max_tokens": 280,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT.format(knowledge=knowledge_block())},
            {"role": "user", "content": query},
        ],
    }
    with httpx.Client(timeout=25) as client:
        response = client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()


def answer(query: str, runtime_key: dict[str, str] | None = None) -> dict[str, Any]:
    query = (query or "").strip()
    if not query:
        return {
            "ok": False,
            "error": "Ask a campus question to begin.",
            "answer": "The console is waiting for a question.",
            "sources": [],
            "model": None,
            "grounded": True,
        }

    hits = retrieve(query)
    groq = (runtime_key or {}).get("groq") or os.getenv("GROQ_API_KEY")
    gemini = (runtime_key or {}).get("gemini") or os.getenv("GEMINI_API_KEY")
    openai = (runtime_key or {}).get("openai") or os.getenv("OPENAI_API_KEY")

    model_used = "campus-nexus-grounded-retriever"
    text = None
    unsupported = looks_unsupported(query) or not hits

    try:
        if unsupported:
            pass
        elif groq:
            text = _groq_chat(query, groq)
            model_used = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant") + " (Groq)"
        elif gemini:
            text = _gemini_chat(query, gemini)
            model_used = os.getenv("GEMINI_MODEL", "gemini-2.0-flash") + " (Gemini)"
        elif openai:
            text = _openai_chat(query, openai)
            model_used = os.getenv("OPENAI_MODEL", "gpt-4o-mini") + " (OpenAI)"
    except Exception:
        text = None

    if not text:
        text, _ = local_answer(query, hits)
        if (groq or gemini or openai) and not unsupported:
            text += "\n\n(Live model call failed, so this answer used the grounded fallback engine.)"

    status = "grounded" if hits and not looks_unsupported(query) else "unavailable"
    return {
        "ok": True,
        "answer": text,
        "sources": hits,
        "model": model_used,
        "status": status,
        "grounded": True,
    }
