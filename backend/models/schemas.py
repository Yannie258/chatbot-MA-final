from pydantic import BaseModel
from typing import Union, Dict

class ChatInput(BaseModel):
    message: str

class ChatResponse(BaseModel):
    role: str = "bot"
    content_type: str  # "text", "card", "markdown", "html"
    content: Union[str, Dict]
