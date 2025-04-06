# utils/ai_chat.py

import requests

def get_ai_response(user_input: str) -> str:
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",  # or "llama2", "codellama", etc.
            "prompt": f"You are a helpful cybersecurity assistant. Keep your answer short and spicy. User asked: {user_input}",
            "stream": False
        })
        data = response.json()
        return data.get("response", "🤖 Sorry, no response received.")
    except Exception as e:
        return f"❌ AI error: {e}"
