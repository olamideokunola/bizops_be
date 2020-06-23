import unittest
import datetime

from domain.sales.Sales import Sale
from domain.sales.SalesDataAccessInterface import SalesDataAccessInterface
from domain.dataAccess.ShelveDatabase import ShelveDataBaseManager, Database
from domain.dataAccess.SalesDataAccess import ShelveSalesDataAccess

from domain.products.Products import Product, Price
from domain.products.ProductsDataAccessInterface import ProductsDataAccessInterface
from domain.dataAccess.ProductsDataAccess import ShelveProductsDataAccess

from domain.customers.Customers import Customer, Person
from domain.customers.CustomersDataAccessInterface import CustomersDataAccessInterface
from domain.dataAccess.CustomersDataAccess import ShelveCustomersDataAccess

from domain.users.Users import Group, Authorization, User
from domain.users.GroupsDataAccessInterface import GroupsDataAccessInterface
from domain.dataAccess.GroupsDataAccess import ShelveGroupsDataAccess

from domain.products.Products import Unit
from domain.products.UnitsDataAccessInterface import UnitsDataAccessInterface
from domain.dataAccess.UnitsDataAccess import ShelveUnitsDataAccess

from domain.production.ProductionBatch import ProductionBatch
from domain.production.ProductionBatchDataAccessInterface import ProductionBatchDataAccessInterface
from domain.dataAccess.ProductionBatchDataAccess import ShelveProductionBatchDataAccess

from domain.dataAccess.DjangoDataAccess.DjangoDatabase import DjangoDataBaseManager


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


djangoDbMgr = DjangoDataBaseManager('')

class DjangoDataBaseTest(unittest.TestCase):

    def setupDb(self):
        self.djangoDbMgr = djangoDbMgr
    
    def test_save(self):
        self.setupDb()

        price = Price(
            fromDate=None,
            toDate=None,
            amount=200,
            currency='NGN'
        )

        product = Product(
            name='Test Product 1',
            price=price
        )
        sale = Sale(
            product=product,
            price=price,
            quantity=2
        )

        savedSale = self.djangoDbMgr.save('','Sale',sale)

        if savedSale != None:
            print('savedSale is: ', savedSale)

        self.assertEqual(2, savedSale.quantity)

    def test_create_new_id(self):
        self.setupDb()
        newId = self.djangoDbMgr.create_new_id('','Sale')

        print(newId)

        self.assertIsNotNone(newId)

    def test_get(self):
        self.setupDb()
        sale = self.djangoDbMgr.get('','Sale',1)

        print(sale.id)

        self.assertEquals(1, sale.id)

class AuthorizationDjangoDataBaseModelManagerTest(unittest.TestCase):
    
    def test_create_new_id(self):
        
        newId = djangoDbMgr.create_new_id('','Authorization')

        print(newId)

        self.assertIsNotNone(newId)

    def test_create(self):
        auth = Authorization(
            model='Sale',
            description='Sale Authorization',
            create=True,
            change=False,
            view=True,
            delete=False,
        )
        savedAuth = djangoDbMgr.save('','Authorization', auth)

        print('savedAuth descriotion is: ' + savedAuth.description)

        self.assertIsNotNone(savedAuth)
        self.assertEqual(savedAuth.description, auth.description)
        self.assertTrue(savedAuth.view)
        self.assertFalse(savedAuth.delete)
        self.assertGreater(savedAuth.id,0)

    def test_get(self):
        id=5
        retrievedAuth = djangoDbMgr.get('','Authorization', id)

        self.assertIsNotNone(retrievedAuth)
        self.assertEqual(retrievedAuth.id,id)

    def test_update(self):
        auth = Authorization(
            id = 5,
            model='Sale',
            description='Sale Authorization changed',
            create=True,
            change=True,
            view=True,
            delete=True,
        )

        updatedAuth = djangoDbMgr.save('','Authorization', auth)

        self.assertIsNotNone(updatedAuth)
        self.assertTrue(updatedAuth.create)
        self.assertTrue(updatedAuth.change)
        self.assertTrue(updatedAuth.view)
        self.assertTrue(updatedAuth.delete)
        self.assertEqual(auth.id, updatedAuth.id)
        self.assertEqual(auth.description, updatedAuth.description)


    def test_getall(self):
        auths = djangoDbMgr.get_all('','Authorization')
        print('Number of items is: ', len(auths))

        for auth in auths:
            print ('auth is ', auth.description)

        self.assertGreater(len(auths), 1)

    def test_delete(self):
        items_pre = len(djangoDbMgr.get_all('','Authorization'))
        print('No of items before deletion: ', items_pre)
        
        itemtodelete = djangoDbMgr.get('','Authorization', 6)
        print('auth to delete is', itemtodelete.model)

        deletedAuth = djangoDbMgr.delete('', 'Authorization', itemtodelete)

        items_post = len(djangoDbMgr.get_all('','Authorization'))
        print('No of items after deletion: ', items_post)

        self.assertIsNotNone(deletedAuth)
        self.assertGreater(items_pre, items_post)

