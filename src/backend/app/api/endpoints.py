from fastapi import APIRouter, HTTPException
from services.rag import RAGService
from models.schemas import ChatResponse
from typing import Optional

router = APIRouter()
rag_service = RAGService()

@router.post("/chatbot", response_model=ChatResponse)
async def chat_endpoint(
    user_message: str,
    model: Optional[str] = "gpt-4o-mini",
    temperature: Optional[float] = 0.2
):
    """
    Process user message through RAG pipeline and return chatbot response
    
    Parameters:
    - user_message: The input message from user
    - model: Which LLM model to use (default: gpt-4o-mini)
    - temperature: Creativity parameter (0-1)
    
    Returns:
    - Structured response from the chatbot
    """
    try:
        return rag_service.generate_response(
            user_message=user_message,
            model=model,
            temperature=temperature
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )

@router.post("/chatbot/plain", response_model=ChatResponse)
async def chat_plain(
    user_message: str,
    model: Optional[str] = "gpt-4o-mini",
    temperature: Optional[float] = 0.2
):
    """
    Baseline chatbot (Version A) returns plain text output
    """
    try:
        return rag_service.generate_response(
            user_message=user_message,
            strategy="plain",  
            model=model,
            temperature=temperature
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/chatbot/structured", response_model=ChatResponse)
async def chat_structured(
    user_message: str,
    model: Optional[str] = "gpt-4o-mini",
    temperature: Optional[float] = 0.2
):
    """
    Enhanced chatbot (Version B) – returns structured JSON output
    """
    try:
        return rag_service.generate_response(
            user_message=user_message,
            strategy="function",
            model=model,
            temperature=temperature
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/health")
async def health_check():
    return {"status": "healthy"}