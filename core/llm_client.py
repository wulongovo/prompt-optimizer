"""Ollama LLM客户端"""
import requests

OLLAMA_BASE = "http://localhost:11434"
MODEL = "qwen2.5"

def chat(messages, temperature=0.3, max_tokens=2000):
    try:
        r = requests.post(f"{OLLAMA_BASE}/api/chat", json={
            "model": MODEL, "messages": messages, "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens}
        }, timeout=120)
        r.raise_for_status()
        return r.json()["message"]["content"]
    except Exception as e:
        return f"LLM调用失败: {e}"

def generate(prompt, system="", temperature=0.3):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return chat(messages, temperature)
