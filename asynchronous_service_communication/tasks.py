from celery import shared_task
from enum import Enum


class DecisionFromInternalAuthorizationService(Enum):
    ALLOWED = 'allowed'
    NOT_ALLOWED = 'not_allowed'
    UNKNOWN = 'unknown'
    INVALID = 'invalid'


@shared_task
def get_decision(station_id: str, driver_token: str) -> DecisionFromInternalAuthorizationService:
    print(f'in get decision Get decision for station {station_id} from driver'
          f' {driver_token}')
    is_station_available = True
    is_driver_token_valid = True
    if is_station_available and is_driver_token_valid:
        return DecisionFromInternalAuthorizationService.ALLOWED
    return DecisionFromInternalAuthorizationService.NOT_ALLOWED


def is_station_availabe(station_id: str) -> bool:
    return True # TODO: check from ACL


def is_driver_token_valid(driver_token: str) -> bool:
    return True # TODO: check from ACL
