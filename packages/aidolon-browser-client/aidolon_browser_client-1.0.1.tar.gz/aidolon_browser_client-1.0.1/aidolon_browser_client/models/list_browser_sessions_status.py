from enum import Enum

class ListBrowserSessionsStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"

    def __str__(self) -> str:
        return str(self.value)
