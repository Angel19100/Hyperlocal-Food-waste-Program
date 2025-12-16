import sqlite3

DATABASE_NAME = "database.db"


def get_connection():
    """Create and return a database connection"""
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    """Create database tables"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        status TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
