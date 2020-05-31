from django.db import models

# Create your models here.
class Sale(models.Model):
    product = models.CharField(max_length=30)
    quantity = models.FloatField()
    price =  models.FloatField()
    currency =  models.FloatField()
    date =  models.DateField()
    customer =  models.CharField(max_length=30)
    creator =  models.CharField(max_length=30)
    lastSaleTime =  models.CharField(max_length=30)