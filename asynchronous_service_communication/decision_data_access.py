from asynchronous_service_communication.constant import DecisionTypes
from asynchronous_service_communication.models import DecisionInstance


def save_decision(
    station_id: str,
    driver_token: str,
    decision: DecisionTypes,
) -> DecisionInstance:
    decision_instance = DecisionInstance(
        station_id=station_id,
        driver_token=driver_token,
        decision=decision,
    )
    decision_instance.save()
    return decision_instance