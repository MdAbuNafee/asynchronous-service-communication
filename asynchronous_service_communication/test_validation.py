from unittest import TestCase

from asynchronous_service_communication.validation import (
    get_session_post_data_validity_error,
)
from asynchronous_service_communication.test_common import TestCaseCommon


class Test(TestCase):
    def test_get_session_post_data_validity_error(self):
        test_case_list = [
            TestCaseCommon(
                input={
                    "driver_token": "validDriverToken1234567",
                    "callback_url": "https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12",
                },
                expected_output=["station_id is missing"],
                msg="station_id is missing",
            ),
            TestCaseCommon(
                input={
                    "station_id": "123e4567-e89b-12d3-a456-42661417400",
                    "driver_token": "validDriverToken1234567",
                    "callback_url": "https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12",
                },
                expected_output=["station id is not a valid uuid"],
                msg="station id is not a valid uuid",
            ),
            TestCaseCommon(
                input={
                    "station_id": "123e4567-e89b-12d3-a456-426614174000",
                    "callback_url": "https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12",
                },
                expected_output=["driver_token is missing"],
                msg="driver_token is missing",
            ),
            TestCaseCommon(
                input={
                    "station_id": "123e4567-e89b-12d3-a456-426614174000",
                    "driver_token": "valid",
                    "callback_url": "https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12",
                },
                expected_output=[
                    "driver token len is 5. But it should be between 20 and 80 "
                    "characters"
                ],
                msg="token len is 8. But it should be between 20 and 80 characters",
            ),
            TestCaseCommon(
                input={
                    "station_id": "123e4567-e89b-12d3-a456-426614174000",
                    "driver_token": "valid01234567890123456789012345678901234567890123456789012345678901234567890123456"
                    "78901234567890123456789012345678901234567890123456789",
                    "callback_url": "https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12",
                },
                expected_output=[
                    "driver token len is 135. But it should be between 20 and "
                    "80 characters"
                ],
                msg="token len is 8. But it should be between 20 and 80 characters",
            ),
            TestCaseCommon(
                input={
                    "station_id": "123e4567-e89b-12d3-a456-426614174000",
                    "driver_token": "validDriverToken1234567!",
                    "callback_url": "https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12",
                },
                expected_output=["driver token contains invalid character !"],
                msg="driver token contains invalid character !",
            ),
            TestCaseCommon(
                input={
                    "station_id": "123e4567-e89b-12d3-a456-426614174000",
                    "driver_token": "validDriverToken1234567",
                },
                expected_output=["callback_url is missing"],
                msg="callback_url is missing",
            ),
            TestCaseCommon(
                input={
                    "station_id": "123e4567-e89b-12d3-a456-426614174000",
                    "driver_token": "validDriverToken1234567",
                    "callback_url": "webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12",
                },
                expected_output=["callback_url is not a valid URL"],
                msg="callback_url is not a valid URL",
            ),
            TestCaseCommon(
                input={
                    "station_id": "123e4567-e89b-12d3-a456-426614174000",
                    "driver_token": "validDriverToken1234567",
                    "callback_url": "https://webhook/a02530e4-62e6-433b-ae31"
                    "-d1392e823f12",
                },
                expected_output=["callback_url is not a valid URL"],
                msg="callback_url is not a valid URL",
            ),
            TestCaseCommon(
                input={
                    "station_id": "123e4567-e89b-12d3-a456-426614174000",
                    "driver_token": "validDriverToken1234567",
                    "callback_url": "https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12",
                },
                expected_output=[],
                msg="No error in post data",
            ),
        ]
        for idx, test_case in enumerate(test_case_list):
            with self.subTest(idx=idx):
                actual_output = get_session_post_data_validity_error(
                    post_data=test_case.input
                )
                self.assertEqual(
                    actual_output,
                    test_case.expected_output,
                    msg=test_case.msg,
                )
