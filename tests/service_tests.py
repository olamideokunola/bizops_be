import unittest
import datetime

from domain.sales.Sales import Sale
from domain.users.Users import User, Group

from domain.dataAccess.SalesDataAccess import ShelveSalesDataAccess
from domain.dataAccess.ProductsDataAccess import ShelveProductsDataAccess
from domain.dataAccess.CustomersDataAccess import ShelveCustomersDataAccess
from domain.dataAccess.UsersDataAccess import ShelveUsersDataAccess
from domain.dataAccess.GroupsDataAccess import ShelveGroupsDataAccess

from domain.dataAccess.ShelveDatabase import ShelveDataBaseManager

from domain.services.ManagerSalesServices import ManagerManageSalesService, ManagerSaleInputData
from domain.services.ManagerSalesPresenters import ManagerSalesPresenter, ManagerSaleViewModel, ManagerSaleOutputData

from domain.services.AuthenticationServices import AuthenticationService, AuthenticationInputData
from domain.services.AuthenticationPresenters import AuthenticationPresenter, AuthenticationViewModel, AuthenticationOutputData

databaseManager = ShelveDataBaseManager("domain/dataAccess/ShelveDatabase/")

class ManagerManageSaleServiceTest(unittest.TestCase):
    sale = Sale()
    managerManageSalesService = None
    databaseManager = ShelveDataBaseManager("domain/dataAccess/ShelveDatabase/")


    productsDataAccess = ShelveProductsDataAccess(databaseManager)
    customersDataAccess = ShelveCustomersDataAccess(databaseManager)
    salesDataAccess = ShelveSalesDataAccess(databaseManager)

    managerSaleInputData = ManagerSaleInputData()
    managerSaleOutputData = ManagerSaleOutputData()
    managerSaleViewModel = ManagerSaleViewModel()
    managerSalePresenter = ManagerSalesPresenter(managerSaleViewModel)
        

    def setup_service(self):
        self.managerManageSalesService = ManagerManageSalesService(
            self.productsDataAccess,
            self.customersDataAccess,
            self.salesDataAccess,
            self.managerSaleInputData,
            self.managerSaleOutputData,
            self.managerSalePresenter
        )

    def create_sales_input(self, productid, customerid, price, quantity):
        inputData = self.managerSaleInputData
        inputData.productid = productid
        inputData.customerid = customerid
        inputData.price = price
        inputData.quantity = quantity

    def test_add_day_sale(self):
        self.setup_service()
       
        # Create first sale
        self.create_sales_input(1,1,100,2)
        self.managerManageSalesService.add_day_sale()

        # get intermediate count
        intermediatecount =  len(self.managerSaleOutputData.daysales)

        # Create second sale
        self.create_sales_input(2,1,200,2)
        self.managerManageSalesService.add_day_sale()

        daysale = self.managerSaleOutputData.sale
        daysales = self.managerSaleOutputData.daysales

        print('product: ' + daysale.product.name)
        self.assertEqual(2, daysale.product.id)
        self.assertEqual(1, daysale.customer.id)
        self.assertEqual(200, daysale.price)
        self.assertEqual(2, daysale.quantity)

        self.assertGreater(len(daysales), intermediatecount)

    def test_delete_sale(self):
        self.setup_service()

        inputData = self.managerSaleInputData
        inputData.saleid = 243

        self.managerManageSalesService.delete_sale()

        deletedsale = self.managerSaleOutputData.sale

        self.assertEqual(243, deletedsale.id)

    
    def test_get_month_sales(self):
        self.setup_service()

        self.managerSaleInputData.year = 2020
        self.managerSaleInputData.month = 5

        self.managerManageSalesService.get_month_sales()

        monthsales  = self.managerSaleOutputData.monthsales

        self.assertGreater(len(monthsales), 0)



    def test_update_sale(self):
        self.setup_service()

        inputData = self.managerSaleInputData
        inputData.saleid = 11
        inputData.price = 250

        self.managerManageSalesService.update_sale()

        daysale = self.managerSaleOutputData.sale

        print('product: ' + daysale.product.name)
        self.assertEqual(250, daysale.price)

    def test_get_customers(self):
        self.setup_service()

        self.managerManageSalesService.get_customers()

        self.assertGreater(len(self.managerSaleOutputData.customers), 0)

    # def test_get_products(self):
    #     self.setup_service()

    #     self.managerManageSalesService.get_products()

    #     self.assertGreater(len(self.managerSaleOutputData.products), 0)

    # def create_product_input(self, name, group):
    #     inputData = self.managerSaleInputData
    #     inputData.name = name
    #     inputData.group = group

    # def test_create_product(self):
    #     self.setup_service()

    #     name="Test Product"
    #     group="Test Group"
    #     self.create_product_input(name, group)

    #     inputData = self.managerSaleInputData
    #     self.managerManageSalesService.create_product()

        self.assertEqual(name, self.managerSaleOutputData.product.name)

