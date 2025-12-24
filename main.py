from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

# ✅ MUST be added immediately after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://assignmentai.com",     # your real frontend
        "https://www.assignmentai.com", # if used
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
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
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": data.prompt}],
    )
    return {"answer": res.choices[0].message.content}
