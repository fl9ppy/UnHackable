# mock_backend.py

def login_user(username, password) -> bool:
    print(f"[MOCK] login_user({username}, {password})")
    return username == "test" and password == "1234"

def create_user(username, password) -> bool:
    print(f"[MOCK] create_user({username}, {password})")
    return True

def get_user_progress(user_id) -> dict:
    print(f"[MOCK] get_user_progress({user_id})")
    return {
        1: {0: 1, 1: 1},  # Chapter 1, levels 0 and 1 complete
        2: {0: 1}         # Chapter 2, level 0 complete
    }

def load_chapters() -> dict:
    print("[MOCK] load_chapters()")
    return {
        "chapters": [
            {
                "title": "Intro to Phishing",
                "lessons": [
                    {"type": "lesson", "title": "What is phishing?"},
                    {"type": "quiz", "question": "Phishing is…", "options": ["A scam", "A fish"], "answer": 0}
                ]
            }
        ]
    }

def check_answer(correct_index, selected_index) -> bool:
    print(f"[MOCK] check_answer({correct_index}, {selected_index})")
    return correct_index == selected_index

def get_next_level(current_level) -> dict:
    print(f"[MOCK] get_next_level({current_level})")
    return {"chapter_id": 1, "level_id": 1}

