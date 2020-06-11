from django.db import models

# Create your models here.

class Price(models.Model):
    fromDate = models.DateField(auto_now=True)
    toDate = models.DateField(null=True)
    amount = models.FloatField(default=0)
    currency =  models.CharField(default='NGN', max_length=3)

    def __str__(self):
        return self.currency + self.amount

class Sale(models.Model):
    product = models.CharField(max_length=30)
    quantity = models.FloatField(default=0)
    price =  models.OneToOneField('Price', on_delete=models.CASCADE)
    currency =  models.CharField(default='NGN', max_length=3)
    date =  models.DateField(auto_now=True)
    customer =  models.CharField(max_length=30)
    creator =  models.CharField(max_length=30)
    lastSaleTime =  models.CharField(max_length=30)

    def __str__(self):
        return self.product + " price is " + str(self.price) + " quantity is " + str(self.quantity) + " value is " + str(self.price * self.quantity)