class GroupDjangoDataBaseModelManagerTest(unittest.TestCase):
    def test_create_new_id(self):
        
        newId = djangoDbMgr.create_new_id('','Group')

        print(newId)

        self.assertIsNotNone(newId)

    def test_create(self):
        grp = Group(
            description='SalesGroup',
            details='Group of salesmen',
        )

        grp.authorizations=[
                djangoDbMgr.get('','Authorization', 6),
                djangoDbMgr.get('','Authorization', 7)
            ]
        savedGrp = djangoDbMgr.save('','Group', grp)

        print('savedGrp descriotion is: ' + savedGrp.description)

        self.assertIsNotNone(savedGrp)
        self.assertEqual(savedGrp.description, grp.description)
        self.assertGreater(savedGrp.id,0)

    def test_get(self):
        id=3
        retrievedAuth = djangoDbMgr.get('','Group', id)

        self.assertIsNotNone(retrievedAuth)
        self.assertEqual(retrievedAuth.id,id)

    def test_update(self):
        grp = Group(
            description='SalesGroup changed',
            details='Group of salesmen changed',
        )

        grp.id = 5

        updatedGrp = djangoDbMgr.save('','Group', grp)

        self.assertIsNotNone(updatedGrp)
        self.assertEqual(grp.id, updatedGrp.id)
        self.assertEqual(grp.description, updatedGrp.description)


    def test_getall(self):
        grps = djangoDbMgr.get_all('','Group')
        print('Number of items is: ', len(grps))

        for grp in grps:
            print ('grp is ', grp.id, grp.description)

        self.assertGreater(len(grps), 1)

    def test_delete(self):
        items_pre = len(djangoDbMgr.get_all('','Group'))
        print('No of items before deletion: ', items_pre)
        
        itemtodelete = djangoDbMgr.get('','Group', 8)
        print('grp to delete is', itemtodelete.description)

        deletedAuth = djangoDbMgr.delete('', 'Group', itemtodelete)

        items_post = len(djangoDbMgr.get_all('','Group'))
        print('No of items after deletion: ', items_post)

        self.assertIsNotNone(deletedAuth)
        self.assertGreater(items_pre, items_post)

