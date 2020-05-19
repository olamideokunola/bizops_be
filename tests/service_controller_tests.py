import unittest
import datetime

from domain.sales.Sales import Sale

from domain.dataAccess.SalesDataAccess import ShelveSalesDataAccess
from domain.dataAccess.ProductsDataAccess import ShelveProductsDataAccess
from domain.dataAccess.CustomersDataAccess import ShelveCustomersDataAccess

from domain.dataAccess.ShelveDatabase import ShelveDataBaseManager

from domain.services.ManagerSalesServices import ManagerManageSalesService, ManagerSaleInputData
from domain.services.ManagerSalesPresenters import ManagerSalesPresenter, ManagerSaleViewModel, ManagerSaleOutputData
from domain.controllers.ManageSalesControllers import ManagerSaleServiceController

class ManagerManageSaleServiceContollerTest(unittest.TestCase):
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

    def setup_service_controller(self):
        self.managerManageSalesServiceController = ManagerSaleServiceController(
            self.managerSaleInputData,
            self.managerManageSalesService
        )

    def test_add_day_sale(self):
        self.setup_service()
        self.setup_service_controller()
        
        # Create first sale
        date = {
            'year': datetime.date.today().year,
            'month': datetime.date.today().month,
            'day': datetime.date.today().day,
        }
        self.managerManageSalesServiceController.add_day_sale(1,20,200,date,2)

        # get intermediate count
        intermediatecount =  len(self.managerSaleOutputData.daysales)

        # Create second sale
        self.managerManageSalesServiceController.add_day_sale(2,10,300,date,1)

        daysale = self.managerSaleOutputData.sale
        daysales = self.managerSaleOutputData.daysales

        print('product: ' + daysale.product.name)
        self.assertEqual(2, daysale.product.id)
        self.assertEqual(1, daysale.customer.id)
        self.assertEqual(300, daysale.price)
        self.assertEqual(10, daysale.quantity)

        self.assertGreater(len(daysales), intermediatecount)

    def test_update_sale(self):
        self.setup_service()
        self.setup_service_controller()

        self.managerManageSalesServiceController.update_sale(9,2,10,350,datetime.date.today(),1)
        
        daysale = self.managerSaleOutputData.sale

        print('product: ' + daysale.product.name)
        self.assertEqual(350, daysale.price)

    def test_get_customers(self):
        self.setup_service()
        self.setup_service_controller()

        self.managerManageSalesServiceController.get_customers()

        self.assertGreater(len(self.managerSaleOutputData.customers), 0)

    def test_get_products(self):
        self.setup_service()
        self.setup_service_controller()

        self.managerManageSalesServiceController.get_products()

        self.assertGreater(len(self.managerSaleOutputData.products), 0)

    def test_create_product(self):
        self.setup_service()
        self.setup_service_controller()

        name="Test Product"
        group="Test Group"
        date = {
            'year': datetime.date.today().year,
            'month': datetime.date.today().month,
            'day': datetime.date.today().day,
        }

        self.managerManageSalesServiceController.create_product(name, group, date)

        self.assertEqual(self.managerSaleOutputData.product.name, name)