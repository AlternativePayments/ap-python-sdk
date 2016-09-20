ApPythonSdk
===================================

Alternative Payments python libary sdk. Accept local payments from all over the world

Installation
-----

Install gem, using pip:

    $ pip install ap-python-sdk

In your initializing files add line:

    import ap_python_sdk

    ap_python_sdk.api_key = 'sk_test_sqJojfKHxRJu0jHFac7bNwf4gQ9HlatcJHTGn03o'


Usage
-----

For usage and examples check `http://www.alternativepayments.com/support/api/` or sample application on our open-source repo `https://github.com/AlternativePayments/ap-python-sdk`
Example of creating new customer:

    customer = Customer.create(
                               {
                                    'firstName': 'John',
                                    'lastName': 'Doe',
                                    'email': 'tempmail@mail.com',
                                    'address': 'Rutledge Ave 409',
                                    'city': 'Folsom',
                                    'zip': '19033',
                                    'country': 'US',
                                    'state': 'PA',
                                    'phone': '55555555555',
                                    'created': '2016-03-24T15:19:10.7800694Z'
                               }
   );

Accessing object's attributes:

    customer.firstName
    => John

Same goes for complex objects like Transaction.
Create SEPA transaction:

    customer = Customer(
        id='cus_bd838e3611d34d598',
        firstName='John',
        lastName='Doe',
        email='john@doe.com',
        country='DE'
    )

    payment = Payment(
        paymentOption='SEPA',
        holder='John Doe',
        iban='BE88271080782541'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 500,
        'currency': 'EUR',
        'description': 'test sepa php sdk',
        'merchantPassThruData': 'test_sepa_123',
        'iPAddress': '127.0.0.1'
    })

Access customer:

    transaction.customer.firstName

Development
-----

To release a new version, update the version number in `version.py`, and then run `python setup.py sdist bdist_wheel upload -r https://pypi.python.org/pypi` to create a new version of library and deploy it to `https://pypi.python.org/pypi/ap_python_sdk`

Contributing
-----

1. Fork it ( https://github.com/AlternativePayments/ap-python-sdk/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request
