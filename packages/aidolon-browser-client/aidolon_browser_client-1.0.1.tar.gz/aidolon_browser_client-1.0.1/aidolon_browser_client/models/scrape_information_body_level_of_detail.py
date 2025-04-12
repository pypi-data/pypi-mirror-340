from enum import Enum

class ScrapeInformationBodyLevelOfDetail(str, Enum):
    BRIEF = "brief"
    FULL = "full"
    STANDARD = "standard"

    def __str__(self) -> str:
        return str(self.value)
