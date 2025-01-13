from django.urls import path
from .views import CustomerView

urlpatterns = [
    path('', CustomerView.get_customers, name='all_customers'),
    path('delete', CustomerView.delete_customer, name='delete_customer'),
    path("customer_details/", CustomerView.customer_details, name="customer_details"),
    path("customer_details/money", CustomerView.update_money, name="customer_details_money"),
    path("customer_details/update_customer/", CustomerView.update_customer, name="update_customer"),
    path("customer_details/update_customer/update_customer_details", CustomerView.update_customer, name="update_customer_details"),
    path("add_customer", CustomerView.add_customer, name="add_customer"),
    ]