from enum import Enum

class ScrapePageBodyFormatItem(str, Enum):
    HTML = "html"
    JSON = "json"
    MARKDOWN = "markdown"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
