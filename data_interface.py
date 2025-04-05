# data_interface.py
import json
import os
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "chapters.json"

def load_chapters() -> dict:
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"[DEBUG] Loaded chapters.json: {data}")  # TEMP
            return data
    except Exception as e:
        print(f"❌ Error loading chapters.json: {e}")
        return {}

def load_level_data(chapter_file: str) -> dict:
    if not os.path.exists(chapter_file):
        raise FileNotFoundError(f"[ERROR] Chapter file not found: {chapter_file}")

    with open(chapter_file, encoding="utf-8") as f:
        return json.load(f)
