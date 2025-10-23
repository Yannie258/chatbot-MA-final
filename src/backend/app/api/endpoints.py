import json
import logging
from fastapi import APIRouter, HTTPException
from models.chat_input import ChatInput        
from models.chat_response import ChatResponse 
from chatbot.llm_client import generate_response 

router = APIRouter()

# ---------------------------------------------------------------------
# Unified Chat Endpoint (auto-detects strategy)
# ---------------------------------------------------------------------
@router.post("/chatbot", response_model=ChatResponse)
async def chat_endpoint(request: ChatInput):
    """
    Process user message and return chatbot response.
    Automatically uses provided strategy (default: 'plain').
    """
    try:
        logging.info("📥 INPUT DICT (/chatbot):")
        logging.info(json.dumps(request.dict(), indent=2))

        return generate_response(
            user_message=request.message,
            strategy=request.strategy or "plain",
            history=request.history
        )
    except Exception as e:
        logging.exception("❌ Error in /chatbot endpoint")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )

# ---------------------------------------------------------------------
# Plain Text Chatbot (Version A)
# ---------------------------------------------------------------------
@router.post("/chatbot/plain", response_model=ChatResponse)
async def chat_plain(request: ChatInput):
    """
    Baseline chatbot (Version A) — returns plain text output.
    """
    try:
        logging.info("INPUT DICT (/chatbot/plain):")
        logging.info(json.dumps(request.dict(), indent=2))

        return generate_response(
            user_message=request.message,
            strategy="plain",
            history=request.history
        )
    except Exception as e:
        logging.exception("Error in /chatbot/plain endpoint")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing plain chatbot request: {str(e)}"
        )

# ---------------------------------------------------------------------
# Structured Output Chatbot (Version B)
# ---------------------------------------------------------------------
@router.post("/chatbot/structured", response_model=ChatResponse)
async def chat_structured(request: ChatInput):
    """
    Enhanced chatbot (Version B) — returns structured JSON output.
    """
    try:
        logging.info("INPUT DICT (/chatbot/structured):")
        logging.info(json.dumps(request.dict(), indent=2))

        return generate_response(
            user_message=request.message,
            strategy="function",
            history=request.history
        )
    except Exception as e:
        logging.exception("Error in /chatbot/structured endpoint")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing structured chatbot request: {str(e)}"
        )

# ---------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------
@router.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy"}
