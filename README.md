# StudySpark

StudySpark is a web-based study notes and flashcards manager
developed for the COM6036 Digital Innovation prototype.

## Architecture

The application uses an N-tier structure:

1. Presentation layer
   - Flask routes
   - HTML/Jinja templates
   - CSS

2. Business logic layer
   - services.py
   - Validation
   - Application rules

3. Data layer
   - repository.py
   - database.py
   - SQLite

## Features

- Create study notes
- Search notes
- Delete notes
- Create flashcards
- Reveal flashcard answers
- Record confidence ratings
- Delete flashcards
- Dashboard statistics
- Responsive interface
- Server-side validation
- Parameterised SQL queries

## Installation

Create a Python virtual environment:

```bash
python3 -m venv .venv