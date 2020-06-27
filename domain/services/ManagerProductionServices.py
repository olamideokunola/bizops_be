
from abc import ABC, abstractmethod
from datetime import date, time
from calendar import Calendar

from domain.production.ProductionBatch import ProductionBatch
from domain.production.ProductionBatchDataAccessInterface import ProductionBatchDataAccessInterface

from domain.services.ServiceUtils import date_is_yesterday_or_today


# an interface for manager ProductionBatchs interactor input boundary interface
class ManagerProductionBatchInputInterface(ABC):
    @abstractmethod
    def add_day_production_batch(self):
        pass

    @abstractmethod
    def update_day_production_batch(self):
        pass

    @abstractmethod
    def get_day_production_batch(self):
        pass
    
    @abstractmethod
    def get_day_production_batches(self):
        pass

# an interface for manager sales interactor output boundary interface
class ManagerProductionBatchOutputInterface(ABC):
    @abstractmethod
    def set_production_batch(self, managerProductionBatchOutputData):
        pass
    
    @abstractmethod
    def set_production_batches(self, managerProductionBatchOutputData):
        pass

    @abstractmethod
    def set_day_production_batches(self, managerProductionBatchOutputData):
        pass

class ManagerProductionBatchInputData():
    productionbatchid = None
    productType=None
    flourQuantity=None
    date=None
    startTime=None
    endTime=None
    products=[]
    baker=None
    supervisor=None
    assistants=[]
    problems=[]
    groups=[]

class ManagerProductionBatchOutputData():
    productionbatch = ProductionBatch()
    productionbatches = []
    dayproductionbatches = []
    monthproductionbatches = []
    feedback = {}
    baker = ''

