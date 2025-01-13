from django.db import models

class Customers(models.Model):
    Name = models.CharField(max_length=100)
    Father_Name = models.CharField(default="", max_length=100)
    Phonenumber = models.IntegerField(unique=True)

class CustomerItems(models.Model):
    Customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    Item = models.CharField(max_length=100)
    Quantity = models.IntegerField()
    Taken_Date = models.DateField()
    Taken_Time = models.TimeField()
    Status = models.BooleanField(default=False)
    Amount = models.IntegerField(default=0)
    Given_Amount = models.IntegerField(default=0)

class CustomerReturnItems(models.Model):
    Customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    CustomerItem = models.ForeignKey(CustomerItems, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=0)
    AmountGiven = models.IntegerField()
    Status = models.BooleanField(default=False)
    Return_Date = models.DateField()
    Return_Time = models.TimeField()
