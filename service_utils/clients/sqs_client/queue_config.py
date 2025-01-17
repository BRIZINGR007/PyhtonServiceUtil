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


class QUEUE_NAMES:
    EMBEDDING_SERVICE = "embedding-service"
    EVALUATION_SERVICE = "evaluation-service"


QUEUE_CONFIG: Dict[str, Dict[str, bool]] = {
    QUEUE_NAMES.EMBEDDING_SERVICE: dict(fifo=False),
    QUEUE_NAMES.EVALUATION_SERVICE: dict(fifo=False),
}
