# data_interface.py

import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "chapters.json"

def load_chapters() -> dict:
    """Parses and returns all chapters and levels as a dictionary."""
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading chapters: {e}")
        return {}

