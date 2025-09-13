from dataclasses import dataclass
from typing import Any

@dataclass
class ChatResponse:
    role: str
    content_type: str
    content: Any
