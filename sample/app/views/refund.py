from django.http import HttpResponse
from django.template import loader

from ap_python_sdk.resources import Transaction, RefundReason

def add_refund(request):
    template = loader.get_template('refund/add_refund.html')

    transaction_id = request.POST.get("transaction_id")
    context = {}

    if transaction_id != None:
        refund = Transaction.refund(RefundReason.FRAUD, transaction_id);

        context = {
            'refund': refund
        }

    return HttpResponse(template.render(context, request))

def retrieve_refund(request):
    template = loader.get_template('refund/retrieve_refund.html')

    transaction_id = request.GET.get("transaction_id")
    refund_id = request.GET.get("refund_id")

    context = {}

    if transaction_id != None and refund_id != None:
        refund = Transaction.retrieve_refund(refund_id, transaction_id)
        context = {
            'refund': refund
        }

    return HttpResponse(template.render(context, request))

def all_refunds(request):
    template = loader.get_template('refund/all_refunds.html')

    transaction_id = request.GET.get("transaction_id")

    context = {}

    if transaction_id != None:
        refunds = Transaction.refunds(transaction_id)
        context = {
            'refunds': refunds
        }

    return HttpResponse(template.render(context, request))