from domain.services.ManagerProductsServices import ManagerProductsInputInterface, ManagerProductInputData
import datetime

class ManagerProductServiceController:
    managerProductService = ManagerProductsInputInterface
    managerProductInputData = ManagerProductInputData()

    def __init__(self, managerProductInputData, managerProductService):
        self.managerProductInputData = managerProductInputData
        if isinstance(managerProductService, ManagerProductsInputInterface):
            self.managerProductService = managerProductService
    
    def get_product(self, id):
        self.managerProductInputData.productid = id
        self.managerProductService.get_product()

    def get_products(self):
        self.managerProductService.get_products()

    def create_product(self, name, group, date, units):
        self.managerProductInputData.name = name
        self.managerProductInputData.group = group
        self.managerProductInputData.units = units

        # date is expected as a dictionary
        self.managerProductInputData.date = datetime.date(date['year'], date['month'], date['day'])

        self.managerProductService.create_product()

    def update_product(self, productid, name, group, units, prices):
        print('In Controller, product id is: ' + str(productid))
        self.managerProductInputData.productid=productid
        self.managerProductInputData.productname=name
        self.managerProductInputData.group=group
        self.managerProductInputData.units=units
        self.managerProductInputData.prices=prices

        self.managerProductService.update_product()

    def delete_product(self, productid):
        self.managerProductInputData.productid = productid
        self.managerProductService.delete_product()
    
    def delete_all_products(self):
        self.managerProductService.delete_all_products()

    def add_prices(self, productid, prices, defaultPrice):
        self.managerProductInputData.productid = productid
        self.managerProductInputData.prices=prices
        self.managerProductInputData.defaultPrice=defaultPrice

        self.managerProductService.add_prices()

    def add_price(self, productid, pricedate, amount, active):
        self.managerProductInputData.productid=productid
        self.managerProductInputData.pricedate=pricedate
        self.managerProductInputData.amount=amount
        self.managerProductInputData.active=active

        self.managerProductService.add_price()

    def get_unit(self, id):
        self.managerProductInputData.unitid = id
        self.managerProductService.get_unit()

    def get_units(self):
        self.managerProductService.get_units()

    def create_unit(self, shortDesc, longDesc, active):
        self.managerProductInputData.unitShortDesc = shortDesc
        self.managerProductInputData.unitLongDesc = longDesc
        self.managerProductInputData.active = active

        self.managerProductService.create_unit()

    def update_unit(self, unitid, shortDesc, longDesc, active):
        print('In Controller, unit id is: ' + str(unitid))
        print('In Controller, unit active is: ' + str(active))
        self.managerProductInputData.unitid=unitid
        self.managerProductInputData.unitShortDesc = shortDesc
        self.managerProductInputData.unitLongDesc = longDesc
        self.managerProductInputData.unitActive = active

        self.managerProductService.update_unit()

    def delete_unit(self, unitid):
        self.managerProductInputData.unitid = unitid
        self.managerProductService.delete_unit()

    def delete_all_units(self):
        self.managerProductService.delete_all_units()