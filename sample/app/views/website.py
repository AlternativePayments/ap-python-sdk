from ap_python_sdk.resources import PhoneVerification, Website, Customer, Payment, Transaction
from django.http import HttpResponse
from django.template import loader


def add_phone_verification(request):
    template = loader.get_template('website/add_phone_verification.html')

    phone_verification = PhoneVerification.create_phone_verification(
         {
            'phone': '+15555555555'
         }
    )

    context = {
       'phone_verification': phone_verification
   }

    return HttpResponse(template.render(context, request))

def check_phone_verification_turned_on(request):
    template = loader.get_template('website/check_phone_verification_turned_on.html')

    payment_option = Website.is_phone_verification_on('SEPA')

    context = {
       'payment_option': payment_option
   }

    return HttpResponse(template.render(context, request))

def add_SEPA_transaction_with_phone_verification(request):
    template = loader.get_template('website/add_SEPA_transaction_with_phone_verification.html')

    context = {}

    is_phone_verification_on = Website.is_phone_verification_on('SEPA')

    if is_phone_verification_on.hasSmsVerification == True:
        phone_verification = PhoneVerification.create_phone_verification(
          {
            'phone': '+15555555555'
           }
        )

        phone_verification['pin'] = 1234

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

        transaction = Transaction.create({
            'customer': customer,
            'payment': payment,
            'phoneverification': phone_verification,
            'amount': 500,
            'currency': 'EUR',
            'ipAddress': '127.0.0.1',
            'description': 'test sepa php sdk',
            'merchantPassThruData': 'test_sepa_123',
        })

        context = {
            'transaction': transaction
        }

    return HttpResponse(template.render(context, request))