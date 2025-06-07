from asynchronous_service_communication.models import DecisionInstance

from asynchronous_service_communication import logger
import requests

def make_callback(
    station_id: str,
    driver_token: str,
    status: str,
    callback_url: str,
) -> bool:
    post_data = {
        'station_id': station_id,
        'driver_token': driver_token,
        'status': status,
    }
    response = requests.post(callback_url, data=post_data)
    if response.status_code != 200:
        logger.error(f"request failed. status code : {response.status_code}. "
                     f"content: {response.content}")
        return False
    return True