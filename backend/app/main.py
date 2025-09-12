from fastapi import FastAPI
from models.schemas import ChatInput, ChatResponse
from chatbot.llm_client import generate_response, generate_response_plain, generate_response_structured
from fastapi.middleware.cors import CORSMiddleware

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
    return generate_response(input.message, input.strategy)


# -----------------------
# Baseline endpoint (Group A)
# -----------------------
@app.post("/chatbot/plain", response_model=ChatResponse)
def chat_plain(input: ChatInput):
    """Return plain text baseline (no structured output)."""
    return generate_response(input.message, strategy="plain")


# ---------------------------
# Structured endpoint (Group B)
# ---------------------------
@app.post("/chatbot/structured", response_model=ChatResponse)
def chat_structured(input: ChatInput):
    """Return structured output"""
    return generate_response(input.message, strategy="function")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
