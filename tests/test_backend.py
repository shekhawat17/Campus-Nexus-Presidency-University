import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

for k in ("GROQ_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY"):
    os.environ.pop(k, None)

import app as appmod


class BackendTests(unittest.TestCase):
    def setUp(self):
        appmod._hits.clear()
        self.c = appmod.app.test_client()

    def ask(self, q):
        return self.c.post("/api/ask", json={"query": q}).get_json()

    def test_home_page(self):
        res = self.c.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"CAMPUS NEXUS", res.data)
        self.assertIn(b"Presidency", res.data)

    def test_health_and_catalog(self):
        health = self.c.get("/api/health").get_json()
        self.assertTrue(health["ok"])
        self.assertEqual(health["service"], "campus-nexus")

        catalog = self.c.get("/api/catalog").get_json()
        self.assertIn("domains", catalog)
        self.assertGreaterEqual(len(catalog["domains"]), 8)

    def test_presidency_probes(self):
        cases = {
            "Whom should I contact for academic problems?": "academics",
            "Where can I find the examination timetable?": "examinations",
            "Whom should I contact for placement training?": "placements",
            "How can I raise a hostel complaint?": "hostel",
            "Tell me about Presidency University": "about",
            "What is the minimum attendance requirement?": "attendance",
            "What library resources are available?": "library",
            "How do I get a bonafide certificate?": "administration",
            "What event announcements are made?": "events",
            "What facilities are available on campus?": "campus",
        }
        for q, src in cases.items():
            r = self.ask(q)
            self.assertEqual(r["status"], "grounded", f"Failed for query: {q}")
            self.assertEqual(r["sources"][0]["id"], src, f"Expected {src} for: {q}")

    def test_unknown_not_invented(self):
        unsupported_queries = [
            "What is the exact date of my next examination?",
            "What is my exam date?",
            "What is the hostel fee?",
            "What is the registrar's phone number?",
            "What time does the library close?",
            "What is my marks and CGPA?",
        ]
        for q in unsupported_queries:
            r = self.ask(q)
            self.assertEqual(r["status"], "unavailable", f"Should be unavailable: {q}")
            self.assertIn("not in the supplied campus data", r["answer"])

    def test_no_substring_false_match(self):
        # 'tc' in match or 'room' in bathroom should not trigger administration/hostel unless intended
        self.assertEqual(self.ask("does this match anything")["sources"], [])

    def test_validation(self):
        self.assertEqual(self.c.post("/api/ask", json={}).status_code, 400)
        self.assertEqual(self.c.post("/api/ask", json={"query": "   "}).status_code, 400)
        self.assertEqual(self.c.post("/api/ask", json={"query": "a" * 501}).status_code, 400)
        self.assertEqual(self.c.get("/nonexistent-endpoint").status_code, 404)

    def test_rate_limit(self):
        appmod.RATE_LIMIT = 3
        codes = [self.c.post("/api/ask", json={"query": "hostel"}).status_code for _ in range(5)]
        appmod.RATE_LIMIT = 30
        self.assertEqual(codes[-1], 429)


if __name__ == "__main__":
    unittest.main()
