from pydantic import BaseModel
from typing import Union, Dict, Optional

class ChatInput(BaseModel):
    message: str
    strategy: Optional[str] = None  # user can choose strategy or not
    #strategy: OutputFormat = OutputFormat.PLAIN  # default strategy is plain text

class ChatResponse(BaseModel):
    role: str = "bot"
    content_type: str = 'plain'  # default is plain text when user does not set in setting
    content: Union[str, Dict]
