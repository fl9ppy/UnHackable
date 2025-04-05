# utils/gamification.py

from database.db import get_connection

# XP rules for gamification events
XP_RULES = {
    "lesson_complete": 50,
    "quiz_correct": 10,
    "quiz_wrong": 2,
    "streak_bonus": 30,
    "master_pass": 100
}

def calculate_xp(event_type: str) -> int:
    """Returns the XP earned for a specific event type."""
    return XP_RULES.get(event_type, 0)

def grant_xp(user_id: int, amount: int):
    """Adds XP to the user's total."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Insert row if not exists
        cursor.execute('''
            INSERT OR IGNORE INTO xp (user_id, total_xp)
            VALUES (?, 0)
        ''', (user_id,))

        # Update XP
        cursor.execute('''
            UPDATE xp SET total_xp = total_xp + ?
            WHERE user_id = ?
        ''', (amount, user_id))

        conn.commit()

def get_user_xp(user_id: int) -> int:
    """Fetches current XP for the user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT total_xp FROM xp WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 0

def award_badge(user_id: int, badge_name: str):
    """Awards a new badge to the user (ignores duplicates)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO badges (user_id, badge_name)
            VALUES (?, ?)
        ''', (user_id, badge_name))
        conn.commit()

def get_user_badges(user_id: int) -> list:
    """Returns a list of all badges earned by the user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT badge_name FROM badges WHERE user_id = ?', (user_id,))
        return [row[0] for row in cursor.fetchall()]
