from django.http import HttpResponse
from django.template import loader

from ap_python_sdk.resources import Transaction, RefundReason

def add_void(request):
    template = loader.get_template('void/add_void.html')

    transaction_id = request.POST.get("transaction_id")
    context = {}

    if transaction_id != None:
        void = Transaction.void(RefundReason.FRAUD, transaction_id);

        context = {
            'void': void
        }

    return HttpResponse(template.render(context, request))

def retrieve_void(request):
    template = loader.get_template('void/retrieve_void.html')

    transaction_id = request.GET.get("transaction_id")
    void_id = request.GET.get("void_id")

    context = {}

    if transaction_id != None and void_id != None:
        void = Transaction.retrieve_void(void_id, transaction_id)
        context = {
            'void': void
        }

    return HttpResponse(template.render(context, request))

def all_voids(request):
    template = loader.get_template('void/all_voids.html')

    transaction_id = request.GET.get("transaction_id")

    context = {}

    if transaction_id != None:
        voids = Transaction.voids(transaction_id)
        context = {
            'voids': voids
        }

    return HttpResponse(template.render(context, request))