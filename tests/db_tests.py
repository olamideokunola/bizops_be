import unittest
import datetime

from domain.sales.Sales import Sale
from domain.sales.SalesDataAccessInterface import SalesDataAccessInterface
from domain.dataAccess.ShelveDatabase import ShelveDataBaseManager, Database
from domain.dataAccess.SalesDataAccess import ShelveSalesDataAccess

from domain.products.Products import Product
from domain.products.ProductsDataAccessInterface import ProductsDataAccessInterface
from domain.dataAccess.ProductsDataAccess import ShelveProductsDataAccess

from domain.customers.Customers import Customer
from domain.customers.CustomersDataAccessInterface import CustomersDataAccessInterface
from domain.dataAccess.CustomersDataAccess import ShelveCustomersDataAccess

from domain.users.Users import Group
from domain.users.GroupsDataAccessInterface import GroupsDataAccessInterface
from domain.dataAccess.GroupsDataAccess import ShelveGroupsDataAccess

from domain.products.Products import Unit
from domain.products.UnitsDataAccessInterface import UnitsDataAccessInterface
from domain.dataAccess.UnitsDataAccess import ShelveUnitsDataAccess

from domain.production.ProductionBatch import ProductionBatch
from domain.production.ProductionBatchDataAccessInterface import ProductionBatchDataAccessInterface
from domain.dataAccess.ProductionBatchDataAccess import ShelveProductionBatchDataAccess

dblocation = "domain/dataAccess/ShelveDatabase/"

class DbSetup:
    dblocation = "domain/dataAccess/ShelveDatabase/"
    shelvedb = ShelveDataBaseManager(dblocation)
    newdb = None
    salesdbname= ''
    test_model_name = ''
    testmodel = None
    

    def __init__(self):
        pass

    def setup_database(self):
        self.salesdbname='salesdb'
        self.shelvedb.create_database(self.salesdbname)
        self.newdb = self.shelvedb.get_database(self.salesdbname)
        return self.newdb

    def setup_model(self, modelname):
        self.setup_database()
        self.test_model_name = modelname
        self.newdb.create_model(self.test_model_name)
        self.testmodel = self.newdb.get_model(self.test_model_name)
    
    
        

class ShelveDataBaseTest(unittest.TestCase):
    shelvedb = ShelveDataBaseManager("domain/dataAccess/ShelveDatabase/")
    newdb = None
    salesdbname= ''
    test_model_name = ''
    testmodel = None
    
    def setup_database(self):
        self.salesdbname='salesdb'
        self.shelvedb.create_database(self.salesdbname)
        self.newdb = self.shelvedb.get_database(self.salesdbname)
        return self.newdb

    def setup_model(self, modelname):
        self.setup_database()
        self.test_model_name = modelname
        self.newdb.create_model(self.test_model_name)
        self.testmodel = self.newdb.get_model(self.test_model_name)

    def test_init_database(self):
        self.shelvedb

    def test_create_database(self):
        self.setup_database()
        self.assertEqual(self.salesdbname, self.newdb.name)

    def test_create_model(self):
        self.setup_model('test')
        self.assertIn('test', self.newdb.models)
    
    def test_create_new_id_on_empty_db(self):
        self.setup_model('test')

        newid = self.newdb.create_new_id(self.test_model_name)
        print ('newid: ' + str(newid))
        self.assertGreater(int(newid),0)

    def test_create_new_id(self):
        self.setup_model('test')

        newid = self.newdb.create_new_id(self.test_model_name)
        print ('newid: ' + str(newid))
        self.assertGreater(int(newid),0)
    
    def test_save(self):
        self.setup_model('test')
        sale = Sale(id=1)
        sale2 = Sale(id=2)

        savedsale = self.newdb.save('test', sale)
        self.newdb.save('test', sale2)
        
        self.assertEqual(savedsale.id, 1)
    
    def test_delete(self):
        self.setup_model('test')
        sale = Sale(id=1)

        savedsale = self.newdb.save('test', sale)

        deletedsale = self.newdb.delete('test', savedsale)

        self.assertEqual(savedsale.id, deletedsale.id)

    def test_get(self):
        self.setup_model('test')

        savedsale = self.newdb.get('test', 1)
        
        self.assertEqual(savedsale.id, 1)
    
    def test_get_many(self):
        self.setup_model('test')

        savedsales = self.newdb.get_many('test', [1,2,3])
        
        self.assertEqual(savedsales[0].id, 1)
        self.assertEqual(savedsales[1].id, 2)
        #self.assertEqual(savedsales[3].id, 3)
    

