from django.db import models

# Create your models here.

class Price(models.Model):
    fromDate = models.DateField(auto_now=True)
    toDate = models.DateField(null=True)
    amount = models.FloatField(default=0)
    currency =  models.CharField(default='NGN', max_length=3, null=True)
    product = models.ForeignKey('Product', on_delete = models.CASCADE, related_name='product_prices', null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.currency + str(self.amount)

class Sale(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    quantity = models.FloatField(default=0)
    price =  models.DecimalField(max_digits=12, decimal_places=2, null=True)
    currency =  models.CharField(default='NGN', max_length=3, null=True)
    date =  models.DateField(auto_now=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    creator =  models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    lastSaleTime =  models.TimeField(auto_now=True)

    def __str__(self):
        return self.product.name + " price is " + str(self.price) + " quantity is " + str(self.quantity) + " value is " + str(self.price * self.quantity)

class Unit(models.Model):
    shortDesc = models.CharField(max_length=6, null=True)
    longDesc = models.CharField(max_length=50, null=True)
    active = models.BooleanField(default=False)

class Product(models.Model):
    name = models.CharField(max_length=50, null=True)
    group = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    date = models.DateField(null=True)
    units = models.ManyToManyField("Unit")

class Authorization(models.Model):
    description = models.CharField(max_length=50, null=True)
    model = models.CharField(max_length=50, null=True)
    can_create = models.BooleanField(default=False)
    can_change = models.BooleanField(default=False)
    can_view = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class Group(models.Model):
    description = models.CharField(max_length=50, null=True)
    details = models.CharField(max_length=120, null=True)
    authorizations = models.ManyToManyField("Authorization")

class User(models.Model):
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    person = models.OneToOneField(
        'Person',
        on_delete=models.CASCADE,
        null=True
    )
    email = models.EmailField(max_length=50, null=True)
    phonenumber = models.CharField(max_length=50, null=True)
    isAuthenticated = models.BooleanField(default=False)
    authorizations = models.ManyToManyField("Authorization")
    groups = models.ManyToManyField("Group")
    active = models.BooleanField(default=False)

class Person(models.Model):
    firstname = models.CharField(max_length=50, null=True)
    middlename = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)

class Customer(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50, null=True)
    phonenumber = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=120, null=True)
    date = models.DateField(null=True)
    contact_persons = models.ForeignKey('Person', on_delete = models.CASCADE, null=True)

class ProductionBatch(models.Model):
    productType = models.CharField(max_length=50, null=True)
    flourQuantity = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    date = models.DateField(null=True)
    startTime = models.TimeField(auto_now=True)
    endTime = models.TimeField(null=True)
    products = models.ManyToManyField('Product')
    baker = models.CharField(max_length=50, null=True)
    supervisor = models.CharField(max_length=50, null=True)
    assistants = models.CharField(max_length=200, null=True)
    problems = models.CharField(max_length=200, null=True)

class ProductType(models.Model):
    name = models.CharField(max_length=50, null=True)

class ProductGroup(models.Model):
    name = models.CharField(max_length=50, null=True)