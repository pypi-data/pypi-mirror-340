from enum import Enum

class PressKeyBodyWait(str, Enum):
    AUTO = "auto"
    NAVIGATION = "navigation"
    NETWORK = "network"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
