import unittest
import datetime

from domain.sales.Sales import Sale
#from domain.services.ManagerSalesServices import ManagerManageSalesService
from domain.dataAccess.SalesDataAccess import ShelveSalesDataAccess as SalesDataAccess
from domain.sales.SalesDataAccessInterface import SalesDataAccessInterface
from domain.products.ProductsDataAccessInterface import ProductsDataAccessInterface
from domain.customers.CustomersDataAccessInterface import CustomersDataAccessInterface

from domain.products.Products import Price, Product

from domain.customers.Party import Person
from domain.customers.Customers import Customer

""" 
class SaleDataAccessTest(unittest.TestCase):
    salesDataAccess = SalesDataAccess()
    sale = None

    def setup_sale(self):
        saleEntityTest = SaleEntityTest()
        self.sale = saleEntityTest.setup_sale()

    def test_get_new_id(self):
        self.assertEqual(1, self.salesDataAccess.get_new_id())

    def test_save_day_sale(self):
        self.setup_sale()
        response = self.salesDataAccess.save_day_sale(self.sale)
        self.assertEqual('Success', response['status'])
        self.assertEqual(2000, response['result'].amount())
        self.assertEqual(datetime.date.today(), response['result'].date)
    
    def test_day_sales(self):
        self.setup_sale()
        self.salesDataAccess.save_day_sale(self.sale)
        daysales = self.salesDataAccess.day_sales()
        self.assertGreater(len(daysales), 0)
 """
class SaleEntityTest(unittest.TestCase):
    sale = Sale()

    def setup_sale(self):
        self.sale = Sale(
            product = {'id': 1, 'name': 'Loaf', 'price': 200},
            quantity = 10,
            price=200,
            currency = 'NGN'
        )
        return self.sale 

    def test_new_sale(self):
        self.setup_sale()
        self.assertEqual('Loaf', self.sale.product['name'])
        self.assertEqual(2000, self.sale.amount())


class ProductAndPriceEntityTest(unittest.TestCase):
    price = Price()
    product = Product()

    def setup_price(self):
        self.price = Price(
            fromDate = datetime.date(2019,1,1),
            amount = 100,
            currency = 'NGN'
        )
        return self.price 

    def setup_product(self, **args):
        if 'prices' in args:
            prices = args['prices'] 
        else:
            prices = None

        if 'name' in args:
            name = args['name'] 
        else:
            name = None

        self.product = Product(
            name = args['name'],
            prices = prices
        )
        return self.product 

    def test_new_price(self):
        self.setup_price()
        self.assertEqual(100, self.price.amount)
        self.assertEqual('NGN', self.price.currency)

    def test_new_product(self):
        self.setup_product(name='Bread')
        self.assertEqual('Bread', self.product.name)

    def test_add_price(self):
        self.setup_product(name='Bread', price=300)
        self.product.add_price(amount=200, fromDate=datetime.date(2019,1,1), currency='NGN')
        self.assertGreater(len(self.product.prices), 0)

class PersonEntityTest(unittest.TestCase):
    person = None

    def setup_person(self):
        self.person = Person('dammy', 'okunola')

    def test_new_person(self):
        self.setup_person()
        address = '1, Hamshire Road, Copan Hangen, USSR'
        website = 'www.myownsite.com'
        email = 'me@email.com'
        phonenumber = '08012345678'

        self.person.set_website(website)
        self.person.set_address(address)
        self.person.set_email(email)
        self.person.add_phonenumber(phonenumber)

        self.assertEqual('dammy', self.person.firstname)
        self.assertEqual('dammy okunola', self.person.get_name())
        self.assertEqual(address, self.person.get_address())
        self.assertEqual(website, self.person.get_website())
        self.assertEqual(email, self.person.get_email())
        self.assertGreater(len(self.person.get_phonenumbers()), 0)

class CustomerEntityTest(unittest.TestCase):
    customer = None
    name = 'Mummy Daniel'

    def setup_customer(self):
        self.customer = Customer(self.name)
        
        self.address = '1, Hamshire Road, Copan Hangen, USSR'
        self.website = 'www.myownsite.com'
        self.email = 'me@email.com'
        self.phonenumber = '08012345678'

        self.customer.set_website(self.website)
        self.customer.set_address(self.address)
        self.customer.set_email(self.email)
        self.customer.add_phonenumber(self.phonenumber)

    def setup_contact_person(self):
        self.contact_person_firstname = 'John'
        self.contact_person_lastname = 'Nash'
        self.contact_person_phonenumber = '08012345678'
        self.contact_person_address = '1, Hamshire Road, Copan Hangen, USSR'
        self.contact_person_website = 'www.myownsite.com'
        self.contact_person_email = 'me@email.com'

        self.customer.add_contact_person(
            self.contact_person_firstname, 
            self.contact_person_lastname, 
            phonenumber=self.contact_person_phonenumber,
            address=self.contact_person_address,
            website=self.contact_person_website,
            email=self.contact_person_email,
            )   

    def test_new_customer(self):
        self.setup_customer()
    
        self.assertEqual(self.name, self.customer.get_name())
        self.assertEqual(self.address, self.customer.get_address())
        self.assertEqual(self.website, self.customer.get_website())
        self.assertEqual(self.email, self.customer.get_email())
        self.assertGreater(len(self.customer.get_phonenumbers()), 0)

    def test_add_customer_contact_person(self):
        self.setup_customer()
        self.setup_contact_person()

        self.assertGreater(len(self.customer.contact_persons), 0)
        self.assertEqual(self.contact_person_firstname, self.customer.contact_persons[0].firstname)
        self.assertEqual(self.contact_person_email, self.customer.contact_persons[0].get_email())
        self.assertEqual(self.contact_person_address, self.customer.contact_persons[0].get_address())
        #self.assertEqual(self.contact_person_phonenumber, self.customer.contact_persons[0].get_phonenumbers()[1])

