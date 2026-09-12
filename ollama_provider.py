import os
import requests

def call_ollama(model: str, messages: list[dict]) -> str:
    """Send a chat completion request to Ollama.
    The payload follows the OpenAI chat completion schema.
    Returns the assistant's reply text or raises on error.
    """
    base_url = os.getenv("OLLAMA_BASE_URL", "http://192.168.18.218:11434")
    url = f"{base_url}/v1/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.1,
    }
    try:
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise RuntimeError(f"Ollama request failed: {e}")

