from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.chat_response import ChatResponse
from models.chat_input import ChatInput
from chatbot.llm_client import generate_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chatbot", response_model=ChatResponse)
def chat(input: ChatInput):
    """Generic dispatcher endpoint (uses input.strategy if provided)"""
    return generate_response(input.message, input.strategy or "plain")

# -----------------------
# Baseline endpoint (Version A)
# -----------------------
@app.post("/chatbot/plain", response_model=ChatResponse)
def chat_plain(input: ChatInput):
    """Return plain text baseline (no structured output)."""
    return generate_response(input.message, strategy="plain")

# ---------------------------
# Structured endpoint (Version B)
# ---------------------------
@app.post("/chatbot/structured", response_model=ChatResponse)
def chat_structured(input: ChatInput):
    """Return structured output."""
    return generate_response(input.message, strategy="function")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
