from ap_python_sdk.error import AlternativePaymentsError
import unittest


class ErrorTest(unittest.TestCase):


    def test_alternative_payments_error(self):
        err = AlternativePaymentsError("Unexpected error communicating with Alternative Payments.")
        assert("Unexpected error communicating with Alternative Payments.", err.message)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
