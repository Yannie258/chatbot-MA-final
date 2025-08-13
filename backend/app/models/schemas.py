from pydantic import BaseModel
from typing import Union, Dict
from typing import Union, Dict
from .strategy import OutputFormat  # import  Enum

class ChatInput(BaseModel):
    message: str
    strategy: str
    #strategy: OutputFormat = OutputFormat.PLAIN  # default strategy is plain text

class ChatResponse(BaseModel):
    role: str = "bot"
    content_type: str = 'plain'  # default is plain text when user does not set in setting
    content: Union[str, Dict]