class AuthenticationServiceTest(unittest.TestCase):
    user = User("","")

    authenticationService = None

    authenticationInputData = AuthenticationInputData()
    authenticationOutputData = AuthenticationOutputData()

    authenticationViewModel = AuthenticationViewModel()
    authenticationPresenter = AuthenticationPresenter(authenticationViewModel)

    authenticationDataAccess = ShelveUsersDataAccess(databaseManager)
    authenticationGroupAccess = ShelveGroupsDataAccess(databaseManager)
 
    def setup_service(self):
        self.authenticationService = AuthenticationService(
            self.authenticationInputData,
            self.authenticationOutputData,
            self.authenticationDataAccess,
            self.authenticationGroupAccess,
            self.authenticationPresenter
        )

    def setup_user(self):
        self.authenticationInputData.username = "testuser"
        self.authenticationInputData.firstname = "First"
        self.authenticationInputData.lastname = "Last"
        self.authenticationInputData.password = "pwd"
        self.authenticationInputData.email = "testuser@mail.com"

        self.authenticationService.createuser()
    
    def test_create_user(self):
        self.setup_service()
        self.setup_user()
    
        print(self.authenticationOutputData)

        self.assertEqual(self.authenticationOutputData.user.id, "testuser")

    def test_delete_user(self):
        self.setup_service()
        self.setup_user()

        self.authenticationInputData.id = self.authenticationOutputData.user.id
        self.authenticationService.deleteuser()

        self.assertEqual(self.authenticationInputData.id, self.authenticationOutputData.user.id )

    def test_update_user(self):
        self.setup_service()
        self.setup_user()

        self.authenticationService.getuser()

        user = self.authenticationOutputData.user

        self.authenticationInputData.username = user.username
        self.authenticationInputData.firstname = user.get_firstname()
        self.authenticationInputData.lastname = user.get_lastname()
        self.authenticationInputData.password = user.password
        self.authenticationInputData.id = user.id
        self.authenticationInputData.email = "newemail@mail.com"

        self.authenticationService.updateuser()

        self.assertEqual(self.authenticationOutputData.user.email, "newemail@mail.com")

    def test_get_models(self):
        self.setup_service()
        
        self.authenticationService.getmodels()

        self.assertGreater(len(self.authenticationOutputData.models), 0)

    def test_get_groups(self):
        self.setup_service()

        self.authenticationService.getgroups()

        self.assertGreater(len(self.authenticationOutputData.groups), 0)

    def test_create_group(self):
        self.setup_service()

        group = {
            'description': "newGroup", 
            'details': "newGroup details"
        }

        self.authenticationInputData.description = "newGroup"
        self.authenticationInputData.details =  "newGroup details"
        self.authenticationInputData.authorizations = []
        self.authenticationService.creategroup()

        self.assertEqual(self.authenticationOutputData.group.description, self.authenticationInputData.description)

    def create_groups_for_delete_update(self):
        self.setup_service()

        self.authenticationInputData.description = "newGroup1"
        self.authenticationInputData.details =  "newGroup1 details"
        self.authenticationInputData.authorizations = []
        self.authenticationService.creategroup()

        id1 = self.authenticationOutputData.group.id


        self.authenticationInputData.description = "newGroup2"
        self.authenticationInputData.details =  "newGroup2 details"
        self.authenticationInputData.authorizations = []
        self.authenticationService.creategroup()

        id2 = self.authenticationOutputData.group.id

        return [id1, id2]

    def test_delete_group(self):
        self.setup_service()
        groupids = self.create_groups_for_delete_update()

        self.authenticationInputData.groupid = groupids[0]
        self.authenticationService.deletegroup()

        self.assertEqual(self.authenticationOutputData.group.id, groupids[0])

    def test_update_group(self):
        self.setup_service()
        groupids = self.create_groups_for_delete_update()

        self.authenticationInputData.groupid = groupids[0]
        self.authenticationInputData.description = "updateGroup"
        self.authenticationInputData.details =  "updateGroup details"
        self.authenticationInputData.authorizations = []

        self.authenticationService.updategroup()

        self.assertEqual(self.authenticationOutputData.group.id, groupids[0])
        self.assertEqual(self.authenticationOutputData.group.description, "updateGroup")
