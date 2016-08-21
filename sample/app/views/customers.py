from django.http import HttpResponse
from django.template import loader

from ap_python_sdk.resources import Customer

def add_customer(request):
    template = loader.get_template('customer/add_customer.html')

    email = request.POST.get("email")
    context = {}

    if email != None:
        customer = Customer.create(
                               {
                                    'firstName': 'John',
                                    'lastName': 'Doe',
                                    'email': email,
                                    'address': 'Rutledge Ave 409',
                                    'city': 'Folsom',
                                    'zip': '19033',
                                    'country': 'US',
                                    'state': 'PA',
                                    'phone': '55555555555',
                                    'created': '2016-03-24T15:19:10.7800694Z'
                               }
        );

        context = {
            'customer': customer
        }

    return HttpResponse(template.render(context, request))

def retrieve_customer(request):
    template = loader.get_template('customer/retrieve_customer.html')

    customer_id = request.GET.get("customer_id")

    context = {}

    if customer_id != None:
        customer = Customer.retrieve(customer_id)
        context = {
            'customer': customer
        }

    return HttpResponse(template.render(context, request))

def all_customers(request):
    template = loader.get_template('customer/all_customers.html')
    context = {'customers': Customer.all()}

    return HttpResponse(template.render(context, request))