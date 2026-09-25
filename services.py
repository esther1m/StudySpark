# Business logic layer
# Handles validation and application rules before data is passed to the repository layer
class StudyService:

    def __init__(self, repository):
        self.repository = repository

    def get_notes(self):
        return self.repository.get_notes()

    def search_notes(self, search_term):
        if not search_term.strip():
            return self.get_notes()

        return self.repository.search_notes(
            search_term.strip()
        )

    def create_note(self, title, subject, content):
        title = title.strip()
        subject = subject.strip()
        content = content.strip()

        # Validate user input in the business layer before it reaches the database layer.
        if not title:
            return False, "A note title is required."

        if not subject:
            return False, "A subject is required."

        if not content:
            return False, "Note must include content"

        if len(title) > 100:
            return False, "The title must be less than 100 characters"

        self.repository.create_note(
            title,
            subject,
            content
        )

        return True, "Note created successfully."

    def delete_note(self, note_id):
        self.repository.delete_note(note_id)

    def get_flashcards(self):
        return self.repository.get_flashcards()

    def create_flashcard(
        self,
        question,
        answer,
        subject
    ):
        question = question.strip()
        answer = answer.strip()
        subject = subject.strip()

        if not question:
            return False, "A question is required."

        if not answer:
            return False, "An answer is required."

        if not subject:
            return False, "A subject is required."

        self.repository.create_flashcard(
            question,
            answer,
            subject
        )

        return True, "Flashcard created successfully."

    def update_flashcard_confidence(
        self,
        flashcard_id,
        confidence
    ):
        if confidence not in (1, 2, 3):
            return False, "Confidence must be between 1 and 3."

        self.repository.update_flashcard_confidence(
            flashcard_id,
            confidence
        )

        return True, "Confidence rating updated."

    def delete_flashcard(self, flashcard_id):
        self.repository.delete_flashcard(
            flashcard_id
        )

    def get_statistics(self):
        return {
            "notes": self.repository.count_notes(),
            "flashcards": self.repository.count_flashcards()
        }