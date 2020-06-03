from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse

from domain.controllers.MainController import MainController

from domain.services.ManagerProductionPresenters import ManagerProductionBatchViewModel, ManagerProductionBatchPresenter


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt, csrf_protect 

import datetime
import json

# Create your views here.
class ManagerProductionBaseView(View):
    viewModel = ManagerProductionBatchViewModel()
    presenter = ManagerProductionBatchPresenter(viewModel)
    controller = MainController(presenter)

    request_params = {}

    def get_params_from_request(self, request):
        # Get param from request body as python object
        print(json.loads(request.body))     
        params = json.loads(request.body)
        self.productType = params['producttype']
        batch = params['batch']

        print("In get request!")
        
        # Get individual params
        self.request_params = {}
        self.request_params['id'] = batch['id'] if 'id' in batch.keys() else None
        self.request_params['productType'] = params['producttype'] if 'producttype' in params.keys() else None
        self.request_params['flourQuantity'] = batch["flourQuantity"] if 'flourQuantity' in batch.keys() else None
        self.request_params['date'] = batch["date"] if 'date' in batch.keys() else None
        self.request_params['startTime'] = batch["startTime"] if 'startTime' in batch.keys() else None
        self.request_params['products'] = batch["products"] if 'products' in batch.keys() else None
        self.request_params['baker'] = batch["baker"] if 'baker' in batch.keys() else None
        self.request_params['supervisor'] = batch["supervisor"] if 'supervisor' in batch.keys() else None
        self.request_params['assistants'] = batch["assistants"] if 'assistants' in batch.keys() else None
        self.request_params['problems'] = batch ["problems"] if 'problems' in batch.keys() else None
        
        user = request.user
        self.request_params['groups'] = user['groups']

        print('self.request_params is: ' + str(self.request_params))

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class ProductionBatches(ManagerProductionBaseView):
    def get(self, request, year, month, day):
        self.request_params['date'] = datetime.date(year, month, day)

        controller = self.controller.manageProductionBatchServiceController
        controller.get_day_production_batches(self.request_params)
  
        return JsonResponse({'dayproductionbatches': self.viewModel.get_day_production_batches()}, safe=False)

    def post(self, request):
        self.get_params_from_request(request)
        print("In post")

        controller = self.controller.manageProductionBatchServiceController
        controller.add_day_production_batch(self.request_params)
        print("In response")
        return JsonResponse({ 'productionbatch': self.viewModel.get_production_batch(), 'dayproductionbatches': self.viewModel.get_day_production_batches()}, safe=False)

    def put(self, request, id):
        self.get_params_from_request(request)
        print("In put")

        controller = self.controller.manageProductionBatchServiceController
        controller.update_day_production_batch(id, self.request_params)
        print("In response")
        return JsonResponse({ 'productionbatch': self.viewModel.get_production_batch(), 'dayproductionbatches': self.viewModel.get_day_production_batches()}, safe=False)