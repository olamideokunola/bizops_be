
from abc import ABC, abstractmethod
from datetime import date
from calendar import Calendar

from domain.sales.Sales import Sale
from domain.products.Products import Product, Price
from domain.products.Units import Unit
from domain.products.ProductsDataAccessInterface import ProductsDataAccessInterface
from domain.products.UnitsDataAccessInterface import UnitsDataAccessInterface
from domain.customers.CustomersDataAccessInterface import CustomersDataAccessInterface
from domain.sales.SalesDataAccessInterface import SalesDataAccessInterface

from domain.services.ServiceUtils import date_is_yesterday_or_today

from .ManagerProductsServices import ManagerManageProductsService

# an interface for manager sales interactor input boundary interface
class ManagerSaleInputInterface(ABC):
    @abstractmethod
    def add_day_sale(self):
        pass

    @abstractmethod
    def update_sale(self):
        pass

    @abstractmethod
    def get_sale(self):
        pass
    
    @abstractmethod
    def get_day_sales(self):
        pass
    
    @abstractmethod
    def get_customers(self):
        pass


# an interface for manager sales interactor output boundary interface
class ManagerSaleOutputInterface(ABC):
    @abstractmethod
    def set_sale(self, managerSaleOutputData):
        pass

    @abstractmethod
    def set_day_sales(self, managerSaleOutputData):
        pass

    @abstractmethod
    def set_customers(self, managerSaleOutputData):
        pass

    @abstractmethod
    def set_products(self, managerSaleOutputData):
        pass

    @abstractmethod
    def set_feedback(self, managerSaleOutputData):
        pass


class ManagerSaleInputData():
    productid = None
    quantity = None
    price = None
    customerid = None
    date = None
    saleid = None
    groups = []
    creator = None

class ManagerSaleOutputData():
    sale = Sale()
    products = []
    customers = []
    sales = []
    daysales = []
    product = Product()
    monthsales = []
    user = None