class PersonDjangoDataBaseModelManagerTest(unittest.TestCase):
    def test_create_new_id(self):
        newId = djangoDbMgr.create_new_id('','Person')

        print(newId)

        self.assertIsNotNone(newId)

    def test_create(self):
        person = Person(
            firstname='John',
            lastname='Nash',
            middlename='Jones',
        )

        savedPerson = djangoDbMgr.save('','Person', person)

        print('savedPerson firstname is: ' + savedPerson.firstname)

        self.assertIsNotNone(savedPerson)
        self.assertEqual(savedPerson.firstname, person.firstname)
        self.assertGreater(savedPerson.id,0)

    def test_get(self):
        id=1
        retrievedItem = djangoDbMgr.get('','Person', id)

        self.assertIsNotNone(retrievedItem)
        self.assertEqual(retrievedItem.id,id)

    def test_update(self):
        item = Person(
            firstname='John',
            lastname='Nash',
            middlename='Junior',
        )

        item.id = 1

        updatedItem = djangoDbMgr.save('','Person', item)

        self.assertIsNotNone(updatedItem)
        self.assertEqual(item.id, updatedItem.id)
        self.assertEqual(item.middlename, updatedItem.middlename)


    def test_getall(self):
        items = djangoDbMgr.get_all('','Person')
        print('Number of items is: ', len(items))

        for item in items:
            print ('grp is ', item.id, item.firstname, item.lastname)

        self.assertGreater(len(items), 0)

    def test_delete(self):
        items_pre = len(djangoDbMgr.get_all('','Person'))
        print('No of items before deletion: ', items_pre)
        
        itemtodelete = djangoDbMgr.get('','Person', 1)
        # print('grp to delete is', itemtodelete.firstname)

        deletedAuth = djangoDbMgr.delete('', 'Person', itemtodelete)

        items_post = len(djangoDbMgr.get_all('','Person'))
        print('No of items after deletion: ', items_post)

        self.assertIsNotNone(deletedAuth)
        self.assertGreater(items_pre, items_post)

class CustomerDjangoDataBaseModelManagerTest(unittest.TestCase):
    def test_create_new_id(self):
        newId = djangoDbMgr.create_new_id('','Customer')

        print(newId)

        self.assertIsNotNone(newId)

    def test_create(self):
        customer = Customer(
            name = 'Customer 1',
            email = 'customer1@email.com', 
            phonenumber = '080200000000', 
            address = '1 Customer Road', 
            date = datetime.date.today(), 
        )

        customer.contact_persons = [djangoDbMgr.get('','Person', 2), djangoDbMgr.get('','Person', 3)]

        savedCustomer = djangoDbMgr.save('','Customer', customer)

        print('savedCustomer firstname is: ' + savedCustomer.name)

        self.assertIsNotNone(savedCustomer)
        self.assertEqual(savedCustomer.name, customer.name)
        self.assertGreater(savedCustomer.id,0)

    def test_get(self):
        id=1
        retrievedItem = djangoDbMgr.get('','Customer', id)

        self.assertIsNotNone(retrievedItem)
        self.assertEqual(retrievedItem.id,id)

    def test_update(self):
        item = Customer(
            name = 'Customer 1 changed',
            email = 'customer1@email.com', 
            phonenumber = '080200000000', 
            address = '1 Customer Road', 
            date = datetime.date.today(), 
        )

        item.id = 1

        updatedItem = djangoDbMgr.save('','Customer', item)

        self.assertIsNotNone(updatedItem)
        self.assertEqual(item.id, updatedItem.id)
        self.assertEqual(item.name, updatedItem.name)


    def test_getall(self):
        items = djangoDbMgr.get_all('','Customer')
        print('Number of items is: ', len(items))

        for item in items:
            print ('item is ', item.id, item.get_name(), item.get_address())

        self.assertGreater(len(items), 1)

    def test_delete(self):
        items_pre = len(djangoDbMgr.get_all('','Customer'))
        print('No of items before deletion: ', items_pre)
        
        itemtodelete = djangoDbMgr.get('','Customer', 1)
        # print('grp to delete is', itemtodelete.firstname)

        deletedAuth = djangoDbMgr.delete('', 'Customer', itemtodelete)

        items_post = len(djangoDbMgr.get_all('','Customer'))
        print('No of items after deletion: ', items_post)

        self.assertIsNotNone(deletedAuth)
        self.assertGreater(items_pre, items_post)

