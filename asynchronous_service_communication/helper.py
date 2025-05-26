from uuid import UUID

ALLOWED_CHARACTERS_FOR_DRIVER_TOKEN = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                                       "abcdefghijklmnopqrstuvwxyz012345678._~")

def get_driver_token_validity_error(token):
    validity_error = []
    if not (20 <= len(token) <= 80):
        validity_error.append(
            f'token len is {len(token)}. But it should be between 20 and 80 '
            f'characters'
        )
    for char in token:
        if char not in ALLOWED_CHARACTERS_FOR_DRIVER_TOKEN:
            validity_error.append(
                f'token contains invalid character {char}'
            )
    return validity_error

def is_valid_uuid(uuid_to_test):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = UUID(uuid_to_test)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test