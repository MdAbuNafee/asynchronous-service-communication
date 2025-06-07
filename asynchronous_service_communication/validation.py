import validators

from asynchronous_service_communication import helper


def get_session_post_data_validity_error(post_data: dict[str, str]) -> list[str]:
    validity_errors = []
    try:
        if "station_id" not in post_data:
            validity_errors.append("station_id is missing")
        else:
            station_id = post_data["station_id"]
            if not helper.is_valid_uuid(uuid_to_test=station_id):
                validity_errors.append("station id is not a valid uuid")

        if "driver_token" not in post_data:
            validity_errors.append("driver_token is missing")
        else:
            driver_token = post_data["driver_token"]
            driver_token_validity_error = helper.get_driver_token_validity_error(
                driver_token=driver_token
            )
            validity_errors.extend(driver_token_validity_error)

        if "callback_url" not in post_data:
            validity_errors.append("callback_url is missing")
        elif not validators.url(post_data["callback_url"]):
            validity_errors.append("callback_url is not a valid URL")

    except:
        validity_errors.append("invalid post data. failed to validate")
    return validity_errors
