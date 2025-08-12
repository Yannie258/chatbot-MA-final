from pydantic import BaseModel
from typing import Union, Dict

class ChatInput(BaseModel):
    message: str
    strategy: str

class ChatResponse(BaseModel):
    role: str = "bot"
    content_type: str = 'plain'  # default is plain text when user does not set in setting
    content: Union[str, Dict]
