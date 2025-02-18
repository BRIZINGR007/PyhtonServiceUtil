from enum import StrEnum


class RedisExpiryEnums(StrEnum):
    ONE_MIN_EXPIRY = "60"
    ONE_HOUR_EXPIRY = "3600"
    ONE_DAY_EXPIRY = "86400"
    ONE_MONTH_EXPIRY = "2592000"  # Note  :  Assuming 30 days in a month
