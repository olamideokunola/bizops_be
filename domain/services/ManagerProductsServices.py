
from abc import ABC, abstractmethod
from datetime import date

from domain.products.Products import Product, Price
from domain.products.Units import Unit
from domain.products.ProductsDataAccessInterface import ProductsDataAccessInterface
from domain.products.UnitsDataAccessInterface import UnitsDataAccessInterface

# an interface for manager products interactor input boundary interface
class ManagerProductsInputInterface(ABC):
    @abstractmethod
    def create_product(self):
        pass

    @abstractmethod
    def update_product(self):
        pass

    @abstractmethod
    def get_product(self):
        pass

    @abstractmethod
    def get_products(self):
        pass

    @abstractmethod
    def create_unit(self):
        pass

    @abstractmethod
    def update_unit(self):
        pass

    @abstractmethod
    def get_unit(self):
        pass

    @abstractmethod
    def get_units(self):
        pass

# an interface for manager product interactor output boundary interface
class ManagerProductOutputInterface(ABC):
    @abstractmethod
    def set_product(self, managerProductOutputData):
        pass

    @abstractmethod
    def set_products(self, managerProductOutputData):
        pass

    @abstractmethod
    def set_unit(self, managerProductOutputData):
        pass

    @abstractmethod
    def set_units(self, managerProductOutputData):
        pass

    @abstractmethod
    def set_feedback(self, managerProductOutputData):
        pass

class ManagerProductInputData():
    productid = None
    name = None
    group = None
    unitid = None
    unitShortDesc = ''
    unitLongDesc = ''
    unitActive = None
    active = None
    unit = None
    units = None
    price = None
    prices = None
    date = None
    feedback = None

class ManagerProductOutputData():
    products = []
    product = Product()
    units = []
    unit = None
    unitid = None
    feedback = None

