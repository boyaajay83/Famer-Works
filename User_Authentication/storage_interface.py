from .models import Customers, CustomerItems, CustomerReturnItems
from datetime import datetime, timedelta


def get_total_amount(date, quantity, return_date=datetime.now().date()):

    if type(date) == str:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    elif type(return_date) == str:
        return_date = datetime.strptime(return_date, '%Y-%m-%d').date()

    no_of_days = (return_date - date).days
    total_amount = (int(no_of_days) * int(quantity)) * 20

    # print(date, quantity, return_date, total_amount, no_of_days)
    # breakpoint()
    return int(total_amount)

def get_total_amount_for_customer_item(customer_item_taken_date, customer_item_quantity, sub_items_list):
    taken_date = datetime.strptime(customer_item_taken_date, '%Y-%m-%d').date()

    all_quantity = 0
    for sub_item in sub_items_list:
        all_quantity += int(sub_item['Quantity'])

    if all_quantity == customer_item_quantity:
        all_amount = [get_total_amount(taken_date, int(sub_item['Quantity']), sub_item['Return_Date']) for sub_item in sub_items_list]
        return sum(all_amount)
    else:
        actual_amount = 0
        quantity = customer_item_quantity
        for sub_item in sub_items_list:
            quantity -= sub_item['Quantity']
            actual_amount += get_total_amount(taken_date, sub_item['Quantity'], sub_item['Return_Date'])
        actual_amount += get_total_amount(customer_item_taken_date, quantity)
    # print(customer_item_taken_date, quantity)
    # breakpoint()

    return actual_amount

def get_customers_details():
    # customers = Customers.objects.all()
    # customers.delete()
    customer_list = []
    customer_item_details = CustomerItems.objects.all().order_by('-Taken_Date')

    # print(customer_item_details)
    # breakpoint()

    for customer_item_detail in customer_item_details:

        Given_Amount_List = [customer_return_item.AmountGiven for customer_return_item in
                        CustomerReturnItems.objects.filter(CustomerItem=customer_item_detail)]

        Given_Amount = sum(Given_Amount_List)

        if customer_item_detail.Amount - Given_Amount - customer_item_detail.Given_Amount < 0:
            balance = 0
        else:
            balance = customer_item_detail.Amount - Given_Amount - customer_item_detail.Given_Amount

        if Given_Amount > customer_item_detail.Amount:
            given_amount = customer_item_detail.Amount
        else:
            given_amount = Given_Amount

        # print(given_amount)
        # breakpoint()
        customer_dict = {"Name": customer_item_detail.Customer.Name.upper(),
                         "Phonenumber": customer_item_detail.Customer.Phonenumber,
                         "Father_Name": customer_item_detail.Customer.Father_Name.upper(),
                         "Items": customer_item_detail.Item,
                         "Quantity": customer_item_detail.Quantity,
                         "Taken_Date": str(customer_item_detail.Taken_Date),
                         "Taken_Time": customer_item_detail.Taken_Time,
                         "Status": customer_item_detail.Status,
                         "Amount": customer_item_detail.Amount,
                         "Given_Amount": given_amount,
                         "Balance": balance
                         }
        customer_list.append(customer_dict)
    return customer_list


