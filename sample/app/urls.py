from django.conf.urls import url

import views

urlpatterns = [
    # Refund URLs
    url(r'^add_refund', views.refund.add_refund, name='add_refund'),
    url(r'^retrieve_refund', views.refund.retrieve_refund, name='retrieve_refund'),
    url(r'^all_refunds', views.refund.all_refunds, name='all_refunds'),

     # Void URLs
    url(r'^add_void', views.void.add_void, name='add_void'),
    url(r'^retrieve_void', views.void.retrieve_void, name='retrieve_void'),
    url(r'^all_voids', views.void.all_voids, name='all_voids'),

    # Subscription URLs
    url(r'^add_subscription', views.subscription.add_subscription, name='add_subscription'),
    url(r'^retrieve_subscription', views.subscription.retrieve_subscription, name='retrieve_subscription'),
    url(r'^all_subscriptions', views.subscription.all_subscriptions, name='all_subscriptions'),

    # Plan URLs
    url(r'^add_plan', views.plan.add_plan, name='add_plan'),
    url(r'^retrieve_plan', views.plan.retrieve_plan, name='retrieve_plan'),
    url(r'^all_plans', views.plan.all_plans, name='all_plans'),

    # Transaction URLs
    url(r'^add_transaction', views.transactions.add_transaction, name='add_transaction'),
    url(r'^retrieve_transaction', views.transactions.retrieve_transaction, name='retrieve_transaction'),
    url(r'^all_transactions', views.transactions.all_transactions, name='all_transactions'),

    # Customer URLs
    url(r'^add_customer', views.customers.add_customer, name='add_customer'),
    url(r'^retrieve_customer', views.customers.retrieve_customer, name='retrieve_customer'),
    url(r'^all_customers', views.customers.all_customers, name='all_customers'),

    # Home URL
    url(r'^$', views.home.index, name='index'),
]