from fastapi import APIRouter, HTTPException
from services.rag import RAGService
from models.schemas import ChatResponse
from typing import Optional

router = APIRouter()
rag_service = RAGService()

@router.post("/chatbot", response_model=ChatResponse)
async def chat_endpoint(
    user_message: str,
    model: Optional[str] = "gpt-3.5-turbo",
    temperature: Optional[float] = 0.2
):
    """
    Process user message through RAG pipeline and return chatbot response
    
    Parameters:
    - user_message: The input message from user
    - model: Which LLM model to use (default: gpt-3.5-turbo)
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

@router.get("/health")
async def health_check():
    return {"status": "healthy"}