class UnitDjangoDataBaseModelManagerTest(unittest.TestCase):
    def test_create_new_id(self):
        newId = djangoDbMgr.create_new_id('','Unit')

        print(newId)

        self.assertIsNotNone(newId)

    def test_create(self):
        unit = Unit(
            shortDesc = 'm',
            longDesc = 'meter', 
            active = True,
        )

        savedUnit = djangoDbMgr.save('','Unit', unit)

        print('savedUnit shortDesc is: ' + savedUnit.shortDesc)

        self.assertIsNotNone(savedUnit)
        self.assertEqual(savedUnit.shortDesc, unit.shortDesc)
        self.assertGreater(savedUnit.id,0)

    def test_get(self):
        id=2
        retrievedItem = djangoDbMgr.get('','Unit', id)

        self.assertIsNotNone(retrievedItem)
        self.assertEqual(retrievedItem.id,id)

    def test_update(self):
        item = Unit(
            shortDesc = 'm',
            longDesc = 'metre', 
            active = True,
        )

        item.id = 2

        updatedItem = djangoDbMgr.save('','Unit', item)

        self.assertIsNotNone(updatedItem)
        self.assertEqual(item.id, updatedItem.id)
        self.assertEqual(item.shortDesc, updatedItem.shortDesc)


    def test_getall(self):
        items = djangoDbMgr.get_all('','Unit')
        print('Number of items is: ', len(items))

        for item in items:
            print ('item is ', item.id, item.shortDesc, item.longDesc)

        self.assertGreater(len(items), 1)

    def test_delete(self):
        items_pre = len(djangoDbMgr.get_all('','Unit'))
        print('No of items before deletion: ', items_pre)
        
        itemtodelete = djangoDbMgr.get('','Unit', 2)
        # print('grp to delete is', itemtodelete.firstname)

        deletedAuth = djangoDbMgr.delete('', 'Unit', itemtodelete)

        items_post = len(djangoDbMgr.get_all('','Unit'))
        print('No of items after deletion: ', items_post)

        self.assertIsNotNone(deletedAuth)
        self.assertGreater(items_pre, items_post)

class PriceDjangoDataBaseModelManagerTest(unittest.TestCase):
    def test_create_new_id(self):
        newId = djangoDbMgr.create_new_id('','Price')

        print(newId)

        self.assertIsNotNone(newId)

    def test_create(self):
        price = Price(
            fromDate = datetime.date.today(),
            toDate = None, 
            amount = 300, 
            currency = 'NGN',
            active = False,
        )

        price.product = None

        savedPrice = djangoDbMgr.save('','Price', price)

        print('savedPrice shortDesc is: ', savedPrice.fromDate)

        self.assertIsNotNone(savedPrice)
        self.assertEqual(savedPrice.fromDate, price.fromDate)
        self.assertGreater(savedPrice.id,0)

    def test_get(self):
        id=4
        retrievedItem = djangoDbMgr.get('','Price', id)

        self.assertIsNotNone(retrievedItem)
        self.assertEqual(retrievedItem.id,id)

    def test_update(self):
        item = Price(
            fromDate = datetime.date.today(),
            toDate = datetime.date(datetime.date.today().year, 
                datetime.date.today().month,
                datetime.date.today().day+7), 
            amount = 300, 
            currency = 'NGN',
            active = True,
        )

        item.product = None

        item.id = 5

        updatedItem = djangoDbMgr.save('','Price', item)

        self.assertIsNotNone(updatedItem)
        self.assertEqual(item.id, updatedItem.id)
        self.assertEqual(item.toDate, updatedItem.toDate)


    def test_getall(self):
        items = djangoDbMgr.get_all('','Price')
        print('Number of items is: ', len(items))

        for item in items:
            print ('item is ', item.id, item.fromDate, item.currency)

        self.assertGreater(len(items), 1)

    def test_delete(self):
        items_pre = len(djangoDbMgr.get_all('','Price'))
        print('No of items before deletion: ', items_pre)
        
        itemtodelete = djangoDbMgr.get('','Price', 2)
        # print('grp to delete is', itemtodelete.firstname)

        deletedAuth = djangoDbMgr.delete('', 'Price', itemtodelete)

        items_post = len(djangoDbMgr.get_all('','Price'))
        print('No of items after deletion: ', items_post)

        self.assertIsNotNone(deletedAuth)
        self.assertGreater(items_pre, items_post)

