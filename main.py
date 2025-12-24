from fastapi import FastAPI
import requests
import os

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = os.getenv("MODEL_NAME", "phi")

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(prompt: str):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload)
    return r.json()
