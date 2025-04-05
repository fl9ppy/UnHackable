# data_interface.py
import json
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
