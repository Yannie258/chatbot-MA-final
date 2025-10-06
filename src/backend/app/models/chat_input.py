from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class HistoryMessage(BaseModel):
    role: str
    content: str

class ChatInput(BaseModel):
    message: str
    strategy: Optional[str] = "plain"
    history: List[HistoryMessage] = []