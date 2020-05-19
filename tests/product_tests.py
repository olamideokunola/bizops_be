import unittest
import datetime

from domain.products.Products import Product, Unit

from domain.dataAccess.ProductsDataAccess import ShelveProductsDataAccess
from domain.dataAccess.UnitsDataAccess import ShelveUnitsDataAccess

from domain.dataAccess.ShelveDatabase import ShelveDataBaseManager

from domain.services.ManagerProductsServices import ManagerManageProductsService, ManagerProductInputData
from domain.services.ManagerProductsPresenters import ManagerProductsPresenter, ManagerProductViewModel, ManagerProductOutputData

class ProductEntityTest(unittest.TestCase):
    product = Product()

    def setup_product(self):
        self.product = Product(
            name = 'test Product',
            date = '',
            price = '200',
            prices= ['100', '200']
        )
        return self.product 

    def test_new_product(self):
        self.setup_product()
        self.assertEqual('test Product', self.product.name)
        self.assertEqual('200', self.product.price)

class UnitEntityTest(unittest.TestCase):
    pass
    unit = Unit()

    def setup_unit(self):
        self.unit = Unit(
            shortDesc = 'in',
            longDesc = 'inch',
        )
        return self.unit 

    def test_new_unit(self):
        self.setup_unit()
        self.assertEqual('in', self.unit.shortDesc)
        self.assertEqual('inch', self.unit.longDesc)
        self.assertEqual(False, self.unit.active)