class SalesDataAccessTest(unittest.TestCase):
    salesdb = None
    dbsetup = DbSetup()

    def setup_db(self):
        self.dbsetup.setup_database()
        self.salesdb = self.dbsetup.newdb

    def setup_model(self):
        self.setup_db()
        self.dbsetup.setup_model("Sale")

    def setup_sales_data_access(self):
        self.shelveDatabase = ShelveDataBaseManager("domain/dataAccess/ShelveDatabase/")
        self.sales_data_access = ShelveSalesDataAccess(self.shelveDatabase)

    def setup_products_data_access(self):
        self.products_data_access = ShelveProductsDataAccess(self.shelveDatabase)

    def setup_customers_data_access(self):
        self.customers_data_access = ShelveCustomersDataAccess(self.shelveDatabase)

    def setup_sale(self):   
        self.setup_sales_data_access() 
        self.setup_products_data_access()
        self.setup_customers_data_access()

        # self.sale9 = Sale(id=9, date=datetime.date.today(), creator='joy@favychos.com')
        # self.sale10 = Sale(id=10, date=datetime.date.today(), creator='joy@favychos.com')
        self.sale9 = Sale(
                product=self.products_data_access.get_product(1),
                quantity=2,
                price=300,
                customer=self.customers_data_access.get_customer(1),
                currency='NGN',
                date=datetime.date.today(),
                creator='joy@favychos.com'
            )
        self.sale10 = Sale(
                product=self.products_data_access.get_product(2),
                quantity=20,
                price=200,
                customer=self.customers_data_access.get_customer(2),
                currency='NGN',
                date=datetime.date.today(),
                creator='olamide@favychos.com'
            )


    def save_sales(self):
        self.sales_data_access.save(self.sale9)
        self.sales_data_access.save(self.sale10)

    def test_save(self):
        self.setup_db()
        self.setup_sale()
        self.setup_sales_data_access()

        savesale = self.sales_data_access.save(self.sale9)

        self.assertNotEqual(None,savesale.id)
    
    def test_delete(self):
        self.setup_db()
        self.setup_sale()
        self.setup_sales_data_access()

        savesale = self.sales_data_access.save(self.sale9)
        deletedsale = self.sales_data_access.delete(savesale)

        self.assertEqual(deletedsale.id, savesale.id)

    def test_get(self):
        self.setup_db()
        self.setup_sale()
        self.setup_sales_data_access()

        self.assertEqual(1,self.sales_data_access.get(1).id)
    
    def test_get_day_sales(self):
        self.setup_db()
        self.setup_sale()
        self.setup_sales_data_access()

        self.save_sales()

        self.assertGreater(len(self.sales_data_access.get_day_sales(datetime.date.today())), 0)

    def test_get_day_sale(self):
        self.setup_db()
        self.setup_sale()
        self.setup_sales_data_access()

        self.save_sales()

        self.assertEqual(1, self.sales_data_access.get_day_sale(datetime.date.today(), 1).id)
    
    def test_get_sales(self):
        self.setup_db()
        self.setup_sale()
        self.setup_sales_data_access()

        print(self.sales_data_access.get_sales())

        self.assertGreater(len(self.sales_data_access.get_sales()), 0)