class UserDjangoDataBaseModelManagerTest(unittest.TestCase):
    def test_create_new_id(self):
        newId = djangoDbMgr.create_new_id('','User')

        print(newId)

        self.assertIsNotNone(newId)

    def test_create(self):


        user = User(
            firstname = 'Jane',
            lastname = 'Doe', 
            username = 'jane', 
            password = 'allow',
            email = 'jane@email.com',
            phonenumber = '08020000000', 
        )

        user.authorizations = djangoDbMgr.get_all('','Authorization')
        user.groups = djangoDbMgr.get_all('','Group')

        savedUser = djangoDbMgr.save('','User', user)

        print('savedUser shortDesc is: ', savedUser.get_firstname())

        self.assertIsNotNone(savedUser)
        self.assertEqual(savedUser.get_firstname(), user.get_firstname())
        self.assertGreater(savedUser.id,0)

    def test_get(self):
        id=4
        retrievedItem = djangoDbMgr.get('','User', id)

        self.assertIsNotNone(retrievedItem)
        self.assertEqual(retrievedItem.id,id)

    def test_update(self):
        item = User(
            firstname = 'Jane',
            lastname = 'Dowen', 
            username = 'jane_dowen', 
            password = 'allow',
            email = 'jane@email.com',
            phonenumber = '08020000000', 
        )

        item.authorizations = djangoDbMgr.get_all('','Authorization')
        item.groups = djangoDbMgr.get_all('','Group')
        item.activate()

        item.id = 5

        updatedItem = djangoDbMgr.save('','User', item)

        self.assertIsNotNone(updatedItem)
        self.assertEqual(item.id, updatedItem.id)
        self.assertEqual(item.get_lastname(), updatedItem.get_lastname())
        self.assertTrue(item.get_active())


    def test_getall(self):
        items = djangoDbMgr.get_all('','User')
        print('Number of items is: ', len(items))

        for item in items:
            print ('item is ', item.id, item.get_firstname(), item.get_lastname(), item.authorizations)

        self.assertGreater(len(items), 1)

    def test_delete(self):
        items_pre = len(djangoDbMgr.get_all('','User'))
        print('No of items before deletion: ', items_pre)
        
        itemtodelete = djangoDbMgr.get('','User', 2)
        # print('grp to delete is', itemtodelete.firstname)

        deletedAuth = djangoDbMgr.delete('', 'User', itemtodelete)

        items_post = len(djangoDbMgr.get_all('','User'))
        print('No of items after deletion: ', items_post)

        self.assertIsNotNone(deletedAuth)
        self.assertGreater(items_pre, items_post)

