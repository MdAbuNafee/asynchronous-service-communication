from uuid import UUID

from asynchronous_service_communication import constant


ALLOWED_CHARACTERS_FOR_DRIVER_TOKEN = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    "-._~"
)


def get_driver_token_validity_error(driver_token: str) -> list[str]:
    """
    Find validity errors for a driver token.
    """
    validity_error = []
    if not (
        constant.MIN_DRIVER_TOKEN_LENGTH
        <= len(driver_token)
        <= constant.MAX_DRIVER_TOKEN_LENGTH
    ):
        validity_error.append(
            f"driver token len is {len(driver_token)}. But it should be "
            f"between 20 and 80 "
            f"characters"
        )
    for char in driver_token:
        if char not in ALLOWED_CHARACTERS_FOR_DRIVER_TOKEN:
            validity_error.append(f"driver token contains invalid character"
                                  f" {char}")
    return validity_error


def is_valid_uuid(uuid_to_test: str) -> bool:
    """
    Check if uuid_to_test is a valid UUID.
    """
    try:
        uuid_obj = UUID(uuid_to_test)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