class ProductsDataAccessTest(unittest.TestCase):
    productsdb = None
    dbsetup = DbSetup()

    def setup_db(self):
        self.dbsetup.setup_database()
        self.productsdb = self.dbsetup.newdb

    def setup_model(self):
        self.setup_db()
        self.dbsetup.setup_model("Product")

    def setup_product(self):        
        self.product1 = Product(id=1, name='Big Loaf',price='200', date=datetime.date.today())
        self.product2 = Product(id=2, name='Small Loaf',price='300', date=datetime.date.today())

    def setup_products_data_access(self):
        shelveDatabase = ShelveDataBaseManager("domain/dataAccess/ShelveDatabase/")
        self.products_data_access = ShelveProductsDataAccess(shelveDatabase)
    
    def save_products(self):
        self.products_data_access.save(self.product1)
        self.products_data_access.save(self.product2)

    def test_save(self):
        self.setup_db()
        self.setup_product()
        self.setup_products_data_access()

        saveproduct = self.products_data_access.save(self.product1)
        saveproduct = self.products_data_access.save(self.product2)

        self.assertEqual(2,saveproduct.id)
        self.assertEqual("Small Loaf",saveproduct.name)

    def test_get(self):
        self.setup_db()
        self.setup_product()
        self.setup_products_data_access()
        self.save_products()

        self.assertEqual(1,self.products_data_access.get(1).id)
    
    def test_get_product(self):
        self.setup_db()
        self.setup_product()
        self.setup_products_data_access()
        self.save_products()

        self.assertEqual(1,self.products_data_access.get_product(1).id)

    def test_get_products(self):
        self.setup_db()
        self.setup_product()
        self.setup_products_data_access()
        self.save_products()

        self.assertEqual(2,len(self.products_data_access.get_products()))

class UnitsDataAccessTest(unittest.TestCase):
    unitsdb = None
    dbsetup = DbSetup()

    def setup_db(self):
        self.dbsetup.setup_database()
        self.unitsdb = self.dbsetup.newdb

    def setup_model(self):
        self.setup_db()
        self.dbsetup.setup_model("Unit")

    def setup_unit(self):        
        self.unit1 = Unit(id=1, shortDesc='ft', longDesc='foot', active=False)
        self.unit2 = Unit(id=2, shortDesc='g', longDesc='gram')

    def setup_units_data_access(self):
        shelveDatabase = ShelveDataBaseManager("domain/dataAccess/ShelveDatabase/")
        self.units_data_access = ShelveUnitsDataAccess(shelveDatabase)
    
    def save_units(self):
        self.units_data_access.save(self.unit1)
        self.units_data_access.save(self.unit2)

    def test_save(self):
        self.setup_db()
        self.setup_unit()
        self.setup_units_data_access()

        saveunit = self.units_data_access.save(self.unit1)
        saveunit = self.units_data_access.save(self.unit2)

        self.assertEqual(2,saveunit.id)
        self.assertEqual("g",saveunit.shortDesc)

    def test_get(self):
        self.setup_db()
        self.setup_unit()
        self.setup_units_data_access()
        self.save_units()

        self.assertEqual(1,self.units_data_access.get(1).id)
    
    def test_get_unit(self):
        self.setup_db()
        self.setup_unit()
        self.setup_units_data_access()
        self.save_units()

        self.assertEqual(1,self.units_data_access.get_unit(1).id)

    def test_get_units(self):
        self.setup_db()
        self.setup_unit()
        self.setup_units_data_access()
        self.save_units()

        self.assertEqual(2,len(self.units_data_access.get_units()))

class CustomersDataAccessTest(unittest.TestCase):
    customersdb = None
    dbsetup = DbSetup()

    def setup_db(self):
        self.dbsetup.setup_database()
        self.customersdb = self.dbsetup.newdb

    def setup_model(self):
        self.setup_db()
        self.dbsetup.setup_model("Customer")

    def setup_customer(self):        
        self.customer1 = Customer(id=1, name='Mallam LSDPC', date=datetime.date.today())
        self.customer2 = Customer(id=2, name='Mummy Mariam', date=datetime.date.today())

    def setup_customers_data_access(self):
        shelveDatabase = ShelveDataBaseManager("domain/dataAccess/ShelveDatabase/")
        self.customers_data_access = ShelveCustomersDataAccess(shelveDatabase)
    
    def save_customers(self):
        self.customers_data_access.save(self.customer1)
        self.customers_data_access.save(self.customer2)

    def test_save(self):
        self.setup_db()
        self.setup_customer()
        self.setup_customers_data_access()

        savecustomer = self.customers_data_access.save(self.customer1)

        self.assertEqual(1,savecustomer.id)
        self.assertEqual("Mallam LSDPC",savecustomer.name)

    def test_get(self):
        self.setup_db()
        self.setup_customer()
        self.setup_customers_data_access()
        self.save_customers()

        self.assertEqual(1,self.customers_data_access.get(1).id)
    
    def test_get_customer(self):
        self.setup_db()
        self.setup_customer()
        self.setup_customers_data_access()
        self.save_customers()

        self.assertEqual(1,self.customers_data_access.get_customer(1).id)

    def test_get_customers(self):
        self.setup_db()
        self.setup_customer()
        self.setup_customers_data_access()
        self.save_customers()

        self.assertEqual(2,len(self.customers_data_access.get_customers()))


