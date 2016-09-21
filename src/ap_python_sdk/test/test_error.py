from ap_python_sdk.api_requester import APIRequester
from ap_python_sdk.error import APIError
import unittest


class ErrorTest(unittest.TestCase):


    def test_alternative_payments_error(self):
        api_requester = APIRequester()
        err = api_requester.interpret_response("Unexpected error communicating with Alternative Payments.", 404)

        assert(isinstance(err, APIError))
        print(err.message)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
