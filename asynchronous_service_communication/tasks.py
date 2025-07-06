from typing import Optional

from celery import shared_task

from asynchronous_service_communication import (
    callback,
    constant,
    models,
    decision_data_access,
    logger,
)


@shared_task
def make_decision(primary_key: int) -> Optional[models.DecisionInstance]:
    """
    Asynchrnous internal authorization service. Makes a decision after
    checking Access Control List (ACL)
    """
    logger.info("celery task started")
    decision_instance = decision_data_access.get_decision_instance_by_pk(
        primary_key=primary_key
    )
    logger.info(f"initial decision_instance {decision_instance}")
    if decision_instance.decision_taken_by:
        logger.info(
            f"Previously decision already taken for primary key "
            f"{primary_key} by {decision_instance.decision_taken_by}"
        )
        return None
    decision = constant.DecisionTypes.NOT_ALLOWED
    if is_station_driver_ok_to_give(
        station_id=str(decision_instance.station_id),
        driver_token=decision_instance.driver_token,
    ):
        decision = constant.DecisionTypes.ALLOWED
    decision_instance = decision_data_access.save_decision(
        primary_key=primary_key,
        decision=decision,
        decision_taken_by=constant.DecisionTakenByTypes.INTERNAL_AUTHORIZATION_SERVICE,
    )
    callback.make_callback(
        station_id=str(decision_instance.station_id),
        driver_token=str(decision_instance.driver_token),
        status=str(decision_instance.decision),
        callback_url=decision_instance.callback_url,
    )
    logger.info(f" final decision_instance {decision_instance}")
    logger.info("celery task finished")

    return decision_instance


def is_station_driver_ok_to_give(station_id: str, driver_token: str) -> bool:
    """
    Result from ACL. Here it is a mock. But in real life it should do some
    operation
    """
    return True
