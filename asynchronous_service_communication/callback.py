import requests

from asynchronous_service_communication import logger


def make_callback(
    station_id: str,
    driver_token: str,
    status: str,
    callback_url: str,
) -> bool:
    """
    Make a callback to the callback_url with other parameters as json post data
    """
    # tyepcasting to all the variables to str again to make sure values are
    # json serializable
    logger.info(f"beginning of make_callback")
    callback_url = str(callback_url)
    post_data = {
        "station_id": str(station_id),
        "driver_token": str(driver_token),
        "status": str(status),
    }
    logger.info(f"making callback to {callback_url} post_data: {post_data}")
    try:
        response = requests.post(callback_url, json=post_data)
        logger.info(f"callback response: {response}")
        if response.status_code != 200:
            logger.error(
                f"request failed. status code : {response.status_code}. "
                f"content: {response.content}"
            )
            return False
    except Exception as e:
        logger.error(f"HTTP Error : {e}")
        return False
    logger.info(f"callback finished")
    return True
