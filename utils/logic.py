# logic/logic.py

import json
from pathlib import Path

CHAPTERS_PATH = Path(__file__).parent.parent / "data" / "chapters.json"

def check_answer(correct_index: int, selected_index: int) -> bool:
    """Checks if the selected answer matches the correct one."""
    return selected_index == correct_index


def get_next_level(current_level: dict) -> dict | None:
    """
    Gets the next level from chapter + level index.
    If it's the last level of the last chapter, returns None.
    
    current_level: { "chapter": int, "level": int }
    """
    chapter_index = current_level["chapter"]
    level_index = current_level["level"]

    # Load chapter index
    try:
        with open(CHAPTERS_PATH, "r", encoding="utf-8") as f:
            chapters_data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load chapters.json: {e}")
        return None

    chapters = chapters_data.get("chapters", [])
    if chapter_index >= len(chapters):
        print("❌ Invalid chapter index")
        return None

    current_chapter = chapters[chapter_index]
    chapter_file = Path(__file__).parent.parent / current_chapter["file"]

    try:
        with open(chapter_file, "r", encoding="utf-8") as f:
            chapter_levels = json.load(f)["levels"]
    except Exception as e:
        print(f"❌ Failed to load chapter levels: {e}")
        return None

    # Go to next level in same chapter
    if level_index + 1 < len(chapter_levels):
        return {"chapter": chapter_index, "level": level_index + 1}

    # Otherwise, go to next chapter
    if chapter_index + 1 < len(chapters):
        return {"chapter": chapter_index + 1, "level": 0}

    # No more levels
    return None
