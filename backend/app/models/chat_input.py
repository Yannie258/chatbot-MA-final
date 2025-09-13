from pydantic import BaseModel

class ChatInput(BaseModel):
    message: str
    strategy: str | None = None   # optional because /plain and /structured set it