class GroupsDataAccessTest(unittest.TestCase):
    groupsdb = None
    dbsetup = DbSetup()

    def setup_db(self):
        self.dbsetup.setup_database()
        self.groupsdb = self.dbsetup.newdb

    def setup_groups(self):
        self.group1 = Group("Group1","Users in Group1")
        self.group2 = Group("Group2","Users in Group2")

    def setup_groups_data_access(self):
        shelveDatabase = ShelveDataBaseManager(dblocation)
        self.groups_data_access = ShelveGroupsDataAccess(shelveDatabase)

    def save_groups(self):
        self.setup_db()
        self.setup_groups()
        self.setup_groups_data_access()

        self.savegroup1 = self.groups_data_access.save(self.group1)
        self.savegroup2 = self.groups_data_access.save(self.group2)
    
    def test_save_group(self):
        self.save_groups()
        #self.assertEqual(1,self.savegroup1.id)
        self.assertEqual(self.group1.description, self.savegroup1.description)
    
    def test_delete_group(self):
        self.save_groups()
        #self.assertEqual(1,self.savegroup1.id)
        deletedgroup = self.groups_data_access.delete(self.savegroup1)
        
        self.assertEqual(self.savegroup1.id, deletedgroup.id)

    def test_get_groups(self):
        self.setup_db()
        self.setup_groups_data_access()

        groups = self.groups_data_access.get_all()

        self.assertGreater(len(groups),0)

class ProductionDataAccessTest(unittest.TestCase):
    productiondb = None
    dbsetup = DbSetup()

    def setup_db(self):
        self.dbsetup.setup_database()
        self.productiondb = self.dbsetup.newdb

    def setup_production_data_access(self):
        shelveDatabase = ShelveDataBaseManager(dblocation)
        self.production_data_access = ShelveProductionBatchDataAccess(shelveDatabase)

    def setup_production_batches(self):
        self.productionbatch1 = ProductionBatch("Bread", 3, "2020-01-01", "10:00 AM", "Ramon")
        self.productionbatch2 = ProductionBatch("Bread", 3, "2020-01-07", "11:00 AM", "Remi")

    def save_production_batches(self):
        self.setup_db()
        self.setup_production_batches()
        self.setup_production_data_access()

        self.savedproductionbatch1 = self.production_data_access.save(self.productionbatch1)
        self.savedproductionbatch2 = self.production_data_access.save(self.productionbatch2)

    def test_save_production_batch(self):
        self.save_production_batches()
        #self.assertEqual(1,self.savegroup1.id)
        self.assertEqual("Ramon", self.productionbatch1.baker)
        self.assertEqual("Remi", self.productionbatch2.baker)
    
    def test_get_production_batches(self):
        self.setup_db()
        self.setup_production_batches()
        self.setup_production_data_access()

        production_batches = self.production_data_access.get_all()

        self.assertGreater(len(production_batches),0)
    
    def test_get_production_batch(self):
        self.save_production_batches()

        production_batch = self.production_data_access.get_production_batch("2020-01-01", self.savedproductionbatch1.id)

        self.assertEqual("2020-01-01", production_batch.date)

    def test_get_day_production_batches(self):
        self.save_production_batches()

        production_batches = self.production_data_access.get_day_production_batches("2020-01-01")

        for batch in production_batches:
            self.assertEqual("2020-01-01", batch.date)