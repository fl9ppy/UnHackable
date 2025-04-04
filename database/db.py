# database/db.py

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "unhackable.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # XP table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS xp (
                user_id INTEGER,
                total_xp INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                user_id INTEGER,
                chapter_id INTEGER,
                level_id INTEGER,
                score INTEGER,
                PRIMARY KEY (user_id, chapter_id, level_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Badges table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS badges (
                user_id INTEGER,
                badge_name TEXT,
                PRIMARY KEY (user_id, badge_name),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()

# Call this manually once during setup
if __name__ == "__main__":
    init_db()
    print("✅ Database initialized.")