class ManagerManageProductServiceTest(unittest.TestCase):
    product = Product()
    managerManageProductsService = None
    databaseManager = ShelveDataBaseManager("domain/dataAccess/ShelveDatabase/")


    productsDataAccess = ShelveProductsDataAccess(databaseManager)
    unitsDataAccess = ShelveUnitsDataAccess(databaseManager)

    managerProductInputData = ManagerProductInputData()
    managerProductOutputData = ManagerProductOutputData()
    managerProductViewModel = ManagerProductViewModel()
    managerProductPresenter = ManagerProductsPresenter(managerProductViewModel)
        
    def setup_service(self):
        self.managerManageProductsService = ManagerManageProductsService(
            self.productsDataAccess,
            self.unitsDataAccess,
            self.managerProductInputData,
            self.managerProductOutputData,
            self.managerProductPresenter
        )

    def test_get_products(self):
        self.setup_service()

        self.managerManageProductsService.get_products()

        self.assertGreater(len(self.managerProductOutputData.products), 0)

    def create_product_input(self, name, group):
        self.managerProductInputData.name = name
        self.managerProductInputData.group = group

    def test_create_product(self):
        self.setup_service()

        name="Test Product"
        group="Test Group"
        self.create_product_input(name, group)

        # inputData = self.managerProductInputData
        self.managerManageProductsService.create_product()

        self.assertEqual(name, self.managerProductOutputData.product.name)

    def test_delete_product(self):
        self.setup_service()

        # create product
        name="Test Product"
        group="Test Group"
        self.create_product_input(name, group)
        
        # get initial length
        self.managerManageProductsService.get_products()
        len1 = len(self.managerProductOutputData.products)

        # inputData = self.managerProductInputData
        self.managerManageProductsService.create_product()

        # Get products before delete
        self.managerManageProductsService.get_products()
        len2 = len(self.managerProductOutputData.products)

        # delete new product
        self.managerProductInputData.productid = self.managerProductOutputData.product.id
        self.managerManageProductsService.delete_product()

        # get product after delete
        self.managerManageProductsService.get_products()
        len3 = len(self.managerProductOutputData.products)

        # Test for increase from len1 to len2
        self.assertGreater(len2, len1)

         # Test for len2 greater than len3 after deletion
        self.assertGreater(len2, len3)

    def test_update_product(self):
        self.setup_service()

        # create product
        name="Test Product"
        group="Test Group"
        self.create_product_input(name, group)
        self.managerManageProductsService.create_product()

        # get initial product name
        name1 = self.managerProductOutputData.product.name

        # set product id to id of created product
        self.managerProductInputData.productid = self.managerProductOutputData.product.id

        # update product name
        self.managerProductInputData.name = "Changed name"

        # update product
        self.managerManageProductsService.update_product()

        # get new name
        name2 = self.managerProductOutputData.product.name

        # test inequality of name1 and name2
        self.assertNotEqual(name1, name2)

    def test_create_unit(self):
        self.setup_service()

        # create unit
        self.managerProductInputData.unitShortDesc = 'sht'
        self.managerProductInputData.unitLongDesc = 'short'

        self.managerManageProductsService.create_unit()

        self.assertEqual(self.managerProductInputData.unitShortDesc, self.managerProductOutputData.unit.shortDesc)
    
    def test_get_units(self):
        self.setup_service()

        self.managerManageProductsService.get_units()

        self.assertGreater(len(self.managerProductOutputData.units), 0)

    def test_get_unit(self):
        self.setup_service()

        self.managerProductInputData.unitid = 1

        self.managerManageProductsService.get_unit()

        self.assertEqual(self.managerProductOutputData.unit.id, 1)

    def test_delete_unit(self):
        self.setup_service()

        # create unit
        self.managerProductInputData.unitShortDesc = 'sht'
        self.managerProductInputData.unitLongDesc = 'short'
        
        # get initial length
        self.managerManageProductsService.get_units()
        len1 = len(self.managerProductOutputData.units)

        # inputData = self.managerProductInputData
        self.managerManageProductsService.create_unit()

        # Get products before delete
        self.managerManageProductsService.get_units()
        len2 = len(self.managerProductOutputData.units)

        # delete new unit
        self.managerProductInputData.unitid = self.managerProductOutputData.unit.id
        self.managerManageProductsService.delete_unit()

        # get product after delete
        self.managerManageProductsService.get_units()
        len3 = len(self.managerProductOutputData.units)

        # Test for increase from len1 to len2
        self.assertGreater(len2, len1)

        # Test for len2 greater than len3 after deletion
        self.assertGreater(len2, len3)

    def test_update_unit(self):
        self.setup_service()

       # create unit
        self.managerProductInputData.unitShortDesc = 'sht'
        self.managerProductInputData.unitLongDesc = 'short'
        self.managerManageProductsService.create_unit()

        # get initial unit shortDesc
        shortDesc1 = self.managerProductOutputData.unit.shortDesc

        # set unit id to id of created unit
        self.managerProductInputData.unitid = self.managerProductOutputData.unit.id

        # update unit name
        self.managerProductInputData.unitShortDesc = "sh"

        # update unit
        self.managerManageProductsService.update_unit()

        # get new name
        shortDesc2 = self.managerProductOutputData.unit.shortDesc

        # test inequality of name1 and name2
        self.assertNotEqual(shortDesc1, shortDesc2)

    def test_add_price(self):
        self.setup_service()

        # create product
        name="Test Product"
        group="Test Group"
        self.create_product_input(name, group)
        self.managerManageProductsService.create_product()

       
        # create price
        self.managerProductInputData.productid = self.managerProductOutputData.product.id
        self.managerProductInputData.amount = 300
        self.managerProductInputData.pricedate =  datetime.date(2020,5,1)

        # add price
        self.managerManageProductsService.add_price()

        # get product
        prices = self.managerProductOutputData.product.prices

        # check for price
        self.assertGreater(len(prices), 0)


class ProductPresenterTest(unittest.TestCase):
    presenter = None
    outputData = ManagerProductOutputData()
    viewModel = ManagerProductViewModel()

    def setup_presenter(self):
        self.presenter = ManagerProductsPresenter(self.viewModel)
    
    def setup_unit(self):
        self.unit = Unit(id= 0, shortDesc='ns', longDesc='new Short', active=False)
        
    def test_set_unit(self):
        self.setup_presenter()
        self.setup_unit()

        self.outputData.unit = self.unit
        self.presenter.set_unit(self.outputData)

        # test
        self.assertDictEqual(self.viewModel.get_unit(),
        {
            'id': 0,
            'short': 'ns',
            'long': 'new Short',
            'active': False
        })