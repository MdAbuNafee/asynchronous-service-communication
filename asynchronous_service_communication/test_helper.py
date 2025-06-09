from unittest import TestCase

from asynchronous_service_communication.helper import is_valid_uuid
from asynchronous_service_communication.test_common import TestCaseCommon
from asynchronous_service_communication.helper import get_driver_token_validity_error


class Test(TestCase):
    def test_get_driver_token_validity_error(self):
        test_case_list = [
            TestCaseCommon(
                input="validDriverToken1234567",
                expected_output=[],
                msg="driver token is ok",
            ),
            TestCaseCommon(
                input="valid",
                expected_output=[
                    "driver token len is 5. But it should be between 20 and 80 "
                    "characters"
                ],
                msg="token len is 8. But it should be between 20 and 80 characters",
            ),
            TestCaseCommon(
                input="valid01234567890123456789012345678901234567890123456789012345678901234567890123456"
                "78901234567890123456789012345678901234567890123456789",
                expected_output=[
                    "driver token len is 135. But it should be between 20 and "
                    "80 characters"
                ],
                msg="token len is 8. But it should be between 20 and 80 characters",
            ),
            TestCaseCommon(
                input="validDriverToken1234567!",
                expected_output=["driver token contains invalid character !"],
                msg="driver token contains invalid character !",
            ),
        ]
        for idx, test_case in enumerate(test_case_list):
            with self.subTest(idx=idx):
                actual_output = get_driver_token_validity_error(
                    driver_token=test_case.input
                )
                self.assertEqual(
                    actual_output,
                    test_case.expected_output,
                    msg=test_case.msg,
                )

    def test_is_valid_uuid(self):
        test_case_list = [
            TestCaseCommon(
                input="123e4567-e89b-12d3-a456-42661417400",
                expected_output=False,
                msg="'station id is not a valid uuid'",
            ),
            TestCaseCommon(
                input="123e4567-e89b-12d3-a456-426614174000",
                expected_output=True,
                msg="'station id is valid'",
            ),
        ]
        for idx, test_case in enumerate(test_case_list):
            with self.subTest(idx=idx):
                actual_output = is_valid_uuid(uuid_to_test=test_case.input)
                self.assertEqual(
                    actual_output,
                    test_case.expected_output,
                    msg=test_case.msg,
                )
