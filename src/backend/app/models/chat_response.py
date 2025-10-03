from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class ChatResponse:
    role: str
    content_type: str
    content: Any
    history: Optional[List[Dict[str, str]]] = None
