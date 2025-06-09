from django.db.models import UUIDField
from typing import List

from asynchronous_service_communication import constant, models
from asynchronous_service_communication.constant import DecisionTakenByTypes


def create_initial_decision(
    station_id: UUIDField,
    driver_token: str,
    callback_url: str,
) -> models.DecisionInstance:
    decision_instance = models.DecisionInstance(
        station_id=station_id,
        driver_token=driver_token,
        callback_url=callback_url,
        decision=constant.DecisionTypes.UNKNOWN,
    )
    decision_instance.save()
    return decision_instance


def get_decision_instance_by_pk(primary_key: int) -> models.DecisionInstance:
    decisionInstance = models.DecisionInstance.objects.get(pk=primary_key)
    return decisionInstance


def get_unattened_decision_instance(
    target_time: any,
) -> List[models.DecisionInstance]:
    decision_instance_list = models.DecisionInstance.objects.filter(
        created_at__lt=target_time,
        decision_taken_by="",
        decision=constant.DecisionTypes.UNKNOWN,
    )
    return decision_instance_list


def save_decision(
    primary_key: int,
    decision: constant.DecisionTypes,
    decision_taken_by: DecisionTakenByTypes,
) -> models.DecisionInstance:
    decision_instance = models.DecisionInstance.objects.get(pk=primary_key)
    decision_instance.decision = decision
    decision_instance.decision_taken_by = decision_taken_by
    decision_instance.save()
    return decision_instance
