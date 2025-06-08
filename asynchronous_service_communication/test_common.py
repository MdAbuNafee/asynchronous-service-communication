class TestCaseCommon:
    def __init__(self, input, expected_output, msg: str):
        self.input = input
        self.expected_output = expected_output
        self.msg = msg