# a class for MangerProductsService
class ManagerManageProductsService(ManagerProductsInputInterface):
    product = None
    products = []
    productsDataAccess = None
    unitsDataAccess = None
    managerProductPresenter = None
    managerProductInputData = ManagerProductInputData()
    managerProductOutputData = ManagerProductOutputData()

    def __init__(self, productsDataAccess, unitsDataAccess, managerProductInputData, managerProductOutputData, managerProductOutputInterfaceObject):
        if isinstance(productsDataAccess, ProductsDataAccessInterface):
            self.productsDataAccess = productsDataAccess
        
        if isinstance(unitsDataAccess, UnitsDataAccessInterface):
            self.unitsDataAccess = unitsDataAccess

        if isinstance(managerProductOutputInterfaceObject, ManagerProductOutputInterface):
            self.managerProductPresenter = managerProductOutputInterfaceObject

        self.managerProductInputData = managerProductInputData

        self.managerProductOutputData = managerProductOutputData

    def delete_product(self):
        # Get product
        if self.managerProductInputData.productid != None:
            self.product = self.productsDataAccess.get(self.managerProductInputData.productid)
            # Delete
            deletedproduct = self.productsDataAccess.delete(self.product)
            products = self.productsDataAccess.get_products()
            self.managerProductOutputData.product = deletedproduct
            self.managerProductPresenter.set_product(self.managerProductOutputData)
            
            # also add products to the view model
            self.get_products()

    def delete_all_products(self):
        # Get product

        products = self.productsDataAccess.get_products()

        for product in products:
            self.productsDataAccess.delete(product)

        self.managerProductOutputData.products = self.productsDataAccess.get_products()
        self.managerProductPresenter.set_products(self.managerProductOutputData)

    def get_product(self):
        self.managerProductOutputData.product = self.productsDataAccess.get_product(id=self.managerProductInputData.productid)
        self.managerProductPresenter.set_product(self.managerProductOutputData)

    def get_products(self):
        self.managerProductOutputData.products = self.productsDataAccess.get_products()
        self.managerProductPresenter.set_products(self.managerProductOutputData)

    def _get_units(self, units):
        unit_ids = [unit['id'] for unit in units] if units != None else None
        return self.unitsDataAccess.get_many(unit_ids)

    @staticmethod
    def _set_price(price):
        if isinstance(price, Price):
            return price
        elif isinstance(price, dict):
            return Price(
                fromDate=price['date'] if 'date' in  price else None,
                toDate=price['toDate'] if 'toDate' in  price else None,
                amount=price['price'] if 'price' in  price else None,
                currency=price['currency'] if 'currency' in  price else None,
                active=price['active'] if 'active' in  price else None,
            )

    def create_product(self):
        name = self.managerProductInputData.name
        group = self.managerProductInputData.group
        units = self.managerProductInputData.units
        price = self.managerProductInputData.price

        print('In create_product, name is: ' + name) 

        products = self.productsDataAccess.get_products()
        productNames = [ product.name for product in products ] if products != None else []

        print('In create_product, productNames are: ' + str(productNames)) 
        
        if name in productNames:
            print('Name exists') 
            self.managerProductOutputData.feedback = {
                    'status': 'Failure',
                    'message': 'Product name already exists!'
                }
            self.managerProductPresenter.set_feedback(self.managerProductOutputData)
 
        else:
            print('Name does not exist') 
            product = Product(name=name)
            product.group = group
            # unit_ids = [unit['id'] for unit in units] if units != None else None
            product.units = self._get_units(units)

            # set today's date for daysale
            product.date = date.today()

            # set price 
            product.price = self._set_price(price)
            # print('In create product product amount is', product.price.amount)

            print('In create product date is', product.date)

            # save new sale to database
            savedproduct = self.productsDataAccess.save(product)
            
            print('Product saved') 

            # if save is successful set output data (product) and format presenter view data
            if savedproduct != None:
                print('Product saved and confirmed')
                self.managerProductOutputData.product = savedproduct

                self.managerProductPresenter.set_product(self.managerProductOutputData)
                
                print('In Service, about to set Feedback')

                self.managerProductOutputData.feedback = {
                    'status': 'Success',
                    'message': 'Product created'
                }

                print('In service about to set feedback in Presenter: ' + str(self.managerProductOutputData.feedback))

                self.managerProductPresenter.set_feedback(self.managerProductOutputData)

                print('Feedback set')

    def update_product(self):
        print('product id is: ' + str(self.managerProductInputData.productid))
        if self.managerProductInputData.productid != None:
            product = self.productsDataAccess.get(self.managerProductInputData.productid)

        print('About to set product name')

        if self.managerProductInputData.productname != None: 
            product.name = self.managerProductInputData.productname

        print('About to set group')

        if self.managerProductInputData.group != None: 
            product.group = self.managerProductInputData.group

        print('About to set units')

        if self.managerProductInputData.units != None:
            product.units = self._get_units(self.managerProductInputData.units)

        print('About to set price')

        if self.managerProductInputData.price != None:
            product.price = self._set_price(self.managerProductInputData.price)
            print('In service price is, ', product.price )

        print('About to add prices')

        if self.managerProductInputData.prices != None:
            product.prices = []
            for price in self.managerProductInputData.prices:
                product.add_price(
                    fromDate = self.format_date(price['date']),
                    amount = price['price'],
                    active = price['active']
                )

        # save product to database
        savedproduct = self.productsDataAccess.save(product)

        # if save is successful set output data (product and products) and format presenter view data
        self.managerProductOutputData.product = savedproduct
        self.managerProductOutputData.products = self.productsDataAccess.get_products()
        self.managerProductPresenter.set_product(self.managerProductOutputData)
        self.managerProductPresenter.set_products(self.managerProductOutputData)

    def format_date(self, inputdate):
        dateElements = inputdate.split('-')
        return date(int(dateElements[0]), int(dateElements[1]), int(dateElements[2]))

    def create_unit(self):
        shortDesc = self.managerProductInputData.unitShortDesc
        longDesc = self.managerProductInputData.unitLongDesc
        active = self.managerProductInputData.active

        unit = Unit(shortDesc=shortDesc, longDesc=longDesc, active=active)

        # save new unit to database
        savedunit = self.unitsDataAccess.save(unit)

        # if save is successful set output data (product) and format presenter view data
        if savedunit != None:
            self.managerProductOutputData.unit = savedunit

            self.managerProductPresenter.set_unit(self.managerProductOutputData)

    def delete_unit(self):
        # Get unit
        if self.managerProductInputData.unitid != None:
            self.unit = self.unitsDataAccess.get(self.managerProductInputData.unitid)
            # Delete
            deletedunit = self.unitsDataAccess.delete(self.unit)
            self.managerProductOutputData.unit = deletedunit
            self.managerProductPresenter.set_unit(self.managerProductOutputData)

    def delete_all_units(self):
        # Get unit

        units = self.unitsDataAccess.get_units()

        for unit in units:
            self.unitsDataAccess.delete(unit)

        try:
            self.managerProductOutputData.units = self.unitsDataAccess.get_units()
            self.managerProductPresenter.set_units(self.managerProductOutputData)
        except TypeError:
            self.managerProductOutputData.feedback = {
                    'status': 'Success',
                    'message': 'No units in database'
                }
            self.managerProductPresenter.set_feedback(self.managerProductOutputData)
    
    def update_unit(self):
        print('In Service Unit id is: ' +  str(self.managerProductInputData.unitid))
        print('In Service Unit active is: ' +  str(self.managerProductInputData.unitActive))
        if self.managerProductInputData.unitid != None:
            unit = self.unitsDataAccess.get(self.managerProductInputData.unitid)

        if self.managerProductInputData.unitShortDesc != None: 
            unit.shortDesc = self.managerProductInputData.unitShortDesc

        if self.managerProductInputData.unitLongDesc != None: 
            unit.longDesc = self.managerProductInputData.unitLongDesc

        if self.managerProductInputData.unitActive != None: 
            unit.active = self.managerProductInputData.unitActive

        # save unit to database
        savedunit = self.unitsDataAccess.save(unit)

        # if save is successful set output data (unit and units) and format presenter view data
        self.managerProductOutputData.unit = savedunit
        self.managerProductOutputData.units = self.unitsDataAccess.get_units()
        self.managerProductPresenter.set_unit(self.managerProductOutputData)
        self.managerProductPresenter.set_units(self.managerProductOutputData)

    def get_unit(self):
        self.managerProductOutputData.unit = self.unitsDataAccess.get_unit(self.managerProductInputData.unitid)
        self.managerProductPresenter.set_unit(self.managerProductOutputData)

    def get_units(self):
        self.managerProductOutputData.units = self.unitsDataAccess.get_units()
        self.managerProductPresenter.set_units(self.managerProductOutputData)

    def add_price(self):
        # get product

        id = self.managerProductInputData.productid
        product = self.productsDataAccess.get(id)
        
        # add price
        product.add_price(
            fromDate = self.format_date(self.managerProductInputData.pricedate),
            amount = self.managerProductInputData.amount,
            active = self.managerProductInputData.active
        )

        print('In service Add price, price is', product.price.fromDate,product.price.amount,product.price.active)

        # save product to database
        savedproduct = self.productsDataAccess.save(product)

        print('product saved')

        # set output
        self.managerProductOutputData.product = savedproduct
        self.managerProductPresenter.set_product(self.managerProductOutputData)

    def add_prices(self):
        # get product
        print('In add prices', self.managerProductInputData.productid)
        prices = self.managerProductInputData.prices
        defaultPrice = self.managerProductInputData.defaultPrice
        id = self.managerProductInputData.productid
        product = self.productsDataAccess.get(id)
        
        print('about to add prices')
        # add prices
        for price in prices:
            product.add_price(
                fromDate = self.format_date(price["date"]),
                amount = price["price"],
                active = price["active"]
            )
        
        print('about to set default price')
        # set default price
        product.set_default_price(
                fromDate = self.format_date(defaultPrice["date"]),
                amount = defaultPrice["price"],
                active = defaultPrice["active"]
            )

        print('about to save product')
        # save product to database
        savedproduct = self.productsDataAccess.save(product)

        print('about to set product price output')
        # set output
        self.managerProductOutputData.product = savedproduct
        self.managerProductPresenter.set_product(self.managerProductOutputData)