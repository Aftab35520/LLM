from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(data: ChatRequest):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ FIXED
        messages=[{"role": "user", "content": data.prompt}],
    )
    return {"answer": res.choices[0].message.content}
