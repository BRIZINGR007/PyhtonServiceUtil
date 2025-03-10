from enum import StrEnum


class ErrorEnums(StrEnum):
    TOKEN_EXPIRED = "Token has expired"
    INVALID_SIGNATURE = "Invalid token: Signature verification failed"
    INVALID_AUDIENCE = "Invalid token: Audience claim verification failed"
    INVALID_ISSUER = "Invalid token: Issuer claim verification failed"
    MALFORMED_TOKEN = "Malformed token: Unable to decode"
    JWT_GENERAL_ERROR = "Internal server error during token validation"
