from domain.services.ManagerSalesServices import ManagerSaleInputInterface, ManagerSaleInputData
import datetime

class ManagerSaleServiceController:
    managerSaleService = ManagerSaleInputInterface
    managerSaleInputData = ManagerSaleInputData()

    def __init__(self, managerSaleInputData, managerSaleService):
        self.managerSaleInputData = managerSaleInputData
        if isinstance(managerSaleService, ManagerSaleInputInterface):
            self.managerSaleService = managerSaleService

    def add_day_sale(self, productid, quantity, price, date, customerid, creator, authorizations, groups):
        
        self.managerSaleInputData.productid = productid
        self.managerSaleInputData.quantity = quantity
        self.managerSaleInputData.price = price

        print('In controller, add_day_sale! date is' + str(date))

        # date is expected as a dictionary
        self.managerSaleInputData.date = datetime.date(date['year'], date['month'], date['day'])

        print('In controller, add_day_sale!')

        self.managerSaleInputData.customerid = customerid
        self.managerSaleInputData.creator = creator

        self.managerSaleInputData.authorizations = authorizations
        self.managerSaleInputData.groups = groups

        self.managerSaleService.add_day_sale()

    def delete_sale(self, saleid):
        self.managerSaleInputData.saleid = saleid
        self.managerSaleService.delete_sale()

    def delete_all_sales(self):
        self.managerSaleService.delete_all_sales()

    def update_sale(self, saleid, productid, quantity, price, date, customerid):
        self.managerSaleInputData.saleid = saleid
        self.managerSaleInputData.productid = productid
        self.managerSaleInputData.quantity = quantity
        self.managerSaleInputData.price = price

        # date is expected as a dictionary
        #self.managerSaleInputData.date = datetime.date(date['year'], date['month'], date['day'])
        
        self.managerSaleInputData.customerid = customerid

        self.managerSaleService.update_sale()

    def get_sale(self, saleid):
        self.managerSaleInputData.saleid = saleid
        self.managerSaleService.get_sale()
    
    def get_day_sales(self, date):
        self.managerSaleInputData.date = date
        self.managerSaleService.get_day_sales()

    def get_month_sales(self, year, month):
        self.managerSaleInputData.year = year
        self.managerSaleInputData.month = month
        self.managerSaleService.get_month_sales()

    def get_sales(self):
        self.managerSaleService.get_sales()
    
    def get_customers(self):
        self.managerSaleService.get_customers()
    
    def get_products(self):
        self.managerSaleService.get_products()

    def create_product(self, name, group, date, units):
        self.managerSaleInputData.name = name
        self.managerSaleInputData.group = group
        self.managerSaleInputData.units = units

        # date is expected as a dictionary
        self.managerSaleInputData.date = datetime.date(date['year'], date['month'], date['day'])

        self.managerSaleService.create_product()