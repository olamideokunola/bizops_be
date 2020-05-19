import unittest
import datetime

from domain.sales.Sales import Sale
from domain.products.Products import Product
from domain.customers.Customers import Customer
from domain.users.Users import Group

from domain.services.ManagerSalesServices import ManagerManageSalesService
from domain.services.ManagerSalesPresenters import ManagerSalesPresenter, ManagerSaleViewModel, ManagerSaleOutputData

from domain.services.AuthenticationServices import AuthenticationService
from domain.services.AuthenticationPresenters import AuthenticationPresenter, AuthenticationViewModel, AuthenticationOutputData

from domain.dataAccess.ProductsDataAccess import ShelveProductsDataAccess
from domain.dataAccess.ShelveDatabase import ShelveDataBaseManager

databseMgr = ShelveDataBaseManager("domain/dataAccess/ShelveDatabase/")

class ManagerSalesPresenterTest(unittest.TestCase):
    sale = Sale()
    managerSaleOutputData = ManagerSaleOutputData()
    managerSaleViewModel = ManagerSaleViewModel()

    def setup_presenter(self):
        self.managerSalesPresenter = ManagerSalesPresenter(self.managerSaleViewModel)
    
    def setup_sale(self):
        product = Product(id=1, name="Bread", date=datetime.date.today())
        product.add_price(amount=200, currency='NGN')
        product.add_price(amount=250, currency='NGN')

        customer = Customer(
            name= 'ALH Stores'
        )

        self.sale = Sale(   
            product=product, 
            quantity=12,
            price=123,
            customer=customer,
            currency='NGN',
            date=datetime.date.today()
        )
        
    def setup_day_sales(self):
        product = Product(id=1, name="Bread", date=datetime.date.today())
        product.add_price(amount=200, currency='NGN')
        product.add_price(amount=250, currency='NGN')

        customer = Customer(
            name= 'ALH Stores'
        )

        self.sale = Sale(
            product=product, 
            quantity=12,
            price=123,
            customer=customer,
            currency='NGN',
            date=datetime.date.today()
        )

        self.sales = []
        self.sales.append(self.sale)
        self.sales.append(self.sale)

    def test_make_json_complaint(self):
        self.setup_presenter()
        self.setup_sale()
        json_compliant_object = self.managerSalesPresenter.make_json_complaint(self.sale)
        print ('json_compliant_object: ' + str(json_compliant_object))
    
    def test_set_sale(self):
        self.setup_presenter()
        self.setup_sale()

        self.managerSaleOutputData.sale = self.sale
        self.managerSalesPresenter.set_sale(self.managerSaleOutputData)
        print (self.managerSaleViewModel.sale)
    
    def test_set_day_sales(self):
        self.setup_presenter()
        self.setup_day_sales()

        print ('Before: ' + str(self.sales))
        self.managerSaleOutputData.sales = self.sales
        self.managerSalesPresenter.set_sales(self.managerSaleOutputData)
        print ('After: ' + str(self.managerSaleViewModel.sales))

class ManagerSaleViewModelTest(unittest.TestCase):
    sale = Sale()
    managerSalesPresenter = None
    managerSaleOutputData = ManagerSaleOutputData()
    managerSaleViewModel = ManagerSaleViewModel()

    def setup_presenter(self):
        self.managerSalesPresenter = ManagerSalesPresenter(self.managerSaleViewModel)
    
    def setup_sale(self):
        product = Product(id=1, name="Bread", date=datetime.date.today())
        product.add_price(amount=200, currency='NGN')
        product.add_price(amount=250, currency='NGN')

        customer = Customer(
            name= 'ALH Stores'
        )

        self.sale = Sale(
            product=product, 
            quantity=12,
            price=123,
            customer=customer,
            currency='NGN',
            date=datetime.date.today()
        )

    def setup_sales(self):
        product = Product(id=1, name="Bread", date=datetime.date.today())
        product.add_price(amount=200, currency='NGN')
        product.add_price(amount=250, currency='NGN')

        customer = Customer(
            name= 'ALH Stores'
        )

        self.sale = Sale(
            product=product, 
            quantity=12,
            price=123,
            customer=customer,
            currency='NGN',
            date=datetime.date.today()
        )

        self.sales = []
        self.sales.append(self.sale)
        self.sales.append(self.sale)

    def test_get_sale(self):
        self.setup_presenter()
        self.setup_sale()

        self.managerSaleOutputData.sale = self.sale
        self.managerSalesPresenter.set_sale(self.managerSaleOutputData)
        # return JSON
        sale = self.managerSaleViewModel.get_sale()
        print(sale)

    def test_get_sales(self):
        self.setup_presenter()
        self.setup_sale()
        self.setup_sales()

        self.managerSaleOutputData.sales = self.sales
        self.managerSalesPresenter.set_sales(self.managerSaleOutputData)
        # return JSON
        sales = self.managerSaleViewModel.get_sales()
        print(sales)

    def test_get_products(self):
        self.setup_presenter()
        self.setup_sale()
        self.setup_sales()

        databseMgr = ShelveDataBaseManager("domain/dataAccess/ShelveDatabase/")
        productsDataAccess = ShelveProductsDataAccess(databseMgr)

        products = productsDataAccess.get_products()

        self.managerSaleOutputData.products = products
        self.managerSalesPresenter.set_products(self.managerSaleOutputData)
        # return JSON
        formatedsales = self.managerSaleViewModel.get_products()
        print(formatedsales)

class AuthenticationPresenterTest(unittest.TestCase):
    authenticationPresenter = None
    authenticationOutputData = AuthenticationOutputData()
    authenticationViewModel = AuthenticationViewModel()

    def setup_presenter(self):
        self.authenticationPresenter = AuthenticationPresenter(self.authenticationViewModel)
    
    def setup_groups(self):
        self.groups = [
            Group("bakers_test","Test Group of Bakers"),
            Group("salesmen_test","Test Group of Salesmen")
        ]
        
    def test_set_groups(self):
        self.setup_presenter()
        self.setup_groups()

        self.authenticationOutputData.groups = self.groups
        self.authenticationPresenter.set_groups(self.authenticationOutputData)

    #     # return JSON
        formattedgroups = self.authenticationViewModel.groups
        print(str(formattedgroups))

    def test_set_group(self):
        self.setup_presenter()

        group = Group("bakers_test","Test Group of Bakers")

        self.authenticationOutputData.group = group
        self.authenticationPresenter.set_group(self.authenticationOutputData)

    #     # return JSON
        formattedgroup = self.authenticationViewModel.group
        print(str(formattedgroup))