# a class for MangerSalesService
class ManagerManageProductionBatchService(ManagerProductionBatchInputInterface):
    productionbatch = None
    productionbatches = []
    productionBatchDataAccess = None
    managerProductionBatchPresenter = None
    managerProductionBatchInputData = ManagerProductionBatchInputData()
    managerProductionBatchOutputData = ManagerProductionBatchOutputData()

    def __init__(self, productionBatchDataAccess, managerProductionBatchInputData, managerProductionBatchOutputData, managerProductionBatchOutputInterfaceObject):
        if isinstance(productionBatchDataAccess, ProductionBatchDataAccessInterface):
            self.productionBatchDataAccess = productionBatchDataAccess

        if isinstance(managerProductionBatchOutputInterfaceObject, ManagerProductionBatchOutputInterface):
            self.managerProductionBatchPresenter = managerProductionBatchOutputInterfaceObject

        self.managerProductionBatchInputData = managerProductionBatchInputData

        self.managerProductionBatchOutputData = managerProductionBatchOutputData

    @staticmethod
    def _date_from_string(i_date):
        print('date is', i_date)
        date_str = i_date.split('-')
        year = int(date_str[0])
        month = int(date_str[1])
        day = int(date_str[2])
        print('date is', date(year,month,day))
        return date(year,month,day)


    def __create_production_batch(self):
        # create empty productionbatch
        # self.productionbatch = ProductionBatch()        

        print('Product Type is: ') # + str(self.managerProductionBatchInputData['productType']))

        # set attributes
        # self.productionbatch.productType = self.managerProductionBatchInputData.productType
        # self.productionbatch.flourQuantity = self.managerProductionBatchInputData.flourQuantity
        # self.productionbatch.date = self.managerProductionBatchInputData.date
        # self.productionbatch.startTime = self.managerProductionBatchInputData.startTime
        # self.productionbatch.products = self.managerProductionBatchInputData.products
        # self.productionbatch.baker = self.managerProductionBatchInputData.baker
        # self.productionbatch.supervisor = self.managerProductionBatchInputData.supervisor
        # self.productionbatch.assistants = self.managerProductionBatchInputData.assistants
        # self.productionbatch.problems = self.managerProductionBatchInputData.problems

        production_date = self._date_from_string(self.managerProductionBatchInputData.date)

        self.productionbatch = {
            'id': None,
            'productType': self.managerProductionBatchInputData.productType,
            "flourQuantity": self.managerProductionBatchInputData.flourQuantity,
            "date": production_date,
            "startTime": time(8,0),
            "endTime": time(8,0),
            "products": self.managerProductionBatchInputData.products,                      
            "baker": self.managerProductionBatchInputData.baker,
            "supervisor": self.managerProductionBatchInputData.supervisor,
            "assistants": ','.join(self.managerProductionBatchInputData.assistants),
            "problems": ','.join(self.managerProductionBatchInputData.problems)
        }

        print('Product Type is: ') # + str(self.productionbatch.productType))

        # save new productionbatch to database
        newproductionbatch = self.productionBatchDataAccess.save(self.productionbatch)

        # if save is successful set output data (productionbatch and day productionbatchs) and format presenter view data
        if newproductionbatch != None:
            self.managerProductionBatchOutputData.feedback = {
                    'status': 'Success',
                    'message': 'DayProductionBatch created'
                }
            self.managerProductionBatchOutputData.productionbatch = newproductionbatch

            self.__get_set_day_production_batches(production_date)


    def add_day_production_batch(self):
        # Check the current date and compare to the date entered
        inputDate = self.managerProductionBatchInputData.date
        print('In service')

        print('inputDate is: ' + str(inputDate))

        # todayStr = "{}-{}-{}".format(date.today().year, date.today().month, date.today().day)
        inputDate =  str(self.managerProductionBatchInputData.date) # '{:%Y-%m-%d}'.format(self.managerProductionBatchInputData.date)
        todayStr = '{:%Y-%m-%d}'.format(date.today())
        print('todayStr is: ' + todayStr)

        # if str(inputDate) == todayStr:
        #     print('Date is today')
        #     # create ProductionBatch
        #     self.__create_production_batch()

        if date_is_yesterday_or_today(str(inputDate)):
            print('Date is today or yesterday')
            # create ProductionBatch
            self.__create_production_batch()

        else:
            # If date is not today, check if user is in manager_group, if return user can only save in the current day
            print('Date is not today or yesterday')

            groups = self.managerProductionBatchInputData.groups
            print('number of groups is: ' + str(len(groups)))

            groupnames = [ group['description'] for group in groups]

            print(str(groupnames))

            if len(groups) > 0 and 'manager_group' in groupnames:
                self.__create_production_batch()
            else:  
                self.managerProductionBatchOutputData.productionbatch = None
                self.managerProductionBatchOutputData.feedback = {
                    'status': 'Failure',
                    'message': 'You can only save ProductionBatch in the current day!'
                }
                self.managerProductionBatchPresenter.set_production_batch(self.managerProductionBatchOutputData)
                self.managerProductionBatchPresenter.set_feedback(self.managerProductionBatchOutputData)
    
    def __update_day_production_batch(self, productionbatch):
        # if self.managerProductionBatchInputData.productType != None: productionbatch.productType = self.managerProductionBatchInputData.productType 
        # if self.managerProductionBatchInputData.flourQuantity != None: productionbatch.flourQuantity = self.managerProductionBatchInputData.flourQuantity
        # if self.managerProductionBatchInputData.date != None: productionbatch.date = self.managerProductionBatchInputData.date
        # if self.managerProductionBatchInputData.startTime != None: productionbatch.startTime = self.managerProductionBatchInputData.startTime
        # if self.managerProductionBatchInputData.products != None: productionbatch.products = self.managerProductionBatchInputData.products
        # if self.managerProductionBatchInputData.baker != None: productionbatch.baker = self.managerProductionBatchInputData.baker
        # if self.managerProductionBatchInputData.supervisor != None: productionbatch.supervisor = self.managerProductionBatchInputData.supervisor
        # if self.managerProductionBatchInputData.assistants != None: productionbatch.assistants = self.managerProductionBatchInputData.assistants
        # if self.managerProductionBatchInputData.problems != None: productionbatch.problems = self.managerProductionBatchInputData.problems

        production_date = self._date_from_string(self.managerProductionBatchInputData.date)

        print('Production date is', production_date)

        self.productionbatch = {
            'id': productionbatch['id'],
            'productType': self.managerProductionBatchInputData.productType,
            "flourQuantity": self.managerProductionBatchInputData.flourQuantity,
            "date": production_date,
            "startTime": time(8,0),
            "endTime": time(8,0),
            "products": self.managerProductionBatchInputData.products,                      
            "baker": self.managerProductionBatchInputData.baker,
            "supervisor": self.managerProductionBatchInputData.supervisor,
            "assistants": ','.join(self.managerProductionBatchInputData.assistants),
            "problems": ','.join(self.managerProductionBatchInputData.problems)
        }

        print('About to save', self.productionbatch)

        savedproductionbatch = self.productionBatchDataAccess.save(self.productionbatch)

        print('Saved', savedproductionbatch)

        self.managerProductionBatchOutputData.productionbatch = savedproductionbatch
        # self.managerProductionBatchPresenter.set_production_batch(self.managerProductionBatchOutputData)
        self.__get_set_day_production_batches(production_date)
        # print('About to get dayproductionbatches')
        # self.managerProductionBatchOutputData.dayproductionbatches = self.productionBatchDataAccess.get_day_production_batches(production_date)
        # print('About to set dayproductionbatches')
        # self.managerProductionBatchPresenter.set_day_production_batches(self.managerProductionBatchOutputData)

    def __get_set_day_production_batches(self,production_date):
        self.managerProductionBatchOutputData.dayproductionbatches = self.productionBatchDataAccess.get_day_production_batches(production_date)

        self.managerProductionBatchPresenter.set_production_batch(self.managerProductionBatchOutputData)
        self.managerProductionBatchPresenter.set_day_production_batches(self.managerProductionBatchOutputData)
        self.managerProductionBatchPresenter.set_feedback(self.managerProductionBatchOutputData)

    def update_day_production_batch(self):
        id = self.managerProductionBatchInputData.id
        print('id', id)
        productionbatch = self.productionBatchDataAccess.get(id)
        print('id', productionbatch)
        # print("ProductionBatch id is: " + str(productionbatch.id))
        # print("ProductionBatch date is: " + str(productionbatch.date))

        inputDate =  str(productionbatch['date'])

        print('inputDate', inputDate)

        # Continue with update only if date is yesterday or today
        if date_is_yesterday_or_today(str(inputDate)):
            print('Date is today or yesterday')
            # update ProductionBatch
            self.__update_day_production_batch(productionbatch)
        # Continue with update if user is Manager
        else:
            print('Date is not today or yesterday')
            
            groups = self.managerProductionBatchInputData.groups
            print('number of groups is: ' + str(len(groups)))

            groupnames = [ group['description'] for group in groups]

            print(str(groupnames))

            if len(groups) > 0 and 'manager_group' in groupnames:
                self.__update_day_production_batch(productionbatch)
            else:  
                self.managerProductionBatchOutputData.productionbatch = None
                self.managerProductionBatchOutputData.feedback = {
                    'status': 'Failure',
                    'message': 'You can only save ProductionBatch in the current day!'
                }
                self.managerProductionBatchPresenter.set_production_batch(self.managerProductionBatchOutputData)
                self.managerProductionBatchPresenter.set_feedback(self.managerProductionBatchOutputData)

            

    def get_day_production_batch(self):
        id = self.managerProductionBatchInputData.id
        productionbatch = self.productionBatchDataAccess.get(id)
        
        self.managerProductionBatchOutputData.productionbatch = productionbatch
        self.managerProductionBatchPresenter.set_production_batch(self.managerProductionBatchOutputData)

    
    def get_day_production_batches(self):
        date = self.managerProductionBatchInputData.date

        dayproductionbatches = self.productionBatchDataAccess.get_day_production_batches(date)

        self.managerProductionBatchOutputData.dayproductionbatches = dayproductionbatches 
        print('dat production batches', dayproductionbatches)
        self.managerProductionBatchPresenter.set_day_production_batches(self.managerProductionBatchOutputData)

