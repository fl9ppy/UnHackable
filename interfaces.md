📄 interfaces.md

🔌 Shared Function Contracts

These are the standardized interfaces that all developers must follow to ensure smooth integration between backend, UI, and game logic. All implementations (real or mock) must respect these signatures.

🧠 User Authentication

login_user(username: str, password: str) -> bool

✅ Returns True if login is successful.

create_user(username: str, password: str) -> bool

✅ Returns True if account is created. False if username exists.

🧾 Progress Tracking

get_user_progress(user_id: int) -> dict

✅ Returns user's chapter-level progress in this format:

{
  1: {0: 1, 1: 1},  # Chapter 1, Level 0 and 1 complete
  2: {0: 1}         # Chapter 2, Level 0 complete
}

📚 Content Loading

load_chapters() -> dict

✅ Loads all chapter metadata and level info from JSON files.

🎮 Game Logic

check_answer(correct_index: int, selected_index: int) -> bool

✅ Returns True if the user's answer is correct.

get_next_level(current_level: dict) -> dict

✅ Given a current level, returns the next level:

{
  "chapter_id": 2,
  "level_id": 0
}

🏅 XP & Gamification (Backend Only)

calculate_xp(event_type: str) -> int

✅ Returns XP value for the event.

grant_xp(user_id: int, amount: int)

✅ Adds XP to the user.

get_user_xp(user_id: int) -> int

✅ Returns total XP.

award_badge(user_id: int, badge_name: str)

✅ Grants a badge.

get_user_badges(user_id: int) -> list[str]

✅ Returns list of badge names earned.

🧪 Development Guidelines

Use mock_backend.py for UI and game logic development

All data flows through these shared interfaces

Real implementation is only integrated at the end

Happy Hacking 🌶️
