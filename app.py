# Presentation layer
# Defines the Flask routes and handles requests between the user interface and the business logic layer

from flask import Flask, render_template, request, redirect, url_for, flash

from database import initialise_database
from repository import StudyRepository
from services import StudyService


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "studyspark-development-key"
    app.config["DATABASE"] = "studyspark.db"

    if test_config:
        app.config.update(test_config)

    initialise_database(app.config["DATABASE"])

    repository = StudyRepository(app.config["DATABASE"])
    service = StudyService(repository)

    @app.route("/")
    def home():
        statistics = service.get_statistics()
        recent_notes = service.get_notes()[:3]
        flashcards = service.get_flashcards()

        return render_template(
            "index.html",
            statistics=statistics,
            recent_notes=recent_notes,
            flashcards=flashcards
        )

    @app.route("/notes")
    def notes():
        search_term = request.args.get("search", "").strip()

        if search_term:
            all_notes = service.search_notes(search_term)
        else:
            all_notes = service.get_notes()

        return render_template(
            "notes.html",
            notes=all_notes,
            search_term=search_term
        )

    @app.route("/notes/add", methods=["GET", "POST"])
    def add_note():
        if request.method == "POST":
            title = request.form.get("title", "")
            subject = request.form.get("subject", "")
            content = request.form.get("content", "")

            success, message = service.create_note(
                title,
                subject,
                content
            )

            if success:
                flash(message, "success")
                return redirect(url_for("notes"))

            flash(message, "error")

        return render_template("add_note.html")

    @app.route("/notes/delete/<int:note_id>", methods=["POST"])
    def delete_note(note_id):
        service.delete_note(note_id)
        flash("Note deleted successfully.", "success")
        return redirect(url_for("notes"))

    @app.route("/flashcards")
    def flashcards():
        all_flashcards = service.get_flashcards()

        return render_template(
            "flashcards.html",
            flashcards=all_flashcards
        )

    @app.route("/flashcards/add", methods=["GET", "POST"])
    def add_flashcard():
        if request.method == "POST":
            question = request.form.get("question", "")
            answer = request.form.get("answer", "")
            subject = request.form.get("subject", "")

            success, message = service.create_flashcard(
                question,
                answer,
                subject
            )

            if success:
                flash(message, "success")
                return redirect(url_for("flashcards"))

            flash(message, "error")

        return render_template("add_flashcard.html")

    @app.route(
        "/flashcards/<int:flashcard_id>/confidence",
        methods=["POST"]
    )
    def update_confidence(flashcard_id):
        confidence = request.form.get("confidence", type=int)

        success, message = service.update_flashcard_confidence(
            flashcard_id,
            confidence
        )

        flash(
            message,
            "success" if success else "error"
        )

        return redirect(url_for("flashcards"))

    @app.route(
        "/flashcards/delete/<int:flashcard_id>",
        methods=["POST"]
    )
    def delete_flashcard(flashcard_id):
        service.delete_flashcard(flashcard_id)
        flash("Flashcard deleted successfully.", "success")

        return redirect(url_for("flashcards"))

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)