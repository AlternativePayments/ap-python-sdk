from ap_python_sdk.error import AlternativePaymentsError, APIError, \
    InvalidParameterError
from numpy.ma.testutils import assert_equal
import unittest


class ErrorTest(unittest.TestCase):

    def test_alternative_payments_error(self):
        err = AlternativePaymentsError("Unexpected error communicating with Alternative Payments.")
        assert_equal(err.message, "Unexpected error communicating with Alternative Payments.")

    def test_api_error(self):
        err = APIError("Unexpected error communicating with Alternative Payments.")
        assert_equal(err.message, "Unexpected error communicating with Alternative Payments.")

    def test_invalid_parameter_error(self):
        err = InvalidParameterError("Invalid parameter name error.", "name")
        assert("Invalid parameter name.", err.message)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
