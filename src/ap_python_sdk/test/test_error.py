from ap_python_sdk.error import AlternativePaymentsError, APIError, \
    InvalidParameterError
import unittest


class ErrorTest(unittest.TestCase):

    def test_alternative_payments_error(self):
        err = AlternativePaymentsError("Unexpected error communicating with Alternative Payments.")
        assert("Unexpected error communicating with Alternative Payments.", err.message)

    def test_api_error(self):
        err = APIError("Unexpected error communicating with Alternative Payments.")
        assert("Unexpected error communicating with Alternative Payments.", err.message)

    def test_invalid_parameter_error(self):
        err = InvalidParameterError("Invalid parameter error")
        assert("Invalid parameter error", err.message)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
