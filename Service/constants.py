# Service/constants.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Constants:
    RETRY_COUNT: int = 5
    RETRY_DELAY: int = 30
    WEB_DELAY: int = 1
    APP_VERSION: str = "1.0.0.0"
    PROCESS_ID: str = "CAU000"
    PROCESS_NAME: str = "RPA"
