from typing import Dict, Tuple
from decouple import UndefinedValueError, config


class Helpers:
    _url_cache: Dict[Tuple[str, str, str, str], str] = {}

    @staticmethod
    def construct_queue_url(
        queue_name: str, region_name: str, params: Dict[str, bool], aws_account_id: str
    ) -> str:
        # Create a unique key for caching
        is_fifo = params.get("fifo", False)
        cache_key = (queue_name, region_name, aws_account_id, str(is_fifo))

        # Check if URL is already cached
        if cache_key in Helpers._url_cache:
            return Helpers._url_cache[cache_key]

        # Fetch environment
        try:
            __environment: str = str(config("ENVIRONMENT"))
        except UndefinedValueError:
            raise ValueError(
                "Specify the name of the environment within the '.env' file."
            )

        # Determine queue name
        try:
            __queue_name: str = str(config(queue_name))
        except UndefinedValueError:
            __queue_name = queue_name
            if not __queue_name:
                raise ValueError(
                    f"The following queue name does not exist: {queue_name}"
                )

        # Construct the queue URL
        queue_url = (
            "https://sqs.{AWS_REGION_NAME}.amazonaws.com/{AWS_ACCOUNT_ID}/queue-{AWS_REGION_NAME}-{QUEUE_NAME}-{ENVIRONMENT}"
        ).format(
            AWS_REGION_NAME=region_name,
            AWS_ACCOUNT_ID=aws_account_id,
            QUEUE_NAME=__queue_name,
            ENVIRONMENT=__environment,
        )

        # Append .fifo if needed
        if is_fifo:
            queue_url += ".fifo"

        # Cache the constructed URL
        Helpers._url_cache[cache_key] = queue_url

        return queue_url