class ProductDjangoDataBaseModelManagerTest(unittest.TestCase):
    def test_create_new_id(self):
        newId = djangoDbMgr.create_new_id('','Product')

        print(newId)

        self.assertIsNotNone(newId)

    def test_create(self):


        product = Product(
            name = '900g Sliced Bread',
            price = 600,
            prices = djangoDbMgr.get_all('','Price'),
            date = datetime.date.today(),
        )

        product.group = "Sliced Bread"
        product.units = djangoDbMgr.get_all('','Unit')

        savedProduct = djangoDbMgr.save('','Product', product)

        print('savedProduct name is: ', savedProduct.name)

        self.assertIsNotNone(savedProduct)
        self.assertEqual(savedProduct.name, product.name)
        self.assertGreater(savedProduct.id,0)

    def test_get(self):
        id=4
        retrievedItem = djangoDbMgr.get('','Product', id)

        self.assertIsNotNone(retrievedItem)
        self.assertEqual(retrievedItem.id,id)

    def test_update(self):
        item = Product(
            name = '1000g Sliced Bread',
            price = 900,
            prices = djangoDbMgr.get_all('','Price'),
            date = datetime.date.today(),
        )

        item.group = "Sliced Bread"
        item.units = djangoDbMgr.get_all('','Unit')

        item.id = 1

        updatedItem = djangoDbMgr.save('','Product', item)

        self.assertIsNotNone(updatedItem)
        self.assertEqual(item.id, updatedItem.id)
        self.assertEqual(item.name, updatedItem.name)


    def test_getall(self):
        items = djangoDbMgr.get_all('','Product')
        print('Number of items is: ', len(items))

        for item in items:
            print ('item is ', item.id, item.name, item.name)

        self.assertGreater(len(items), 1)

    def test_delete(self):
        items_pre = len(djangoDbMgr.get_all('','Product'))
        print('No of items before deletion: ', items_pre)
        
        itemtodelete = djangoDbMgr.get('','Product', 2)
        # print('grp to delete is', itemtodelete.firstname)

        deletedAuth = djangoDbMgr.delete('', 'Product', itemtodelete)

        items_post = len(djangoDbMgr.get_all('','Product'))
        print('No of items after deletion: ', items_post)

        self.assertIsNotNone(deletedAuth)
        self.assertGreater(items_pre, items_post)

class SaleDjangoDataBaseModelManagerTest(unittest.TestCase):
    def test_create_new_id(self):
        newId = djangoDbMgr.create_new_id('','Sale')

        print(newId)

        self.assertIsNotNone(newId)

    def test_create(self):

        sale = Sale(
            product = djangoDbMgr.get('','Product', 6),
            quantity = 20,
            price = 500,
            currency = 'NGN',
            date = datetime.date.today(),
            customer = djangoDbMgr.get('','Customer', 6),
            creator = djangoDbMgr.get('','User', 6),   
        )

        savedSale = djangoDbMgr.save('','Sale', sale)

        print('savedSale product is: ', savedSale.product)

        self.assertIsNotNone(savedSale)
        self.assertEqual(savedSale.product.name, sale.product.name)
        self.assertGreater(savedSale.id,0)

    def test_get(self):
        id=4
        retrievedItem = djangoDbMgr.get('','Sale', id)

        self.assertIsNotNone(retrievedItem)
        self.assertEqual(retrievedItem.id,id)

    def test_getdayitems(self):
        date = datetime.date(2020,6,datetime.date.today().day-1)
        items = djangoDbMgr.get_day_items('','Sale', date)

        print('Number of items is: ', len(items))

        for item in items:
            print ('item is ', item.id, item.product.name if item.product != None else None )

        self.assertGreater(len(items), 1)

    def test_getdayitem(self):
        date = datetime.date(2020,6,datetime.date.today().day-1)
        item = djangoDbMgr.get_day_item('','Sale', date, 12)

        print ('item is ', item.id, item.product.name if item.product != None else None )

        self.assertEqual(item.id, 12)

    def test_update(self):
        item = Sale(
            product = djangoDbMgr.get('','Product', 6),
            quantity = 300,
            price = 900,
            currency = 'NGN',
            date = datetime.date.today(),
            customer = djangoDbMgr.get('','Customer', 6),
            creator = djangoDbMgr.get('','User', 6),   
        )

        item.id = 3

        updatedItem = djangoDbMgr.save('','Sale', item)

        self.assertIsNotNone(updatedItem)
        self.assertEqual(item.id, updatedItem.id)
        self.assertEqual(item.product.name, updatedItem.product.name)


    def test_getall(self):
        items = djangoDbMgr.get_all('','Sale')
        print('Number of items is: ', len(items))

        for item in items:
            print ('item is ', item.id, item.product.name if item.product != None else None )

        self.assertGreater(len(items), 1)

    def test_delete(self):
        items_pre = len(djangoDbMgr.get_all('','Sale'))
        print('No of items before deletion: ', items_pre)
        
        itemtodelete = djangoDbMgr.get('','Sale', 2)
        # print('grp to delete is', itemtodelete.firstname)

        deletedAuth = djangoDbMgr.delete('', 'Sale', itemtodelete)

        items_post = len(djangoDbMgr.get_all('','Sale'))
        print('No of items after deletion: ', items_post)

        self.assertIsNotNone(deletedAuth)
        self.assertGreater(items_pre, items_post)

