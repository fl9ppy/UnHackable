# database/db.py

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "database.db"

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

def create_user(username: str, password: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password) VALUES (?, ?)
            ''', (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def login_user(username: str, password: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM users WHERE username = ? AND password = ?
        ''', (username, password))
        return cursor.fetchone() is not None

def get_user_progress(user_id: int) -> dict:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT chapter_id, level_id, score
            FROM progress
            WHERE user_id = ?
        ''', (user_id,))
        rows = cursor.fetchall()

        progress = {}
        for chapter_id, level_id, score in rows:
            if chapter_id not in progress:
                progress[chapter_id] = {}
            progress[chapter_id][level_id] = score

        return progress

def grant_xp(user_id: int, amount: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO xp (user_id, total_xp) VALUES (?, 0)
        ''', (user_id,))
        cursor.execute('''
            UPDATE xp SET total_xp = total_xp + ? WHERE user_id = ?
        ''', (amount, user_id))
        conn.commit()

def get_user_xp(user_id: int) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT total_xp FROM xp WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 0

def award_badge(user_id: int, badge_name: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO badges (user_id, badge_name)
            VALUES (?, ?)
        ''', (user_id, badge_name))
        conn.commit()

def get_user_badges(user_id: int) -> list:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT badge_name FROM badges WHERE user_id = ?', (user_id,))
        return [row[0] for row in cursor.fetchall()]

def save_user_progress(user_id: int, chapter_id: int, level_id: int, score: int = 1):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Check if this user has already completed this level
        cursor.execute('''
            SELECT score FROM progress
            WHERE user_id = ? AND chapter_id = ? AND level_id = ?
        ''', (user_id, chapter_id, level_id))

        result = cursor.fetchone()
        if result:
            # Already completed → do not update again
            return

        # First time → save it
        cursor.execute('''
            INSERT INTO progress (user_id, chapter_id, level_id, score)
            VALUES (?, ?, ?, ?)
        ''', (user_id, chapter_id, level_id, score))
        conn.commit()

def get_user_id(username: str) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        return row[0] if row else -1

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
