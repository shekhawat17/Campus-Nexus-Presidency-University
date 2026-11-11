"""Official sample campus knowledge for TECHNOPIA 2.0.

Do not add invented regulations, dates, or contact details.
"""

from __future__ import annotations

KNOWLEDGE = [
    {
        "id": "academics",
        "label": "Academics",
        "icon": "◈",
        "summary": "Students may contact their faculty advisor for academic-related assistance.",
        "facts": [
            "Students may contact their faculty advisor for academic-related assistance.",
        ],
        "triggers": [
            "academic",
            "academics",
            "faculty advisor",
            "advisor",
            "subject",
            "course",
            "syllabus",
            "mentor",
            "faculty",
            "study problem",
            "academic problem",
            "academic help",
        ],
    },
    {
        "id": "attendance",
        "label": "Attendance",
        "icon": "◉",
        "summary": "Students should follow the minimum attendance requirement prescribed by university regulations.",
        "facts": [
            "Students should follow the minimum attendance requirement prescribed by university regulations.",
        ],
        "triggers": [
            "attendance",
            "minimum attendance",
            "present",
            "shortage",
            "bunk",
            "absent",
        ],
    },
    {
        "id": "examinations",
        "label": "Examinations",
        "icon": "▣",
        "summary": "Examination timetables and notifications are published through official university channels.",
        "facts": [
            "Examination timetables and notifications are published through official university channels.",
        ],
        "triggers": [
            "exam",
            "exams",
            "examination",
            "timetable",
            "time table",
            "schedule",
            "notification",
            "hall ticket",
            "results",
        ],
    },
    {
        "id": "placements",
        "label": "Placements",
        "icon": "◇",
        "summary": "Students may contact the Placement Department for training and placement-related information.",
        "facts": [
            "Students may contact the Placement Department for training and placement-related information.",
        ],
        "triggers": [
            "placement",
            "placements",
            "training",
            "internship",
            "job",
            "recruit",
            "company",
            "career",
            "placement department",
        ],
    },
    {
        "id": "library",
        "label": "Library",
        "icon": "▤",
        "summary": "Students may access library resources according to the library's timings and regulations.",
        "facts": [
            "Students may access library resources according to the library's timings and regulations.",
        ],
        "triggers": [
            "library",
            "book",
            "books",
            "journal",
            "reading",
            "library timing",
            "library hours",
        ],
    },
    {
        "id": "hostel",
        "label": "Hostel",
        "icon": "⌂",
        "summary": "Hostel-related complaints should be submitted to the Hostel Administration.",
        "facts": [
            "Hostel-related complaints should be submitted to the Hostel Administration.",
        ],
        "triggers": [
            "hostel",
            "complaint",
            "mess",
            "room",
            "warden",
            "hostel administration",
        ],
    },
    {
        "id": "administration",
        "label": "Administration",
        "icon": "⬡",
        "summary": "Students may contact the respective administrative office for certificates and student records.",
        "facts": [
            "Students may contact the respective administrative office for certificates and student records.",
        ],
        "triggers": [
            "admin",
            "administration",
            "certificate",
            "bonafide",
            "transcript",
            "records",
            "student records",
            "office",
            "tc",
            "document",
        ],
    },
    {
        "id": "events",
        "label": "Events",
        "icon": "✦",
        "summary": "University event announcements are shared through official communication channels.",
        "facts": [
            "University event announcements are shared through official communication channels.",
        ],
        "triggers": [
            "event",
            "events",
            "fest",
            "technopia",
            "announcement",
            "workshop",
            "seminar",
        ],
    },
]

UNSUPPORTED_INTENTS = [
    "exact date",
    "specific date",
    "my next exam",
    "when is my exam",
    "what time",
    "phone number",
    "email id",
    "room number",
    "fee amount",
    "how much",
    "cutoff",
    "marks",
    "personal",
]


def knowledge_block() -> str:
    lines = []
    for item in KNOWLEDGE:
        lines.append(f"- {item['label']}: {' '.join(item['facts'])}")
    return "\n".join(lines)


def public_catalog() -> list[dict]:
    return [
        {
            "id": item["id"],
            "label": item["label"],
            "icon": item["icon"],
            "summary": item["summary"],
        }
        for item in KNOWLEDGE
    ]
