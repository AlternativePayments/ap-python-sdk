from django.conf.urls import url

import views

urlpatterns = [
    # Transactions URLs
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