# a class for MangerSalesService
class ManagerManageSalesService(ManagerSaleInputInterface):
    sale = None
    sales = []
    productsDataAccess = None
    customersDataAccess = None
    salesDataAccess = None
    managerSalePresenter = None
    managerSaleInputData = ManagerSaleInputData()
    managerSaleOutputData = ManagerSaleOutputData()

    def __init__(self, productsDataAccess, customersDataAccess, salesDataAccess, managerSaleInputData, managerSaleOutputData, managerSaleOutputInterfaceObject):
        if isinstance(productsDataAccess, ProductsDataAccessInterface):
            self.productsDataAccess = productsDataAccess
        
        if isinstance(customersDataAccess, CustomersDataAccessInterface):
            self.customersDataAccess = customersDataAccess

        if isinstance(salesDataAccess, SalesDataAccessInterface):
            self.salesDataAccess = salesDataAccess

        if isinstance(managerSaleOutputInterfaceObject, ManagerSaleOutputInterface):
            self.managerSalePresenter = managerSaleOutputInterfaceObject

        self.managerSaleInputData = managerSaleInputData

        self.managerSaleOutputData = managerSaleOutputData

    def __create_sale(self):
        # create empty sale
        self.sale = Sale()

        print('In create sale!')
        print('In create sale!, productid is: ' + str(self.managerSaleInputData.productid))


        # get product and customer from database using the ids
        product = self.productsDataAccess.get_product(self.managerSaleInputData.productid)
        
        print('Customer id is ', self.managerSaleInputData.customerid)

        if self.managerSaleInputData.customerid != None:
            customer = self.customersDataAccess.get_customer(self.managerSaleInputData.customerid) 
            print('Customer is', customer)
        else:
            customer = None
        
        # print('Customer is ', customer.id)

        # associate products and customers and set attributes quantity and price
        self.sale.product = product
        self.sale.customer = customer
        self.sale.quantity = self.managerSaleInputData.quantity
        self.sale.price = self.managerSaleInputData.price

        self.sale.creator = self.managerSaleInputData.creator

        self.sale.date = self.managerSaleInputData.date

        # save new sale to database
        print('sale price is ', self.sale.price)
        newsale = self.salesDataAccess.save(self.sale)

        # if save is successful set output data (sale and day sales) and format presenter view data
        if newsale != None:
            self.managerSaleOutputData.feedback = {
                    'status': 'Success',
                    'message': 'DaySale created'
                }
            self.managerSaleOutputData.sale = newsale
            self.managerSaleOutputData.daysales = self.salesDataAccess.get_day_sales(self.sale.date)

            print('day sales received')
            print('daysales are', self.managerSaleOutputData.daysales)

            self.managerSalePresenter.set_sale(self.managerSaleOutputData)
            self.managerSalePresenter.set_day_sales(self.managerSaleOutputData)
            self.managerSalePresenter.set_feedback(self.managerSaleOutputData)

            print('day sales set in presenter')

    def add_day_sale(self):
        print('In add_day_dale!')
        # Check the current date and compare to the date entered
        inputDate = self.managerSaleInputData.date

        print('inputDate is: ' + str(inputDate))

        # todayStr = "{}-{}-{}".format(date.today().year, date.today().month, date.today().day)
        inputDate =  '{:%Y-%m-%d}'.format(self.managerSaleInputData.date)
        todayStr = '{:%Y-%m-%d}'.format(date.today())
        print('todayStr is: ' + todayStr)

        # if inputDate == todayStr:
        #     print('Date is today')
        #     # create sale
        #     self.__create_sale()
        
        if date_is_yesterday_or_today(str(inputDate)):
            print('Date is today or yesterday')
            # create ProductionBatch
            self.__create_sale()
            
        else:
            # If date is not today, check if user is in manager_group, if return user can only save in the current day
            print('Date is not today')

            groups = self.managerSaleInputData.groups
            print('number of groups is: ' + str(len(groups)))

            groupnames = [ group['description'] for group in groups]

            print(str(groupnames))

            if len(groups) > 0 and 'manager_group' in groupnames:
                self.__create_sale()
            else:  
                self.managerSaleOutputData.sale = None
                self.managerSaleOutputData.feedback = {
                    'status': 'Failure',
                    'message': 'You can only save sale in the current day!'
                }
                self.managerSalePresenter.set_sale(self.managerSaleOutputData)
                self.managerSalePresenter.set_feedback(self.managerSaleOutputData)
    
    def delete_sale(self):
        # Get sale
        if self.managerSaleInputData.saleid != None:
            self.sale = self.salesDataAccess.get(self.managerSaleInputData.saleid)
            # Delete
            deletedsale = self.salesDataAccess.delete(self.sale)
            self.managerSaleOutputData.sale = deletedsale
            self.managerSalePresenter.set_sale(self.managerSaleOutputData)

    def delete_all_sales(self):
        # Get sales

        sales = self.salesDataAccess.get_sales()

        for sale in sales:
            self.salesDataAccess.delete(sale)

        self.managerSaleOutputData.sales = self.salesDataAccess.get_sales()
        self.managerSalePresenter.set_sales(self.managerSaleOutputData)

    def __update_sale(self):
        # Update sale
        if self.managerSaleInputData.productid != None:
            self.sale.product = self.productsDataAccess.get_product(self.managerSaleInputData.productid)
        
        if self.managerSaleInputData.quantity != None:
            self.sale.quantity = self.managerSaleInputData.quantity

        if self.managerSaleInputData.price != None:
            self.sale.price = self.managerSaleInputData.price
        
        if self.managerSaleInputData.customerid != None:
            self.sale.customer = self.customersDataAccess.get_customer(self.managerSaleInputData.customerid)
        
        if self.managerSaleInputData.date != None:
            self.sale.date =  self.managerSaleInputData.date
        
        # save new sale to database
        savedsale = self.salesDataAccess.save(self.sale)

        # if save is successful set output data (sale and day sales) and format presenter view data
        self.managerSaleOutputData.sale = savedsale
        self.managerSaleOutputData.daysales = self.salesDataAccess.get_day_sales(date.today())
        self.managerSalePresenter.set_sale(self.managerSaleOutputData)
        self.managerSalePresenter.set_day_sales(self.managerSaleOutputData)

    def update_sale(self):
        # Get sale
        if self.managerSaleInputData.saleid != None:
            self.sale = self.salesDataAccess.get(self.managerSaleInputData.saleid)
            date = self.sale.date

            print('Date is: ' + str(date))

            if date_is_yesterday_or_today(str(date)):
                print('Date is today or yesterday')
                # create ProductionBatch
                self.__update_sale()
        
            else:
                # If date is not today, check if user is in manager_group, if return user can only save in the current day
                print('Date is not today')

                groups = self.managerSaleInputData.groups
                print('number of groups is: ' + str(len(groups)))

                groupnames = [ group['description'] for group in groups]

                print(str(groupnames))

                if len(groups) > 0 and 'manager_group' in groupnames:
                    self.__update_sale()
                else:  
                    self.managerSaleOutputData.sale = None
                    self.managerSaleOutputData.feedback = {
                        'status': 'Failure',
                        'message': 'You can only save sale in the current day!'
                    }
                    self.managerSalePresenter.set_sale(self.managerSaleOutputData)
                    self.managerSalePresenter.set_feedback(self.managerSaleOutputData)

    def get_sale(self):
        self.managerSaleOutputData.sale = self.salesDataAccess.get_day_sale(id=self.managerSaleInputData.id)
        self.managerSalePresenter.set_sale(self.managerSaleOutputData)

    def get_day_sales(self):
        self.managerSaleOutputData.daysales = self.salesDataAccess.get_day_sales(date=self.managerSaleInputData.date)
        self.managerSalePresenter.set_day_sales(self.managerSaleOutputData)

    def get_month_sales(self):
        # self.managerSaleOutputData.monthsales = self.salesDataAccess.get_month_sales(
        #     year=self.managerSaleInputData.year,
        #     month=self.managerSaleInputData.month
        # )

        year=self.managerSaleInputData.year
        month=self.managerSaleInputData.month

        cal = Calendar(0)
        monthDays = cal.itermonthdates(year, month)
        
        self.managerSaleOutputData.monthsales = [ self.salesDataAccess.get_day_sales(monthDay) for monthDay in monthDays ]
 
        self.managerSalePresenter.set_month_sales(self.managerSaleOutputData)
  
    def get_sales(self):
        self.managerSaleOutputData.sales = self.salesDataAccess.get_sales()
        self.managerSalePresenter.set_sales(self.managerSaleOutputData)

    def get_customers(self):
        self.managerSaleOutputData.customers = self.customersDataAccess.get_customers()
        self.managerSalePresenter.set_customers(self.managerSaleOutputData)
