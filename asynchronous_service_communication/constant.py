from enum import Enum

MIN_DRIVER_TOKEN_LENGTH = 20
MAX_DRIVER_TOKEN_LENGTH = 80

TIMEOUT_IN_SECONDS = 60


class DecisionTypes(Enum):
    ALLOWED = "allowed"
    NOT_ALLOWED = "not_allowed"
    UNKNOWN = "unknown"
    INVALID = "invalid"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
