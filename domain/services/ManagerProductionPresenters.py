import datetime
from abc import ABC, abstractmethod

from domain.services.ManagerProductionServices import ManagerProductionBatchOutputData, ManagerProductionBatchOutputInterface

import json

class ManagerProductionBatchViewModel:
    productionbatch = None
    productionbatches = []
    dayproductionbatches = []
    monthproductionbatches = []
    indent = 4
    feedback = {}

    def __init__(self):
        pass
    
    def get_production_batch(self):
        # return JSON
        return self.productionbatch

    def get_production_batches(self):
        # return JSON
        return self.productionbatches

    def get_day_production_batches(self):
        # return JSON
        return self.dayproductionbatches

    def get_month_production_batches(self):
        # return JSON
        return self.monthproductionbatches
    
    def get_feedback(self):
        # set to JSON
        return self.feedback

class ManagerProductionBatchPresenter(ManagerProductionBatchOutputInterface):
    managerProductionBatchViewModel = None

    def __init__(self, managerProductionBatchViewModel):
        self.managerProductionBatchViewModel = managerProductionBatchViewModel

    def set_production_batch(self, managerProductionBatchOutputData):
        # get productionbatch from managerProductionBatchOutputData,
        # convert to JSON and put in 
        # managerProductionBatchViewModel
        dayproductionbatch = managerProductionBatchOutputData.productionbatch

        if dayproductionbatch != None:
            print('In Presenter, Product Type is: ' + str(dayproductionbatch.productType))

        
        self.managerProductionBatchViewModel.productionbatch = {
            "id": dayproductionbatch.id if dayproductionbatch.id  != None else None,
            "productType": dayproductionbatch.productType if dayproductionbatch.productType != None else None,
            "flourQuantity": dayproductionbatch.flourQuantity if dayproductionbatch.flourQuantity != None else None,
            "startTime": dayproductionbatch.startTime if dayproductionbatch.startTime != None else None,
            "endTime": dayproductionbatch.endTime if dayproductionbatch.endTime  != None else None,
            "date": dayproductionbatch.date if dayproductionbatch.date  != None else None,
            "products": dayproductionbatch.products if dayproductionbatch.products != None else None,
            "baker": dayproductionbatch.baker if dayproductionbatch.baker != None else None,
            "supervisor": dayproductionbatch.supervisor if dayproductionbatch.supervisor  != None else None,
            "assistants": dayproductionbatch.assistants if dayproductionbatch.assistants != None else None,
            "problems": dayproductionbatch.problems if dayproductionbatch.problems != None else None,
        } if dayproductionbatch != None else None

    def set_production_batches(self, managerProductionBatchOutputData):
        # get productionbatch from managerProductionBatchOutputData,
        # convert to JSON and put in 
        # managerProductionBatchViewModel
        self.managerProductionBatchViewModel.productionbatches = self.__get_formatted_production_batches(managerProductionBatchOutputData.productionbatches)
    
    def __get_formatted_production_batches(self, productionBatchesObj):
        return [ 
            {
                "id": productionBatch.id,
                "productType": productionBatch.productType,
                "flourQuantity": productionBatch.flourQuantity,
                "startTime": productionBatch.startTime,
                "endTime": productionBatch.endTime,
                "date": productionBatch.date,
                "products": productionBatch.products,
                "baker": productionBatch.baker,
                "supervisor": productionBatch.supervisor,
                "assistants": productionBatch.assistants,
                "problems": productionBatch.problems
            } for productionBatch in productionBatchesObj
        ]

    def set_day_production_batches(self, managerProductionBatchOutputData):
        # get daysale from managerProductionBatchOutputData,
        # convert to JSON and put in 
        # managerProductionBatchViewModel
        print("In presenter")
        self.managerProductionBatchViewModel.dayproductionbatches = self.__get_formatted_production_batches(managerProductionBatchOutputData.dayproductionbatches)
    
    # def set_month_sales(self, managerProductionBatchOutputData):
    #     # get daysale from managerProductionBatchOutputData,
    #     # convert to JSON and put in 
    #     # managerProductionBatchViewModel
    #     # self.managerProductionBatchViewModel.daysales = self.make_json_complaint(managerProductionBatchOutputData.daysales)

    #     self.managerProductionBatchViewModel.monthsales = [
    #         self.__get_formatted_sales(monthsale) for monthsale in managerProductionBatchOutputData.monthsales
    #         if len(self.__get_formatted_sales(monthsale)) > 0
    #     ]


    def set_feedback(self, managerProductionBatchOutputData):
        self.managerProductionBatchViewModel.feedback = managerProductionBatchOutputData.feedback