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
    EMAIL_SERVICE = "app001emailservice"


QUEUE_CONFIG: Dict[str, Dict[str, bool]] = {
    QUEUE_NAMES.EMAIL_SERVICE: dict(fifo=False),
}
