import logging

import requests


def make_callback(
    station_id: str,
    driver_token: str,
    status: str,
    callback_url: str,
) -> bool:
    # tyepcasting to str again to make sure values are json serializable
    station_id = str(station_id)
    driver_token = str(driver_token)
    status = str(status)
    callback_url = str(callback_url)
    post_data = {
        "station_id": station_id,
        "driver_token": driver_token,
        "status": status,
    }
    response = requests.post(callback_url, json=post_data)
    if response.status_code != 200:
        logger.error(
            f"request failed. status code : {response.status_code}. "
            f"content: {response.content}"
        )
        return False
    return True
