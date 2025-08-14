# define enums for validation and clarification of strategy types
from enum import Enum
class OutputFormat(Enum):
    PLAIN = "plain"
    MARKDOWN = "markdown"
    JSON = "json"
    CARD = "card"
    CAROUSEL = "carousel"
    BUTTON = "button"
    LINK = "link"
    FEWSHOT = 'fewshot'