def get_customer_with_phone_number(phone_number: int):
    customer = Customers.objects.get(Phonenumber=phone_number)
    customer_item_details = CustomerItems.objects.filter(Customer=customer)

    customer_details_list = []

    for customer_item_detail in customer_item_details:
        Given_Amount_List = [customer_return_item.AmountGiven for customer_return_item in
                             CustomerReturnItems.objects.filter(CustomerItem=customer_item_detail)]

        Given_Amount = sum(Given_Amount_List)

        # print(Given_Amount, customer_item_detail.Amount)
        # breakpoint()

        if customer_item_detail.Amount - Given_Amount - customer_item_detail.Given_Amount < 0:
            balance = 0
        else:
            balance = customer_item_detail.Amount - Given_Amount - customer_item_detail.Given_Amount

        if Given_Amount > customer_item_detail.Amount:
            given_amount = customer_item_detail.Amount
        else:
            given_amount = Given_Amount

        customer_dict = {"Name": customer.Name.upper(), "Phonenumber": customer.Phonenumber,
                         "Father_Name": customer.Father_Name.upper(), "Items": customer_item_detail.Item,
                         "Quantity": customer_item_detail.Quantity,
                         "Taken_Date": str(customer_item_detail.Taken_Date),
                         "Taken_Time": customer_item_detail.Taken_Time,
                         "Status": customer_item_detail.Status,
                         "Amount": customer_item_detail.Amount,
                         "Given_Amount": given_amount,
                         "Balance": balance
                         }
        if CustomerReturnItems.objects.filter(CustomerItem=customer_item_detail, Customer=customer).exists():

            customer_return_item_taken_date = customer_item_detail.Taken_Date
            customer_return_item_list = []
            for customer_return_item in CustomerReturnItems.objects.filter(CustomerItem=customer_item_detail,
                                                                           Customer=customer):
                # print(CustomerReturnItems.objects.filter(CustomerItem=customer_item_detail))
                # breakpoint()
                quantity = customer_return_item.Quantity
                Amount = get_total_amount(customer_return_item_taken_date,  quantity, return_date=customer_return_item.Return_Date)

                if Amount - customer_return_item.AmountGiven < 0:
                    balance = 0
                else:
                    balance = Amount - customer_return_item.AmountGiven

                if customer_return_item.AmountGiven > Amount:
                    given_amount = Amount
                else:
                    given_amount = customer_return_item.AmountGiven

                customer_item_details = {
                    "Name": customer.Name.upper(),
                    "Phonenumber": customer.Phonenumber,
                    "Father_Name": customer.Father_Name.upper(),
                    "Quantity": customer_return_item.Quantity,
                    "Taken_Date": str(customer_item_detail.Taken_Date),
                    "Taken_Time": customer_item_detail.Taken_Time,
                    "Return_Date": str(customer_return_item.Return_Date),
                    "Return_Time": customer_return_item.Return_Time,
                    "Status": customer_return_item.Status,
                    "Amount": Amount,
                    "AmountGiven": given_amount,
                    "Balance": balance
                }
                customer_return_item_list.append(customer_item_details)
            customer_dict["sub_customer_return_item_list"] = customer_return_item_list
        customer_details_list.append(customer_dict)
    return customer_details_list

def add_customer(name, father_name, phone, quantity, taken_date, taken_time):

    # print(name, father_name, phone, quantity, taken_date, taken_time)
    # breakpoint()

    if Customers.objects.filter(Phonenumber=phone).exists():
        customer = Customers.objects.get(Phonenumber=phone)
        # print(customer)
        # breakpoint()
    else:
        # print("customer does not exist")
        # breakpoint()
        customer = Customers.objects.create(Name=name, Father_Name=father_name, Phonenumber=phone)
        customer.save()

        # print(customer.Name, customer.Father_Name, customer.Phonenumber)
        # breakpoint()


    taken_date = datetime.strptime(taken_date, '%Y-%m-%d').date()
    taken_time = datetime.strptime(taken_time, '%H:%M').time()

    customer_item = CustomerItems.objects.create(Customer=customer, Item="Curtains", Quantity=quantity,
                                  Taken_Date=taken_date, Taken_Time=taken_time,
                                  Amount=get_total_amount(taken_date, quantity))
    # print(customer_item)
    # breakpoint()

    customer_item.save()

def is_today_customer(phone_number: int, taken_date: str):
    if Customers.objects.filter(Phonenumber=phone_number).exists():
        customer = Customers.objects.get(Phonenumber=phone_number)
        if CustomerItems.objects.filter(Customer=customer, Taken_Date=taken_date).exists():
            return True
    return False

