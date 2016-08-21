from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add_customer', views.add_customer, name='add_customer'),
    url(r'^retrieve_customer', views.retrieve_customer, name='retrieve_customer'),
    url(r'^all_customers', views.all_customers, name='all_customers'),
    url(r'^$', views.index, name='index'),
]