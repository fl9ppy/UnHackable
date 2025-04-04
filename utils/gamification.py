# UnHackable/utils/gamification.py

# This module handles XP calculation, level-up logic, badges, and stats

XP_THRESHOLDS = [0, 50, 150, 300, 500, 750, 1050]  # XP needed for each level-up

BADGES = {
    "first_correct": "First Pepper Pop!",
    "perfect_lesson": "Lesson Master",
    "streak_5": "Spicy Streak!",
    # Add more badges here
}

def calculate_xp_gain(event_type: str) -> int:
    """Return XP based on the event type."""
    xp_map = {
        "lesson_complete": 20,
        "quiz_correct": 10,
        "quiz_incorrect": 2,
        "streak_bonus": 15,
    }
    return xp_map.get(event_type, 0)

def check_level_up(current_xp: int, new_xp: int) -> bool:
    """Returns True if user levels up after gaining XP."""
    old_level = get_level_from_xp(current_xp)
    new_level = get_level_from_xp(new_xp)
    return new_level > old_level

def get_level_from_xp(xp: int) -> int:
    """Determine level based on total XP."""
    level = 0
    for threshold in XP_THRESHOLDS:
        if xp >= threshold:
            level += 1
        else:
            break
    return level

def award_badge(user_data: dict, event: str) -> str | None:
    """Returns badge name if new badge is awarded, else None."""
    awarded = user_data.get("badges", [])
    if event in BADGES and event not in awarded:
        return BADGES[event]
    return None

def get_user_stats(user_id: int) -> dict:
    """
    Placeholder function – to be connected to DB.
    Returns a dict with user XP, level, and badges.
    """
    # Replace with real DB logic later
    return {
        "user_id": user_id,
        "xp": 120,
        "level": get_level_from_xp(120),
        "badges": ["first_correct"]
    }

