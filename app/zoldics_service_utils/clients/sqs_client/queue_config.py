from enum import StrEnum
from typing import Dict

"""
Configuration:
- When running locally, mock the queue names in a .env file.

Example:
<env>
embedding-service=yourname-embedding-service
evaluation-service=yourname-evaluation-service
</env>
"""


class QUEUE_NAMES(StrEnum):
    APP_001_AI_SERVICE = "app001-ai-service"
    APP_001_AI_DUB_LAMBDA = "app001-ai-dub-lambda"


QUEUE_CONFIG: Dict[str, Dict[str, bool]] = {
    QUEUE_NAMES.APP_001_AI_SERVICE: dict(fifo=False),
    QUEUE_NAMES.APP_001_AI_DUB_LAMBDA: dict(fifo=True),
}
