from django.http import HttpResponse
from django.template import loader

from ap_python_sdk.resources import Plan, Period

def add_plan(request):
    template = loader.get_template('plan/add_plan.html')

    plan_name = request.POST.get("plan_name")
    plan_amount = request.POST.get("plan_amount")

    context = {}

    if plan_name != None and plan_name != "" \
        and plan_amount != None and plan_amount != "":
        plan = Plan.create({
                                'interval': 1,
                                'period': Period.DAY,
                                'amount': plan_amount,
                                'currency': 'EUR',
                                'name': plan_name,
                                'description': 'Test plan'
                            })

        context = {
            'plan': plan
        }

    return HttpResponse(template.render(context, request))

def retrieve_plan(request):
    template = loader.get_template('plan/retrieve_plan.html')

    plan_id = request.GET.get("plan_id")

    context = {}

    if plan_id != None:
        plan = Plan.retrieve(plan_id)
        context = {
            'plan': plan
        }

    return HttpResponse(template.render(context, request))

def all_plans(request):
    template = loader.get_template('plan/all_plans.html')
    context = {'plans': Plan.all()}

    return HttpResponse(template.render(context, request))