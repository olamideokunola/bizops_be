from domain.controllers.ManageSalesControllers import ManagerSaleServiceController
from domain.controllers.AuthenticationControllers import AuthenticationController
from domain.controllers.ManageProductsControllers import ManagerProductServiceController
from domain.controllers.ManageProductionControllers import ManagerProductionBatchServiceController


from domain.services.ManagerSalesServices import ManagerSaleInputData, ManagerManageSalesService,ManagerSaleOutputData
from domain.services.AuthenticationServices import AuthenticationInputData, AuthenticationOutputData, AuthenticationService
from domain.services.ManagerProductsServices import ManagerProductInputData, ManagerManageProductsService, ManagerProductOutputData
from domain.services.ManagerProductionServices import ManagerProductionBatchInputData, ManagerManageProductionBatchService, ManagerProductionBatchOutputData


from domain.dataAccess.CustomersDataAccess import CustomersDataAccessInterface, ShelveCustomersDataAccess
from domain.dataAccess.ShelveDatabase import ShelveDataBaseManager
from domain.dataAccess.SalesDataAccess import ShelveSalesDataAccess
from domain.dataAccess.ProductsDataAccess import ShelveProductsDataAccess
from domain.dataAccess.UnitsDataAccess import ShelveUnitsDataAccess
from domain.dataAccess.UsersDataAccess import ShelveUsersDataAccess
from domain.dataAccess.GroupsDataAccess import ShelveGroupsDataAccess
from domain.dataAccess.ProductionBatchDataAccess import ShelveProductionBatchDataAccess

from domain.dataAccess.DjangoDataAccess.DjangoDatabase import DjangoDataBaseManager

class MainController:
    # Service declaration 
    managerManageSalesService = None
    authenticationService = None
    managerManageProductionBatchService = None

    # Shelve Database
    # dblocation = "../../domain/dataAccess/ShelveDatabase/"
    # databaseManager = ShelveDataBaseManager(dblocation)

    # Django DataAccess
    databaseManager = DjangoDataBaseManager()

    # data access objects
    productsDataAccess = ShelveProductsDataAccess(databaseManager)
    unitsDataAccess = ShelveUnitsDataAccess(databaseManager)
    customersDataAccess = ShelveCustomersDataAccess(databaseManager)
    salesDataAccess = ShelveSalesDataAccess(databaseManager)
    usersDataAccess = ShelveUsersDataAccess(databaseManager)
    groupsDataAccess = ShelveGroupsDataAccess(databaseManager)
    productionBatchDataAccess = ShelveProductionBatchDataAccess(databaseManager)

    presenter = None

    def __init__(self, presenter):
        self.presenter = presenter
        self.setup_controllers()

    def setup_controllers(self):
        self.setup_managerManageSalesController()
        self.setup_authenticationController()
        self.setup_managerManageProductsController()
        self.setup_managerManageProductionBatchController()

    def setup_managerManageSalesController(self):

        managerSaleInputData = ManagerSaleInputData()
        managerSaleOutputData = ManagerSaleOutputData()

        managerManageSalesService = ManagerManageSalesService(
            self.productsDataAccess, 
            self.customersDataAccess, 
            self.salesDataAccess, 
            managerSaleInputData,
            managerSaleOutputData,
            self.presenter
            )

        self.manageSalesServiceController = ManagerSaleServiceController(managerSaleInputData, managerManageSalesService)

    def setup_authenticationController(self):
        inputData = AuthenticationInputData()
        outputData = AuthenticationOutputData()

        authenticationService = AuthenticationService(inputData, outputData, self.usersDataAccess, self.groupsDataAccess, self.presenter)

        self.authenticationController = AuthenticationController(inputData, authenticationService)

    def setup_managerManageProductsController(self):

        managerProductInputData = ManagerProductInputData()
        managerProductOutputData = ManagerProductOutputData()

        managerManageProductsService = ManagerManageProductsService(
            self.productsDataAccess, 
            self.unitsDataAccess, 
            managerProductInputData,
            managerProductOutputData,
            self.presenter
            )

        self.manageProductsServiceController = ManagerProductServiceController(managerProductInputData, managerManageProductsService)

    def setup_managerManageProductionBatchController(self):

        managerProductionBatchInputData = ManagerProductionBatchInputData()
        managerProductionBatchOutputData = ManagerProductionBatchOutputData()

        managerManageProductionBatchService = ManagerManageProductionBatchService(
            self.productionBatchDataAccess, 
            managerProductionBatchInputData,
            managerProductionBatchOutputData,
            self.presenter
            )

        self.manageProductionBatchServiceController = ManagerProductionBatchServiceController(managerProductionBatchInputData, managerManageProductionBatchService)