class ProductionBatchDjangoDataBaseModelManagerTest(unittest.TestCase):
    def test_create_new_id(self):
        newId = djangoDbMgr.create_new_id('','ProductionBatch')

        print(newId)

        self.assertIsNotNone(newId)

    def test_create(self):

        productionBatch = ProductionBatch(
            productType='', 
            flourQuantity=50, 
            date=datetime.date.today(), 
            startTime='', 
            baker='Ramon',  
        )

        productionBatch.endTime = ''
        productionBatch.supervisor = ''
        productionBatch.assistants = 'James, John'
        productionBatch.problems = 'No flour, No water'

        productionBatch.products = djangoDbMgr.get_all('', 'Product')

        savedProductionBatch = djangoDbMgr.save('','ProductionBatch', productionBatch)

        print('savedProductionBatch flourQuantity is: ', savedProductionBatch.flourQuantity)

        self.assertIsNotNone(savedProductionBatch)
        self.assertEqual(savedProductionBatch.flourQuantity, productionBatch.flourQuantity)
        self.assertGreater(savedProductionBatch.id,0)

    def test_get(self):
        id=4
        retrievedItem = djangoDbMgr.get('','ProductionBatch', id)

        self.assertIsNotNone(retrievedItem)
        self.assertEqual(retrievedItem.id,id)

    def test_update(self):
        item = ProductionBatch(
             productType='', 
            flourQuantity=50, 
            date=datetime.date.today(), 
            startTime=datetime.datetime.now(), 
            baker='Ramonilahi', 
        )

        item.endTime = datetime.datetime.now()
        item.supervisor = ''
        item.assistants = 'James, John'
        item.problems = 'No flour, No water'

        item.products = djangoDbMgr.get_all('', 'Product')

        item.id = 3

        updatedItem = djangoDbMgr.save('','ProductionBatch', item)

        self.assertIsNotNone(updatedItem)
        self.assertEqual(item.id, updatedItem.id)
        self.assertEqual(item.baker, updatedItem.baker)


    def test_getall(self):
        items = djangoDbMgr.get_all('','ProductionBatch')
        print('Number of items is: ', len(items))

        for item in items:
            print ('item is ', item.id, item.flourQuantity )

        self.assertGreater(len(items), 1)
    
    def test_getmany(self):
        ids = [1,3,4]
        items = djangoDbMgr.get_many('','ProductionBatch',ids)
        print('Number of items is: ', len(items))

        for item in items:
            print ('item is ', item.id, item.flourQuantity )

        self.assertGreater(len(items), 1)

    def test_delete(self):
        items_pre = len(djangoDbMgr.get_all('','ProductionBatch'))
        print('No of items before deletion: ', items_pre)
        
        itemtodelete = djangoDbMgr.get('','ProductionBatch', 2)
        # print('grp to delete is', itemtodelete.firstname)

        deletedAuth = djangoDbMgr.delete('', 'ProductionBatch', itemtodelete)

        items_post = len(djangoDbMgr.get_all('','ProductionBatch'))
        print('No of items after deletion: ', items_post)

        self.assertIsNotNone(deletedAuth)
        self.assertGreater(items_pre, items_post)

