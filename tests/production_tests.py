import unittest
import datetime

from domain.production.ProductionBatch import ProductionBatch

from domain.dataAccess.ProductionBatchDataAccess import ShelveProductionBatchDataAccess

from domain.dataAccess.ShelveDatabase import ShelveDataBaseManager

from domain.services.ManagerProductionServices import ManagerManageProductionBatchService, ManagerProductionBatchInputData
from domain.services.ManagerProductionPresenters import ManagerProductionBatchPresenter, ManagerProductionBatchViewModel, ManagerProductionBatchOutputData


class ManagerManageProductServiceTest(unittest.TestCase):
    productbatch = ProductionBatch()
    managerManageProductionBatchService = None
    databaseManager = ShelveDataBaseManager("domain/dataAccess/ShelveDatabase/")


    productionBatchDataAccess = ShelveProductionBatchDataAccess(databaseManager)

    managerProductionBatchInputData = ManagerProductionBatchInputData()
    managerProductionBatchOutputData = ManagerProductionBatchOutputData()
    managerProductionBatchViewModel = ManagerProductionBatchViewModel()
    managerProductionBatchPresenter = ManagerProductionBatchPresenter(ManagerProductionBatchViewModel)
        
    def setup_service(self):
        self.managerManageProductionBatchService = ManagerManageProductionBatchService(
            self.productionBatchDataAccess,
            self.managerProductionBatchInputData,
            self.managerProductionBatchOutputData,
            self.managerProductionBatchPresenter
        )

    def create_day_production_batch_input(self):
        self.managerProductionBatchInputData.productType = "Bread"
        self.managerProductionBatchInputData.flourQuantity = 3
        self.managerProductionBatchInputData.date = '2020-05-28'
        self.managerProductionBatchInputData.startTime = "8:00 AM"
        self.managerProductionBatchInputData.products = [
	      {
	        "id": 1,
	        "name": "800g Loaf Bread",
	        "price": 400,
	        "goodQuantity": 16,
	        "damagedQuantity": 0
	      },
	      {
	        "id": 1,
	        "name": "600g Loaf Bread",
	        "price": 300,
	        "goodQuantity": 20,
	        "damagedQuantity": 0
	      }
	    ]
        self.managerProductionBatchInputData.baker = "Ramon"
        self.managerProductionBatchInputData.supervisor = "Bose"
        self.managerProductionBatchInputData.assistants = ["Chidinma", "Busayo"]
        self.managerProductionBatchInputData.problems = ["Insufficient butter", "Intermittent stoppage of mixer"]


    def test_add_day_production_batch(self):
        self.setup_service()

        self.create_day_production_batch_input()

        # inputData = self.managerProductInputData
        self.managerManageProductionBatchService.add_day_production_batch()

        print(str(self.managerProductionBatchViewModel.productionbatch))

        self.assertEqual("Ramon", self.managerProductionBatchOutputData.productionbatch.baker)
        self.assertEqual(2, len(self.managerProductionBatchOutputData.productionbatch.products))

    def test_update_day_production_batch(self):
        self.setup_service()

        self.managerProductionBatchInputData.id = 23
        self.managerProductionBatchInputData.date = "2020-05-27"
        self.managerProductionBatchInputData.baker = "Remi"

        self.managerManageProductionBatchService.update_day_production_batch()

        self.assertEqual("Remi", self.managerProductionBatchOutputData.productionbatch.baker)

    def test_get_day_production_batch(self):
        self.setup_service()

        self.managerProductionBatchInputData.id = 23

        self.managerManageProductionBatchService.get_day_production_batch()

        self.assertEqual(23, self.managerProductionBatchOutputData.productionbatch.id)

    def test_get_day_production_batches(self):
        self.setup_service()

        self.managerProductionBatchInputData.date = "2020-05-27"

        self.managerManageProductionBatchService.get_day_production_batches()

        self.assertGreater(len(self.managerProductionBatchOutputData.productionbatches), 10)



# class ProductPresenterTest(unittest.TestCase):
#     presenter = None
#     outputData = ManagerProductOutputData()
#     viewModel = ManagerProductViewModel()

#     def setup_presenter(self):
#         self.presenter = ManagerProductsPresenter(self.viewModel)
    
#     def setup_unit(self):
#         self.unit = Unit(id= 0, shortDesc='ns', longDesc='new Short', active=False)
        
#     def test_set_unit(self):
#         self.setup_presenter()
#         self.setup_unit()

#         self.outputData.unit = self.unit
#         self.presenter.set_unit(self.outputData)

#         # test
#         self.assertDictEqual(self.viewModel.get_unit(),
#         {
#             'id': 0,
#             'short': 'ns',
#             'long': 'new Short',
#             'active': False
#         })