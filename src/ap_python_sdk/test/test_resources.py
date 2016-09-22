from ap_python_sdk.resources import Customer, Payment, Plan, Period, Transaction, \
    Subscription, Void
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

    def test_payment(self):
        payment = Payment(
            paymentOption='SEPA',
            holder='John Doe',
            iban='BE88271080782541'
        )

        assert_equal(payment.paymentOption, 'SEPA')
        assert_equal(payment.holder, 'John Doe')
        assert_equal(payment.iban, 'BE88271080782541')

    def test_plan(self):
        plan = Plan(
            interval=1,
            period=Period.DAY,
            amount=30,
            currency="EUR",
            name="New Plan Name",
            description="Test plan"
        )

        assert_equal(plan.interval, 1)
        assert_equal(plan.period, Period.DAY)
        assert_equal(plan.amount, 30)
        assert_equal(plan.currency, "EUR")
        assert_equal(plan.name, "New Plan Name")
        assert_equal(plan.description, "Test plan")

    def test_transaction(self):
        customer = Customer(
            id="cus_bd838e3611d34d598",
            firstName="John",
            lastName="Doe",
            email="john@doe.com",
            country="DE"
        )

        payment = Payment(
            paymentOption="SEPA",
            holder="John Doe",
            iban="BE88271080782541"
        )

        transaction = Transaction(
             customer=customer,
             payment=payment,
             amount=500,
             currency="EUR",
             description="test sepa php sdk",
             merchantPassThruData="test_sepa_123",
             iPAddress="127.0.0.1"
        )

        assert_equal(transaction.customer.id, "cus_bd838e3611d34d598")
        assert_equal(transaction.customer.firstName, "John")
        assert_equal(transaction.customer.lastName, "Doe")
        assert_equal(transaction.customer.email, "john@doe.com")
        assert_equal(transaction.customer.country, "DE")

        assert_equal(transaction.payment.paymentOption, "SEPA")
        assert_equal(transaction.payment.holder, "John Doe")
        assert_equal(transaction.payment.iban, "BE88271080782541")

        assert_equal(transaction.amount, 500)
        assert_equal(transaction.currency, "EUR")
        assert_equal(transaction.description, "test sepa php sdk")
        assert_equal(transaction.merchantPassThruData, "test_sepa_123")
        assert_equal(transaction.iPAddress, "127.0.0.1")

    def test_subscription(self):
        subscription = Subscription(
            paymentId="pay_2131221f312",
            customerId="cus_bd838e3611d34d598",
            planId="plan_231f2ewqsf12"
        )

        assert_equal(subscription.paymentId, "pay_2131221f312")
        assert_equal(subscription.customerId, "cus_bd838e3611d34d598")
        assert_equal(subscription.planId, "plan_231f2ewqsf12")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
