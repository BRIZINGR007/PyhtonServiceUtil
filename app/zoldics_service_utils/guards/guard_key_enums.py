from enum import StrEnum


class RateLimiterGuardKeys(StrEnum):
    BEDROCK_LLM_CALL_GUARD = "BEDROCK_LLM_CALL_GUARD"
    BEDROCK_EMBEDDING_CALL_GUARD = "BEDROCK_EMBEDDING_CALL_GUARD"
    COGNITO_GUARD = "COGNITO_GURAD"
    TEST_KEY = "TEST_KEY"
