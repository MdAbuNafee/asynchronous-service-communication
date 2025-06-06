from django.db.models import UUIDField

from asynchronous_service_communication.constant import DecisionTypes
from asynchronous_service_communication.models import DecisionInstance

def create_initial_decision(
    station_id: UUIDField,
    driver_token: str,
    callback_url: str,
) -> DecisionInstance:
    decision_instance = DecisionInstance(
        station_id=station_id,
        driver_token=driver_token,
        callback_url=callback_url,
        decision=DecisionTypes.UNKNOWN,
        decision_taken=False,
    )
    decision_instance.save()
    return decision_instance

def get_decision_instance(primary_key : int) -> DecisionInstance:
    decisionInstance = DecisionInstance.objects.get(pk=primary_key)
    return decisionInstance

def save_decision(primary_key: int, decision: DecisionTypes) -> DecisionInstance:
    decision_instance = DecisionInstance.objects.get(pk=primary_key)
    decision_instance.decision = decision
    decision_instance.decision_taken = True
    decision_instance.save()
    return decision_instance

# def save_decision(
#     station_id: str,
#     driver_token: str,
#     decision: DecisionTypes,
# ) -> DecisionInstance:
#     decision_instance = DecisionInstance(
#         station_id=station_id,
#         driver_token=driver_token,
#         decision=decision
#     )
#     decision_instance.save()
#     return decision_instance