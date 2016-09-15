from ap_python_sdk.resources import Transaction, Customer, Payment, RedirectUrls
from django.http import HttpResponse
from django.template import loader


def add_transaction(request):
    template = loader.get_template('transaction/add_transaction.html')

    transaction_type = request.GET.get("transaction_type").encode('utf8')
    context = {}

    if transaction_type != None:
        transaction = {}
        if transaction_type == 'sepa':
            transaction = __create_sepa_transaction()

        elif transaction_type == 'brazil_pay_boleto':
            transaction = __create_brazil_pay_boleto_transaction()

        elif transaction_type == 'brazil_pay_bank_transfer':
            transaction = __create_brazil_pay_bank_transfer_transaction()

        elif transaction_type == 'mistercash':
            transaction = __create_mistercash_transaction()

        elif transaction_type == 'teleingreso':
            transaction = __create_teleingreso_transaction()

        elif transaction_type == 'safetypay':
            transaction = __create_safetypay_transaction()

        elif transaction_type == 'poli':
            transaction = __create_poli_transaction()

        elif transaction_type == 'ideal':
            transaction = __create_ideal_transaction()

        elif transaction_type == 'trustpay':
            transaction = __create_trustpay_transaction()

        elif transaction_type == 'przelewy24':
            transaction = __create_przelewy24_transaction()

        elif transaction_type == 'giropay':
            transaction = __create_giropay_transaction()

        elif transaction_type == 'credit_card':
            transaction = __create_credit_card_transaction()

        elif transaction_type == 'directpay':
            transaction = __create_directpay_transaction()

        elif transaction_type == 'directpaymax':
            transaction = __create_directpaymax_transaction()

        else:
            raise Exception('Need to supply valid transaction type')

        context = {
            'transaction': transaction
        }

    return HttpResponse(template.render(context, request))

def retrieve_transaction(request):
    template = loader.get_template('transaction/retrieve_transaction.html')

    transaction_id = request.GET.get("transaction_id")

    context = {}

    if transaction_id != None:
        transaction = Transaction.retrieve(transaction_id)
        context = {
            'transaction': transaction
        }

    return HttpResponse(template.render(context, request))

def all_transactions(request):
    template = loader.get_template('transaction/all_transactions.html')
    context = {'transactions': Transaction.all()}

    return HttpResponse(template.render(context, request))

def __create_sepa_transaction():
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

def __create_brazil_pay_boleto_transaction():
    customer = Customer(
        firstName='Jose',
        lastName='Silva',
        email='jose@silva.com',
        address='Rua E',
        address2='1040',
        city='Maracanau',
        zip='61919-230',
        country='BR',
        state='CE',
        birthDate='12/04/1979',
        phone='+5572222312'
    )

    payment = Payment(
        paymentOption='BrazilPayBankTransfer',
        holder='JoseSilva',
        documentId='853.513.468-93',
        bankCode='hsbc'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 4500,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })

def __create_brazil_pay_bank_transfer_transaction():
    customer = Customer(
        firstName='Jose',
        lastName='Silva',
        email='jose@silva.com',
        address='Rua E',
        address2='1040',
        city='Maracanau',
        zip='61919-230',
        country='BR',
        state='CE',
        birthDate='12/04/1979',
        phone='+5572222312'
    )

    payment = Payment(
        paymentOption='BrazilPayBankTransfer',
        holder='Jose Silva',
        documentId='853.513.468-93',
        bankCode='hsbc'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 4500,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })

def __create_mistercash_transaction():
    customer = Customer(
        id='cus_bd838e3611d34d598',
        firstName='John',
        lastName='Doe',
        email='john@doe.com',
        country='BE'
    )

    payment = Payment(
        paymentOption='mistercash',
        holder='John Doe'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 500,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })

def __create_teleingreso_transaction():
    customer = Customer(
        id='cus_bd838e3611d34d598',
        firstName='John',
        lastName='Doe',
        email='john@doe.com',
        country='ES'
    )

    payment = Payment(
        paymentOption='Teleingreso',
        holder='John Doe'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 500,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })

def __create_safetypay_transaction():
    customer = Customer(
        id='cus_bd838e3611d34d598',
        firstName='John',
        lastName='Doe',
        email='john@doe.com',
        country='DE'
    )

    payment = Payment(
        paymentOption='SafetyPay',
        holder='John Doe'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 500,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })

def __create_poli_transaction():
    customer = Customer(
        id='cus_bd838e3611d34d598',
        firstName='John',
        lastName='Doe',
        email='john@doe.com',
        country='AU'
    )

    payment = Payment(
        paymentOption='POLi',
        holder='John Doe'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 500,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })

def __create_ideal_transaction():
    customer = Customer(
        id='cus_bd838e3611d34d598',
        firstName='John',
        lastName='Doe',
        email='john@doe.com',
        country='NL'
    )

    payment = Payment(
        paymentOption='ideal',
        holder='John Doe',
        bankCode='ABN_AMRO'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 500,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })

def __create_trustpay_transaction():
    customer = Customer(
        id='cus_bd838e3611d34d598',
        firstName='John',
        lastName='Doe',
        email='john@doe.com',
        country='GB'
    )

    payment = Payment(
        paymentOption='TrustPay',
        holder='John Doe'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 500,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })

def __create_przelewy24_transaction():
    customer = Customer(
        id='cus_bd838e3611d34d598',
        firstName='John',
        lastName='Doe',
        email='john@doe.com',
        country='PL'
    )

    payment = Payment(
        paymentOption='Przelewy24',
        holder='John Doe'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 500,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })

def __create_giropay_transaction():
    customer = Customer(
        id='cus_bd838e3611d34d598',
        firstName='John',
        lastName='Doe',
        email='john@doe.com',
        country='DE'
    )

    payment = Payment(
        paymentOption='Giropay',
        holder='John Doe',
        bic='TESTDETT421'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 500,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })

def __create_credit_card_transaction():
    customer = Customer(
        id='cus_bd838e3611d34d598',
        firstName='John',
        lastName='Doe',
        email='john@doe.com',
        country='US'
    )

    payment = Payment(
        paymentOption='CreditCard',
        holder='John Doe',
        creditCardNumber='4111111111111111',
        CVV2='222',
        creditCardType='visa',
        expirationYear='2019',
        expirationMonth='12'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 500,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })

def __create_directpay_transaction():
    customer = Customer(
        id='cus_bd838e3611d34d598',
        firstName='John',
        lastName='Doe',
        email='john@doe.com',
        country='DE'
    )

    payment = Payment(
        paymentOption='directpay',
        holder='John Doe'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 100,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })

def __create_directpaymax_transaction():
    customer = Customer(
        id='cus_bd838e3611d34d598',
        firstName='John',
        lastName='Doe',
        email='john@doe.com',
        country='DE'
    )

    payment = Payment(
        paymentOption='directpaymax',
        bankCode='POSTBANK',
        holder='John Doe'
    )

    redirectUrls = RedirectUrls(
        returnUrl='http://plugins.alternativepayments.com/message/success.html',
        cancelUrl='http://plugins.alternativepayments.com/message/failure.html'
    )

    return Transaction.create({
        'customer': customer,
        'payment': payment,
        'amount': 100,
        'currency': 'EUR',
        'iPAddress': '127.0.0.1',
        'redirectUrls': redirectUrls
    })
