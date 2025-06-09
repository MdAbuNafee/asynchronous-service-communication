from enum import Enum

MIN_DRIVER_TOKEN_LENGTH = 20
MAX_DRIVER_TOKEN_LENGTH = 80

TIMEOUT_IN_SECONDS = 60

CRON_JOB_SLEEP_TIME_IN_SECONDS = 30

MAX_LEN_DECISION_TYPE = 20
MAX_LEN_DECISION_TAKEN_By = 20


class DecisionTypes(Enum):
    ALLOWED = "allowed"
    NOT_ALLOWED = "not_allowed"
    UNKNOWN = "unknown"
    INVALID = "invalid"


class DecisionTakenByTypes(Enum):
    INTERNAL_AUTHORIZATION_SERVICE = "internal_authorization_service"
    CRON_JOB = "cron_job"