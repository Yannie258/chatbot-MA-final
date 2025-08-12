from fastapi import FastAPI
from models.schemas import ChatInput, ChatResponse
from services.llm_client import generate_response
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
