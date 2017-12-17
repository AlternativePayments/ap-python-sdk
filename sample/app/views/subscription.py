from ap_python_sdk.resources import Subscription, Plan, Transaction, Customer, Period, Payment, PhoneVerification
from django.http import HttpResponse
from django.template import loader


def add_subscription(request):
    template = loader.get_template('subscription/add_subscription.html')

    plan_name = request.POST.get("plan_name")
    plan_amount = request.POST.get("plan_amount")
    email = request.POST.get("email")

    context = {}

    if plan_name != None and plan_name != "" \
        and plan_amount != None and plan_amount != "" \
        and email != None and email != "":

        plan = Plan.create({
            'intervalCount': 1,
            'intervalUnit': Period.DAY,
            'amount': plan_amount,
            'currency': 'EUR',
            'name': plan_name,
            'description': 'Test plan',
            'billingCycles': 12,
            'isConversionRateFixed': True,
            'ipAddress': '91.218.229.20',
            'trialPeriod': 7
        })

        customer = Customer(
            firstName='John',
            lastName='Doe',
            email=email,
            country='DE'
        )

        payment = Payment(
            paymentOption='SEPA',
            holder='John Doe',
            iban='DE89370400440532013000'
        )

        phone_verification = PhoneVerification.create_phone_verification(
          {
            'phone': '+15555555555'
           }
        )
        phone_verification['pin'] = 1234

        transaction = Transaction.create({
            'customer': customer,
            'payment': payment,
            'amount': 500,
            'currency': 'EUR',
            'description': 'test sepa php sdk',
            'merchantPassThruData': 'test_sepa_123',
            'ipAddress': '127.0.0.1',
            'phoneverification': phone_verification
        })

        subscription = Subscription.create({
            'quantity': 2,
            'ipAddress': '91.218.229.20',
            'paymentId': transaction.payment.id,
            'customerId': transaction.customer.id,
            'planId': plan.id,
            'phoneverification': phone_verification
        })

        context = {
            'subscription': subscription
        }

    return HttpResponse(template.render(context, request))

def retrieve_subscription(request):
    template = loader.get_template('subscription/retrieve_subscription.html')

    subscription_id = request.GET.get("subscription_id")

    context = {}

    if subscription_id != None:
        subscription = Subscription.retrieve(subscription_id)
        context = {
            'subscription': subscription
        }

    return HttpResponse(template.render(context, request))


def all_subscriptions(request):
    template = loader.get_template('subscription/all_subscriptions.html')
    context = {'subscriptions': Subscription.all()}

    return HttpResponse(template.render(context, request))
