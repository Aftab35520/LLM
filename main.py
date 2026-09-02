from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq, RateLimitError
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

MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "qwen/qwen3.6-27b",
    "groq/compound",
    "groq/compound-mini",
]

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def health():
    return {"status": "ok"}

@app.head("/")
def health_head():
    return Response(status_code=200)

@app.post("/chat")
def chat(data: ChatRequest):
    for model in MODELS:
        try:
            res = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": data.prompt}],
            )
            return {"answer": res.choices[0].message.content}
        except RateLimitError:
            continue

    return {"answer": "All models are currently rate limited. Please try again later."}
