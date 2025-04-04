import sqlite3
from pathlib import Path

# Path to your database file (stored inside /cyberlingo/database/)
DB_PATH = Path(__file__).parent / "cyberlingo.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # USERS table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # PROGRESS table
    c.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chapter_id TEXT NOT NULL,
            level_id TEXT NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # XP table
    c.execute('''
        CREATE TABLE IF NOT EXISTS xp (
            user_id INTEGER PRIMARY KEY,
            xp_amount INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


# -----------------------------
# Placeholder Logic Functions
# -----------------------------
def update_user_xp(user_id, amount):
    pass  # To be implemented

def get_user_progress(user_id):
    pass  # To be implemented

def save_progress(user_id, chapter_id, level_id):
    pass  # To be implemented
