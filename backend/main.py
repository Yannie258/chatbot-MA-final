from fastapi import FastAPI
from models.schemas import ChatInput, ChatResponse
from services.llm_client import generate_response

app = FastAPI()

@app.post("/chatbot", response_model=ChatResponse)
def chat(input: ChatInput):
    return generate_response(input.message)
