import sqlite3


def get_connection(database_path):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    return connection


def initialise_database(database_path):
    connection = get_connection(database_path)

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            subject TEXT NOT NULL,
            confidence INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    connection.commit()
    connection.close()