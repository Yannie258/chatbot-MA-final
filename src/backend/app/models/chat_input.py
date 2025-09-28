from typing import Dict, List
from pydantic import BaseModel

class ChatInput(BaseModel):
    message: str
    strategy: str | None = None   # optional because /plain and /structured set it
    history: List[Dict[str, str]] | None = None # chat history
