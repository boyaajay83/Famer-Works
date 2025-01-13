from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from .storage_interface import (
    get_customers_details,
    add_customer,
    get_customer_with_phone_number,
    is_today_customer,
    update_customer,
    verify_quantity,
    update_money,
    delete_contact
)


class CustomerView:
    @staticmethod
    def get_customers(request):
        try:
            data = get_customers_details()
            return render(request, 'Frontend/get_customers.html', {'customers': data})
        except Exception as e:
            messages.error(request, "Unable to fetch customer details. Please try again.")
            return redirect(reverse('error_page'))

    @staticmethod
    def customer_details(request):
        phone = request.GET.get('phone')
        if not phone:
            messages.error(request, "Phone number is required to fetch customer details.")
            return redirect(reverse('all_customers'))
        try:
            customer_details = get_customer_with_phone_number(phone_number=phone)
            return render(request, 'Frontend/customer_details.html', {'customer': customer_details})
        except Exception as e:
            messages.error(request, "Customer not found. Please check the phone number.")
            return redirect(reverse('all_customers'))

    @staticmethod
    def add_customer(request):
        if request.method == 'POST':
            required_fields = ['name', 'father_name', 'phone', 'quantity', 'taken_date', 'taken_time']
            data = {field: request.POST.get(field) for field in required_fields}

            if not all(data.values()):
                messages.error(request, "All fields are required.")
                return render(request, 'Frontend/add_customers.html')

            try:
                if is_today_customer(data['phone'], data['taken_date']):
                    messages.warning(request, "Customer has already taken items today.")
                    return render(request, 'Frontend/add_customers.html')

                add_customer(**data)
                messages.success(request, "Customer added successfully.")
                return redirect(reverse('all_customers'))
            except Exception as e:
                messages.error(request, "An error occurred while adding the customer.")
                return render(request, 'Frontend/add_customers.html')
        return render(request, 'Frontend/add_customers.html')

    @staticmethod
    def update_customer(request):
        phone = request.GET.get('phone')
        taken_date = request.GET.get('Taken_Date')
        quantity = request.GET.get('Quantity')
        name = request.GET.get('Name')

        if not all([phone, taken_date, quantity, name]):
            messages.error(request, "Missing required data.")
            return redirect(reverse('all_customers'))

        customer = {
            'Phone_Number': phone,
            'Taken_Date': taken_date,
            'Quantity': quantity,
            'Name': name
        }

        if request.method == 'POST':
            try:
                return_date = request.POST.get('return_date')
                return_time = request.POST.get('return_time')
                given_amount = request.POST.get('given_amount')
                return_quantity = request.POST.get('return_quantity')

                if int(return_quantity) > int(quantity):
                    messages.warning(request, "Return quantity exceeds taken quantity.")
                    return render(request, 'Frontend/update_customer.html', {"customer": customer})

                if verify_quantity(phone, taken_date, return_quantity, quantity):
                    messages.warning(request, "Customer does not have enough items to return.")
                    return render(request, 'Frontend/update_customer.html', {"customer": customer})

                update_customer(
                    phone_number=phone,
                    taken_date=taken_date,
                    return_quantity=return_quantity,
                    return_date=return_date,
                    return_time=return_time,
                    given_amount=given_amount
                )
                messages.success(request, "Customer details updated successfully.")
                return redirect(reverse('all_customers'))
            except Exception as e:
                messages.error(request, "Failed to update customer details.")
                return render(request, 'Frontend/update_customer.html', {"customer": customer})
        return render(request, 'Frontend/update_customer.html', {'customer': customer})

    @staticmethod
    def update_money(request):
        phone = request.GET.get('phone')
        taken_date = request.GET.get('Taken_Date')
        quantity = request.GET.get('Quantity')

        if not all([phone, taken_date, quantity]):
            messages.error(request, "Missing required data.")
            return redirect(reverse('all_customers'))

        customer = {
            'Phone_Number': phone,
            'Taken_Date': taken_date,
            'Quantity': quantity
        }

        if request.method == "POST":
            try:
                money = request.POST.get("money")
                update_money(phone_number=phone, taken_date=taken_date, quantity=quantity, money=money)
                messages.success(request, "Money updated successfully.")
                return redirect(reverse('all_customers'))
            except Exception as e:
                messages.error(request, "Failed to update money.")
                return render(request, 'Frontend/update_money.html', {'customer': customer})
        return render(request, 'Frontend/update_money.html', {'customer': customer})

    @staticmethod
    def delete_customer(request):
        phone = request.GET.get('phone')
        taken_date = request.GET.get('Taken_Date')

        if not all([phone, taken_date]):
            messages.error(request, "Phone number and taken date are required.")
            return redirect(reverse('all_customers'))

        try:
            delete_contact(phone_number=phone, taken_date=taken_date)
            messages.success(request, "Customer deleted successfully.")
            return redirect(reverse('all_customers'))
        except Exception as e:
            messages.error(request, "Failed to delete customer.")
            return redirect(reverse('all_customers'))
