from django.urls import path
from . import managerviews

from sales_api.managerviews import Products, Product, ProductPrices, ProductPrice, Customers, Sales, Sale, DaySales, MonthSales, ProductImage, Units, Unit
from sales_api.authenticationViews import Login, Users, JwtAuthenticator, User, Groups, Models
from sales_api.managerProductionViews import ProductionBatches

urlpatterns = [
    path('productionbatches/<int:id>', ProductionBatches.as_view(), name='addproductionbatch'),
    path('productionbatches/', ProductionBatches.as_view(), name='addproductionbatch'),
    path('<int:year>/<int:month>/<int:day>/productionbatches/', ProductionBatches.as_view(), name='productionbatches'),
    path('productimage/<str:name>', ProductImage.as_view(), name='productimage'),
    path('uploadproductimage/<int:id>', ProductImage.as_view(), name='uploadproductimage'), 
    path('groups/', Groups.as_view(), name='groups'),
    path('groups/<int:id>', Groups.as_view(), name='groups'),
    path('models/', Models.as_view(), name='models'),
    path('auth/',JwtAuthenticator.as_view(), name='auth'),
    path('users/<str:username>', User.as_view(), name='user'),
    path('users/', Users.as_view(), name='users'),
    path('login/', Login.as_view(), name='login'),
    path('units/<int:id>', Unit.as_view(), name='unit'),
    path('units/', Units.as_view(), name='units'),
    path('products/<int:id>/addprice/', ProductPrice.as_view(), name='product'),
    path('products/<int:id>/addprices/', ProductPrices.as_view(), name='product'),
    path('products/', Products.as_view(), name='products'),
    path('products/<int:id>', Product.as_view(), name='product'),
    path('customers/', Customers.as_view(), name='customers'),
    path('sales/', Sales.as_view(), name='sales'),
    path('sales/<int:id>', Sale.as_view(), name='sales'),
    path('<int:year>/<int:month>/<int:day>/sales/', DaySales.as_view(), name='daysale'),
    path('<int:year>/<int:month>/monthsales/', MonthSales.as_view(), name='monthsales')
]