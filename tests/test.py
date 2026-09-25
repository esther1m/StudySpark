import os
import tempfile
import unittest

from app import create_app


class StudySparkTestCase(unittest.TestCase):

    def setUp(self):
        database_file = tempfile.NamedTemporaryFile(
            delete=False
        )

        database_file.close()

        self.database_path = database_file.name

        self.app = create_app(
            {
                "TESTING": True,
                "DATABASE": self.database_path,
                "SECRET_KEY": "test-key"
            }
        )

        self.client = self.app.test_client()

    def tearDown(self):
        os.unlink(self.database_path)

    def test_home_loads(self):
        response = self.client.get("/")

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            b"StudySpark",
            response.data
        )

    def test_note_create_and_validation(self):
        invalid_response = self.client.post(
            "/notes/add",
            data={
                "title": "",
                "subject": "Computing",
                "content": "Test content"
            },
            follow_redirects=True
        )

        self.assertIn(
            b"A note title is required.",
            invalid_response.data
        )

        valid_response = self.client.post(
            "/notes/add",
            data={
                "title": "Distributed Systems",
                "subject": "Computing",
                "content": "Presentation, business and data layers."
            },
            follow_redirects=True
        )

        self.assertEqual(
            valid_response.status_code,
            200
        )

        self.assertIn(
            b"Distributed Systems",
            valid_response.data
        )

    def test_flashcard_create_and_rate(self):
        response = self.client.post(
            "/flashcards/add",
            data={
                "question": "What is an N-tier architecture?",
                "answer": "A system separated into logical layers.",
                "subject": "Computing"
            },
            follow_redirects=True
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            b"What is an N-tier architecture?",
            response.data
        )

        rating_response = self.client.post(
            "/flashcards/1/confidence",
            data={
                "confidence": "3"
            },
            follow_redirects=True
        )

        self.assertEqual(
            rating_response.status_code,
            200
        )

        self.assertIn(
            b"Current confidence:",
            rating_response.data
        )

    def test_injection_strings_are_escaped_and_db_survives(self):
        malicious_input = (
            "<script>alert('x')</script>'; "
            "DROP TABLE notes; --"
        )

        response = self.client.post(
            "/notes/add",
            data={
                "title": malicious_input,
                "subject": "Security",
                "content": "Parameterised query test."
            },
            follow_redirects=True
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertNotIn(
            b"<script>alert('x')</script>",
            response.data
        )

        second_response = self.client.post(
            "/notes/add",
            data={
                "title": "Database still works",
                "subject": "Security",
                "content": "The notes table remains available."
            },
            follow_redirects=True
        )

        self.assertEqual(
            second_response.status_code,
            200
        )

        self.assertIn(
            b"Database still works",
            second_response.data
        )


if __name__ == "__main__":
    unittest.main()