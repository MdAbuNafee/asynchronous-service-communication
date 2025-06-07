from typing import Optional

from django.forms import UUIDField

from asynchronous_service_communication import logger

from celery import shared_task

from asynchronous_service_communication.constant import \
    DecisionTypes

from asynchronous_service_communication.models import DecisionInstance
from asynchronous_service_communication.decision_data_access import save_decision


@shared_task
def make_decision(primary_key: int) -> Optional[DecisionInstance]:
    decision_instance = DecisionInstance.objects.get(pk=primary_key)
    logger.info(f'in get decision for decision_instance {decision_instance}')
    if decision_instance.decision_taken:
        logger.info(f"Previously decision already taken for primary key {primary_key}")
        return None
    decision = DecisionTypes.NOT_ALLOWED
    if is_station_driver_ok_to_give(
            station_id=str(decision_instance.station_id),
            driver_token=decision_instance.driver_token,
    ):
        decision = DecisionTypes.ALLOWED
    decision = save_decision(primary_key=primary_key, decision=decision)

    # TODO: make a command to check the models created 5 mins ago and not yet
    #  called url callback. Then call the url with decision unknown and call
    #  url callback
    # TODO: create another url callback in urls.py
    # TODO: write unit tests

    return decision


def is_station_driver_ok_to_give(station_id: str, driver_token: str) -> bool:
    return True # In real life it should be checked from ACL


