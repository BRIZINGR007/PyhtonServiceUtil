from enum import StrEnum


class RateLimiterGuardKeys(StrEnum):
    BEDROCK_LLM_CALL_GUARD = "BEDROCK_LLM_CALL_GUARD"
    BEDROCK_EMBEDDING_CALL_GUARD = "BEDROCK_EMBEDDING_CALL_GUARD"
    COGNITO_GUARD = "COGNITO_GURAD"
    AI_DUB_GUARD = "AI_DUB_GUARD"
    TEST_KEY = "TEST_KEY"