def update_customer(phone_number, taken_date, return_quantity, return_date, return_time, given_amount):

    customer = Customers.objects.get(Phonenumber=phone_number)
    customer_item = CustomerItems.objects.get(Customer=customer, Taken_Date=taken_date)

    return_given_amount = get_total_amount(customer_item.Taken_Date, return_quantity, return_date)
    if int(given_amount) >= return_given_amount:
        status = True
    else:
        status = False

    customer_return_item = CustomerReturnItems.objects.create(Customer=customer, CustomerItem=customer_item,
                                                              Quantity=return_quantity, AmountGiven=given_amount,
                                                              Return_Date=datetime.strptime(return_date, '%Y-%m-%d').date(),
                                                              Return_Time=datetime.strptime(return_time, '%H:%M').time(),
                                                              Status=status)

    given_amount = [customer_return_item.AmountGiven for customer_return_item in CustomerReturnItems.objects.filter(CustomerItem=customer_item)]
    total_amount = sum(given_amount)

    customer_return_item_list = []
    if CustomerReturnItems.objects.filter(CustomerItem=customer_item).exists():
        for customer_returns_item in CustomerReturnItems.objects.filter(CustomerItem=customer_item):
            customer_return_item_dict = {}
            customer_return_item_dict["Quantity"] = customer_returns_item.Quantity
            customer_return_item_dict["Return_Date"] = customer_returns_item.Return_Date
            customer_return_item_list.append(customer_return_item_dict)
    customer_item.Amount = get_total_amount_for_customer_item(taken_date, customer_item.Quantity, customer_return_item_list)

    customer_item.save()
    if customer_item.Amount <= total_amount:
        customer_item.Status = True
    else:
        customer_item.Status = False

    customer_item.save()
    customer_return_item.save()

def verify_quantity(phone_number, taken_date, return_quantity, quantity):
    customer = Customers.objects.get(Phonenumber=phone_number)
    customer_item = CustomerItems.objects.get(Customer=customer, Taken_Date=taken_date)
    customer_return_items = CustomerReturnItems.objects.filter(CustomerItem=customer_item)
    all_return_quantity = 0
    # print(phone_number, taken_date, return_quantity, quantity)
    # breakpoint()
    if customer_return_items.exists():
        for customer_return_item in customer_return_items:
            all_return_quantity += int(customer_return_item.Quantity)
        remained_quantity = int(quantity) - all_return_quantity
        if int(return_quantity) > remained_quantity:
            return True
    else:
        return False
    # print(all_return_quantity, return_quantity)
    # breakpoint()

def update_money(phone_number, taken_date, quantity, money):
    customer = Customers.objects.get(Phonenumber=phone_number)
    customer_item = CustomerItems.objects.get(Customer=customer, Taken_Date=taken_date, Quantity=quantity)
    customer_return_items = CustomerReturnItems.objects.filter(Customer=customer, CustomerItem=customer_item)

    for customer_return_item in customer_return_items:
        customer_return_item.AmountGiven += int(money)

        customer_return_item.save()

        # print(customer_return_item.AmountGiven)
        # print(customer_return_item.AmountGiven >= get_total_amount(customer_item.Taken_Date, customer_return_item.Quantity, customer_return_item.Return_Date))
        # breakpoint()
        if customer_return_item.AmountGiven >= get_total_amount(customer_item.Taken_Date, customer_return_item.Quantity, customer_return_item.Return_Date):
            customer_return_item.Status = True
            customer_return_item.save()
        else:
            customer_return_item.Status = False
            customer_return_item.save()

        given_amount = [customer_return_item.AmountGiven for customer_return_item in
                        CustomerReturnItems.objects.filter(CustomerItem=customer_item)]
        total_amount = sum(given_amount)

        customer_return_item_list = []
        if CustomerReturnItems.objects.filter(CustomerItem=customer_item).exists():
            for customer_returns_item in CustomerReturnItems.objects.filter(CustomerItem=customer_item):
                customer_return_item_dict = {}
                customer_return_item_dict["Quantity"] = customer_returns_item.Quantity
                customer_return_item_dict["Return_Date"] = customer_returns_item.Return_Date
                customer_return_item_list.append(customer_return_item_dict)
        customer_item.Amount = get_total_amount_for_customer_item(taken_date, customer_item.Quantity,
                                                                  customer_return_item_list)

        customer_item.save()
        if customer_item.Amount <= total_amount:
            customer_item.Status = True
        else:
            customer_item.Status = False

        customer_item.save()
        customer_return_item.save()

        # print(customer_return_item.Status)
        # breakpoint()
        break

def delete_contact(phone_number, taken_date):
    customer = Customers.objects.get(Phonenumber=phone_number)
    customer_item = CustomerItems.objects.get(Customer=customer, Taken_Date=taken_date)
    customer_item.delete()
