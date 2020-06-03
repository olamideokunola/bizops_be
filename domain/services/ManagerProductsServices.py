
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
    def set_feedback(self, managerSaleOutputData):
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

class ManagerProductOutputData():
    products = []
    product = Product()
    units = []
    unit = None
    unitid = None

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

    def create_product(self):
        name = self.managerProductInputData.name
        group = self.managerProductInputData.group
        units = self.managerProductInputData.units

        products = self.productsDataAccess.get_products()
        productNames = [ product.name for product in products ] 
        
        if name in productNames:
            self.managerProductOutputData.feedback = {
                    'status': 'Failure',
                    'message': 'Product name already exists!'
                }
            self.managerProductPresenter.set_feedback(self.managerProductOutputData)

        else:
            
            product = Product(name=name)
            product.group = group
            product.units = units

            # set today's date for daysale
            product.date = date.today()

            # save new sale to database
            savedproduct = self.productsDataAccess.save(product)

            # if save is successful set output data (product) and format presenter view data
            if savedproduct != None:
                self.managerProductOutputData.product = savedproduct

                self.managerProductPresenter.set_product(self.managerProductOutputData)

                self.managerProductOutputData.feedback = {
                    'status': 'Success',
                    'message': 'Product created'
                }

    def update_product(self):
        print('product id is: ' + str(self.managerProductInputData.productid))
        if self.managerProductInputData.productid != None:
            product = self.productsDataAccess.get(self.managerProductInputData.productid)

        if self.managerProductInputData.productname != None: 
            product.name = self.managerProductInputData.productname

        if self.managerProductInputData.group != None: 
            product.group = self.managerProductInputData.group

        if self.managerProductInputData.units != None:
            product.units = self.managerProductInputData.units

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

        self.managerProductOutputData.units = self.unitsDataAccess.get_units()
        self.managerProductPresenter.set_units(self.managerProductOutputData)

    
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

        # save product to database
        savedproduct = self.productsDataAccess.save(product)

        # set output
        self.managerProductOutputData.product = savedproduct
        self.managerProductPresenter.set_product(self.managerProductOutputData)

    def add_prices(self):
        # get product
        prices = self.managerProductInputData.prices
        defaultPrice = self.managerProductInputData.defaultPrice
        id = self.managerProductInputData.productid
        product = self.productsDataAccess.get(id)
        
        # add prices
        for price in prices:
            product.add_price(
                fromDate = self.format_date(price["date"]),
                amount = price["price"],
                active = price["active"]
            )
        
        # set default price
        product.set_default_price(
                fromDate = self.format_date(defaultPrice["date"]),
                amount = defaultPrice["price"],
                active = defaultPrice["active"]
            )

        # save product to database
        savedproduct = self.productsDataAccess.save(product)

        # set output
        self.managerProductOutputData.product = savedproduct
        self.managerProductPresenter.set_product(self.managerProductOutputData)