from typing import Optional

from celery import shared_task

from asynchronous_service_communication import (
    callback,
    constant,
    models,
    decision_data_access,
    logger,
)

# TODO: write unit tests
# TODO: write python manage.py shell -> db inspection -> fetch all recent
#  DecisionInstance

@shared_task
def make_decision(primary_key: int) -> Optional[models.DecisionInstance]:
    logger.info("celery task started")
    decision_instance = decision_data_access.get_decision_instance_by_pk(
        primary_key=primary_key
    )
    logger.info(f"in get decision for decision_instance {decision_instance}")
    if decision_instance.decision_taken:
        logger.info(f"Previously decision already taken for primary key {primary_key}")
        return None
    decision = constant.DecisionTypes.NOT_ALLOWED
    if is_station_driver_ok_to_give(
        station_id=str(decision_instance.station_id),
        driver_token=decision_instance.driver_token,
    ):
        decision = constant.DecisionTypes.ALLOWED
    decision = decision_data_access.save_decision(
        primary_key=primary_key,
        decision=decision,
    )
    callback.make_callback(
        station_id=str(decision.station_id),
        driver_token=str(decision.driver_token),
        status=str(decision.decision),
        callback_url=decision.callback_url,
    )
    logger.info("celery task finished")

    return decision


def is_station_driver_ok_to_give(station_id: str, driver_token: str) -> bool:
    return True  # In real life it should be checked from ACL
