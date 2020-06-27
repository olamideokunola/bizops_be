from domain.services.ManagerProductionServices import ManagerProductionBatchInputInterface, ManagerProductionBatchInputData
import datetime

class ManagerProductionBatchServiceController:
    managerProductionBatchService = ManagerProductionBatchInputInterface
    managerProductionBatchInputData = ManagerProductionBatchInputData()

    def __init__(self, managerProductionBatchInputData, managerProductionBatchService):
        self.managerProductionBatchInputData = managerProductionBatchInputData
        if isinstance(managerProductionBatchService, ManagerProductionBatchInputInterface):
            self.managerProductionBatchService = managerProductionBatchService

    def add_day_production_batch(self, params):
        self.managerProductionBatchInputData.productType = params["productType"] if params["productType"] != None else None
        self.managerProductionBatchInputData.flourQuantity = params["flourQuantity"] if params["flourQuantity"] != None else None
        self.managerProductionBatchInputData.date = params["date"] if params["date"] != None else None
        self.managerProductionBatchInputData.startTime = params["startTime"] if params["startTime"] != None else None
        self.managerProductionBatchInputData.products = params["products"] if params["products"] != None else None
        self.managerProductionBatchInputData.baker = params["baker"] if params["baker"] != None else None
        self.managerProductionBatchInputData.supervisor = params["supervisor"] if params["supervisor"] != None else None
        self.managerProductionBatchInputData.assistants = params["assistants"] if params["assistants"] != None else None
        self.managerProductionBatchInputData.problems = params ["problems"] if params["problems"] != None else None
        
        self.managerProductionBatchInputData.groups = params ["groups"] if params["groups"] != None else None

        self.managerProductionBatchService.add_day_production_batch()

    def update_day_production_batch(self, id, params):
        print("In controller, update_day_production_batch", params)
        self.managerProductionBatchInputData.id = id if id != None else None
        self.managerProductionBatchInputData.productType = params["productType"] if params["productType"] != None else None
        self.managerProductionBatchInputData.flourQuantity = params["flourQuantity"] if params["flourQuantity"] != None else None
        self.managerProductionBatchInputData.date = params["date"] if params["date"] != None else None
        self.managerProductionBatchInputData.startTime = params["startTime"] if params["startTime"] != None else None
        self.managerProductionBatchInputData.products = params["products"] if params["products"] != None else None
        self.managerProductionBatchInputData.baker = params["baker"] if params["baker"] != None else None
        self.managerProductionBatchInputData.supervisor = params["supervisor"] if params["supervisor"] != None else None
        self.managerProductionBatchInputData.assistants = params["assistants"] if params["assistants"] != None else None
        self.managerProductionBatchInputData.problems = params ["problems"] if params["problems"] != None else None

        self.managerProductionBatchService.update_day_production_batch()
    
    def get_day_production_batch(self, params):
        self.managerProductionBatchInputData.id = params["id"] if params["id"] != None else None
        self.managerProductionBatchInputData.date = params["date"] if params["date"] != None else None

        self.managerProductionBatchService.get_day_production_batch()

    def get_day_production_batches(self, params):
        print("In Controller, params: " + str(params))
        self.managerProductionBatchInputData.date = str(params["date"]) if params["date"] != None else None

        print("date: " + self.managerProductionBatchInputData.date)

        self.managerProductionBatchService.get_day_production_batches()