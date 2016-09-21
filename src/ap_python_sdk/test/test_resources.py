from ap_python_sdk.resources import Customer
from numpy.ma.testutils import assert_equal
import unittest


class Test(unittest.TestCase):


    def test_customer(self):
        customer = Customer(
            id='cus_bd838e3611d34d598',
            firstName='John',
            lastName='Doe',
            email='john@doe.com',
            country='DE'
        )
        
        assert_equal(customer.id, 'cus_bd838e3611d34d598')
        assert_equal(customer.firstName, 'John')
        assert_equal(customer.lastName, 'Doe')
        assert_equal(customer.email, 'john@doe.com')
        assert_equal(customer.country, 'DE')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
