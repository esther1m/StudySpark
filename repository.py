from database import get_connection


class StudyRepository:

    def __init__(self, database_path):
        self.database_path = database_path

    def get_notes(self):
        connection = get_connection(self.database_path)

        notes = connection.execute(
            """
            SELECT id, title, subject, content, created_at
            FROM notes
            ORDER BY created_at DESC
            """
        ).fetchall()

        connection.close()

        return notes

    def search_notes(self, search_term):
        connection = get_connection(self.database_path)

        search_pattern = f"%{search_term}%"

        notes = connection.execute(
            """
            SELECT id, title, subject, content, created_at
            FROM notes
            WHERE title LIKE ?
               OR subject LIKE ?
               OR content LIKE ?
            ORDER BY created_at DESC
            """,
            (
                search_pattern,
                search_pattern,
                search_pattern
            )
        ).fetchall()

        connection.close()

        return notes

    def create_note(self, title, subject, content):
        connection = get_connection(self.database_path)

        connection.execute(
            """
            INSERT INTO notes (title, subject, content)
            VALUES (?, ?, ?)
            """,
            (title, subject, content)
        )

        connection.commit()
        connection.close()

    def delete_note(self, note_id):
        connection = get_connection(self.database_path)

        connection.execute(
            "DELETE FROM notes WHERE id = ?",
            (note_id,)
        )

        connection.commit()
        connection.close()

    def get_flashcards(self):
        connection = get_connection(self.database_path)

        flashcards = connection.execute(
            """
            SELECT
                id,
                question,
                answer,
                subject,
                confidence,
                created_at
            FROM flashcards
            ORDER BY created_at DESC
            """
        ).fetchall()

        connection.close()

        return flashcards

    def create_flashcard(
        self,
        question,
        answer,
        subject
    ):
        connection = get_connection(self.database_path)

        connection.execute(
            """
            INSERT INTO flashcards (
                question,
                answer,
                subject
            )
            VALUES (?, ?, ?)
            """,
            (question, answer, subject)
        )

        connection.commit()
        connection.close()

    def update_flashcard_confidence(
        self,
        flashcard_id,
        confidence
    ):
        connection = get_connection(self.database_path)

        connection.execute(
            """
            UPDATE flashcards
            SET confidence = ?
            WHERE id = ?
            """,
            (confidence, flashcard_id)
        )

        connection.commit()
        connection.close()

    def delete_flashcard(self, flashcard_id):
        connection = get_connection(self.database_path)

        connection.execute(
            "DELETE FROM flashcards WHERE id = ?",
            (flashcard_id,)
        )

        connection.commit()
        connection.close()

    def count_notes(self):
        connection = get_connection(self.database_path)

        result = connection.execute(
            "SELECT COUNT(*) AS total FROM notes"
        ).fetchone()

        connection.close()

        return result["total"]

    def count_flashcards(self):
        connection = get_connection(self.database_path)

        result = connection.execute(
            "SELECT COUNT(*) AS total FROM flashcards"
        ).fetchone()

        connection.close()

        return result["total"]