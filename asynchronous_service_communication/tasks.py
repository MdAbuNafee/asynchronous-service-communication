from celery import shared_task

from asynchronous_service_communication.constant import \
    DecisionTypes

from asynchronous_service_communication.models import DecisionInstance
from asynchronous_service_communication.decision_data_access import (
    save_decision)


@shared_task
def make_decision(station_id: str, driver_token: str, callback_url: str) -> DecisionInstance:
    print(f'in get decision Get decision for station {station_id} from driver'
          f' {driver_token}')
    # TODO: set value as not allowed if decision not given
    decision = DecisionTypes.NOT_ALLOWED
    if is_station_available(station_id=station_id) and is_driver_token_valid(driver_token=driver_token):
        decision = DecisionTypes.ALLOWED
    save_decision(
        station_id=station_id,
        driver_token=driver_token,
        decision=decision,
    )
    return decision


def is_station_available(station_id: str) -> bool:
    return True # TODO: check from ACL


def is_driver_token_valid(driver_token: str) -> bool:
    return True # TODO: check from ACL
