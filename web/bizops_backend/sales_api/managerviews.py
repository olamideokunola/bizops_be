from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse

from domain.controllers.MainController import MainController
from domain.services.ManagerSalesPresenters import ManagerSaleViewModel, ManagerSalesPresenter
from domain.services.ManagerProductsPresenters import ManagerProductViewModel, ManagerProductsPresenter

from domain.services.ManagerProductionPresenters import ManagerProductionBatchViewModel, ManagerProductionBatchPresenter


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt, csrf_protect 

import datetime
import json

from django.core.files.base import ContentFile
from django.core.files.storage import  FileSystemStorage
import os
from django.conf import settings

from django.http import FileResponse

path = str(settings.CUSTOM_PACKAGE_ROOT) + '/web/uploaded/productphotos'

# Create your views here.
class ManagerSaleBaseView(View):
    viewModel = ManagerSaleViewModel()
    presenter = ManagerSalesPresenter(viewModel)
    controller = MainController(presenter)

    def get_params_from_request(self, request):
        # Get param from request body as python object
        print(json.loads(request.body))     
        params = json.loads(request.body)
        
        # Get individual params
        self.productid = params['productid'] if 'productid' in params.keys() else None
        self.quantity = params['quantity'] if 'quantity' in params.keys()  else None
        self.price = params['price'] if 'price' in params.keys() else None 
        self.date = params['date'] if 'date' in params.keys() else None
        self.customerid = params['customerid'] if 'customerid' in params.keys()  else None
        self.saleid = params['saleid'] if 'saleid' in params.keys()  else None
        self.creator = params['creator'] if 'creator' in params.keys()  else None


class ManagerProductBaseView(View):
    viewModel = ManagerProductViewModel()
    presenter = ManagerProductsPresenter(viewModel)
    controller = MainController(presenter)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Products(ManagerProductBaseView):
    def get(self, request):
        controller = self.controller.manageProductsServiceController
        self.controller.manageProductsServiceController.get_products()
        return JsonResponse(self.viewModel.get_products(), safe=False)

    def post(self, request):
        # Get param from request body as python object
        print('In post method to create new product!')
        print(json.loads(request.body))     
        params = json.loads(request.body)

        for param in params:
            print(str(param))
        
        # Get individual params
        self.name = params['name'] if 'name' in params.keys() else None
        self.group = params['group'] if 'group' in params.keys() else None
        self.units = params['units'] if 'units' in params.keys() else None
        self.prices = params['prices'] if 'prices' in params.keys() else None
        
        # set current date as date product was created
        self.date = {
            'year': datetime.date.today().year,
            'month': datetime.date.today().month,
            'day': datetime.date.today().day,
        }

        controller = self.controller.manageProductsServiceController
        self.controller.manageProductsServiceController.create_product(self.name, self.group, self.date, self.units)
        return JsonResponse(self.viewModel.get_product(), safe=False)
    
    def delete(self, request):
        self.controller.manageProductsServiceController.delete_all_products()
        
        return JsonResponse({self.viewModel.get_products()}, safe=False)
    
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Product(ManagerProductBaseView):
    def get(self, request, id):
        controller = self.controller.manageProductsServiceController
        self.controller.manageProductsServiceController.get_product(id)

        return JsonResponse(self.viewModel.get_product(), safe=False)

    def put(self, request, id):
        print(json.loads(request.body))     
        params = json.loads(request.body)
        print('id is: ' + str(id))

        # Get individual params
        self.name = params['name'] if 'name' in params.keys() else None
        self.group = params['group'] if 'group' in params.keys() else None
        self.units = params['units'] if 'units' in params.keys() else None
        self.prices = params['prices'] if 'prices' in params.keys() else None

        self.controller.manageProductsServiceController.update_product(
            productid=id,
            name=self.name,
            group=self.group,
            units=self.units,
            prices=self.prices,
        )
        print (self.viewModel.get_product())
        return JsonResponse(self.viewModel.get_product(), safe=False)

    def delete(self, request, id):
        self.controller.manageProductsServiceController.delete_product(id)

        return JsonResponse({ "product": self.viewModel.get_product(), "products": self.viewModel.get_products()}, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class ProductPrices(ManagerProductBaseView):
    # Add prices to products
    def post(self, request, id):
        params = json.loads(request.body)
        print('id is: ' + str(id))

        # Get individual params
        self.prices = params['prices'] if 'prices' in params.keys() else None
        self.defaultPrice = params['defaultPrice'] if 'defaultPrice' in params.keys() else None

        print('Default Price: ' + str(self.defaultPrice))

        self.controller.manageProductsServiceController.add_prices(
            productid = id,
            prices=self.prices,
            defaultPrice=self.defaultPrice
            )
        
        self.controller.manageProductsServiceController.get_products()

        return JsonResponse({ "product": self.viewModel.get_product(), "products": self.viewModel.get_products() }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class ProductPrice(ManagerProductBaseView):
    # Add prices to products
    def post(self, request, id):
        params = json.loads(request.body)
        print('id is: ' + str(id))

        # Get individual params
        self.pricedate = params['date'] if 'date' in params.keys() else None
        self.amount = params['price'] if 'price' in params.keys() else None
        self.active = params['active'] if 'active' in params.keys() else None

        self.controller.manageProductsServiceController.add_price(
            productid=id,
            pricedate=self.pricedate,
            amount=self.amount,
            active=self.active
            )

        return JsonResponse(self.viewModel.get_product(), safe=False)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class ProductImage(ManagerProductBaseView):
    def post(self, request, id):
        params = request.POST
        # print('id is: ' + str(id))

        # Get individual params
        self.name = params['name'] if 'name' in params.keys() else None
        self.group = params['group'] if 'group' in params.keys() else None
        # path = "/media/uploaded/productphotos"
        # path = os.path.join(settings.MEDIA_ROOT, '/productphotos')
         # save image
        fs = FileSystemStorage(path)
        for fileid in request.FILES:
            print(request.FILES[fileid].name)
            file = request.FILES[fileid]
            #filename = fileid
            originalfilename = request.FILES[fileid].name
            filenamelements = originalfilename.split('.')
            ext = filenamelements[1]
            print('extension is: ' + ext)
            filename = str(id) + '.' + ext
            #print('location: ' + str(storage.location))
            if fs.exists(path + '/' + filename):
                print('File exists!')
                fs.delete(path + '/' + filename)
            else:
                print('File does not exist!')
            fs.save(filename, file)
        
        return JsonResponse(self.viewModel.get_product(), safe=False)
    
    def put(self, request, id):
        params = request.PUT
        # print('id is: ' + str(id))

        # Get individual params
        self.name = params['name'] if 'name' in params.keys() else None
        self.group = params['group'] if 'group' in params.keys() else None
        # path = "/media/uploaded/productphotos"
         # save image
        fs = FileSystemStorage(path)
        for fileid in request.FILES:
            print(request.FILES[fileid].name)
            file = request.FILES[fileid]
            #filename = fileid
            originalfilename = request.FILES[fileid].name
            filenamelements = originalfilename.split('.')
            ext = filenamelements[1]
            print('extension is: ' + ext)
            filename = str(id) + '.' + ext
            #print('location: ' + str(storage.location))
            if fs.exists(path + '/' + filename + '.' + ext):
                print('File exists!')
                fs.delete(path + '/' + filename + '.' + ext)
            else:
                print('File does not exist!')
            fs.save(filename, file)
        
        return JsonResponse(self.viewModel.get_product(), safe=False)
    
    def get(self, request, name):
        print('In download product image!, filename is: ' + name)
        # testing
        print('Path is: ' + path)
        response = FileResponse(open(os.path.join(settings.BASE_DIR, path + '/' + name), 'rb'), as_attachment = True)
        
        return response

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Units(ManagerProductBaseView):
    def get(self, request):
        controller = self.controller.manageProductsServiceController
        self.controller.manageProductsServiceController.get_units()

        return JsonResponse(self.viewModel.get_units(), safe=False)

    def post(self, request):
        # Get param from request body as python object
        print('In post method to create new unit!')
        print(json.loads(request.body))     
        params = json.loads(request.body)

        for param in params:
            print(str(param))
        
        # Get individual params
        self.shortDesc = params['short'] if 'short' in params.keys() else None
        self.longDesc = params['long'] if 'long' in params.keys() else None
        self.active = params['active'] if 'active' in params.keys() else None
        
        controller = self.controller.manageProductsServiceController
        self.controller.manageProductsServiceController.create_unit(self.shortDesc, self.longDesc, self.active)
        
        return JsonResponse(self.viewModel.get_unit(), safe=False)

    def delete(self, request):
        self.controller.manageProductsServiceController.delete_all_units()
        
        return JsonResponse(self.viewModel.get_units(), safe=False)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Unit(ManagerProductBaseView):
    def get(self, request, id):
        controller = self.controller.manageProductsServiceController
        self.controller.manageProductsServiceController.get_unit(id)

        return JsonResponse(self.viewModel.get_unit(), safe=False)

    def put(self, request, id):
        print(json.loads(request.body))     
        params = json.loads(request.body)
        print('id is: ' + str(id))

        # Get individual params
        self.short = params['short'] if 'short' in params.keys() else None
        self.long = params['long'] if 'long' in params.keys() else None
        self.active = params['active'] if 'active' in params.keys() else None

        self.controller.manageProductsServiceController.update_unit(
            unitid=id,
            shortDesc=self.short,
            longDesc=self.long,
            active=self.active
        )
        print (self.viewModel.get_unit())
        return JsonResponse(self.viewModel.get_unit(), safe=False)
    
    def delete(self, request, id):
        self.controller.manageProductsServiceController.delete_unit(id)

        return JsonResponse(self.viewModel.get_unit(), safe=False)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Customers(ManagerSaleBaseView):
    def get(self, request):
        controller = self.controller.manageSalesServiceController
        self.controller.manageSalesServiceController.get_customers()
        return JsonResponse(self.viewModel.get_customers(), safe=False)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Sales(ManagerSaleBaseView):

    def get(self, request):
        self.controller.manageSalesServiceController.get_sales()
        return JsonResponse(self.viewModel.get_sales(), safe=False)

    def post(self, request):
        controller = self.controller.manageSalesServiceController

        # Get param from request body as python object
        self.get_params_from_request(request)
        user = request.user
        print('User is: ' + str(user))
        print('date: ' + str(self.date))
        print('productid: ' + str(self.productid))
        print('quantity: ' + str(self.quantity))
        print('price: ' + str(self.price))
        controller.add_day_sale(
            productid=self.productid,
            quantity=self.quantity,
            price=self.price,
            date=self.date,
            customerid=self.customerid,
            creator=user['username'],
            authorizations=user['authorizations'],
            groups=user['groups']
        )
        print ('In POST, saved sale is: ' + str(self.viewModel.get_sale()))
        
        feedback = self.viewModel.get_feedback()

        if feedback['status'] == 'Success':
            print('In success, feedback is: '+ str(feedback))
            return JsonResponse({'status': feedback['status'], 'daysale': self.viewModel.get_sale(), 'daysales': self.viewModel.get_day_sales()}, safe=False)
        elif feedback['status'] =='Failure':
            print('In failure, feedback is: '+ str(feedback))
            return JsonResponse(feedback, safe=False)

    def put(self, request):
        self.get_params_from_request(request)

        self.controller.manageSalesServiceController.update_sale(
            saleid=self.saleid,
            productid=self.productid,
            quantity=self.quantity,
            price=self.price,
            date=self.date,
            customerid=self.customerid
        )
        print (self.viewModel.get_sale())
        return JsonResponse(self.viewModel.get_sale(), safe=False)
    
    def delete(self, request):
        self.controller.manageSalesServiceController.delete_all_sales()

        return JsonResponse({'message': 'All sales deleted!'}, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Sale(ManagerSaleBaseView):   
    
    def delete(self, request, id):
        self.controller.manageSalesServiceController.delete_sale(id)

        return JsonResponse(self.viewModel.get_sale(), safe=False)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class DaySales(ManagerSaleBaseView):
    def get(self, request, year, month, day):
        controller = self.controller.manageSalesServiceController
        date = datetime.date(year, month, day)
        self.controller.manageSalesServiceController.get_day_sales(date)
        return JsonResponse(self.viewModel.get_day_sales(), safe=False)
    
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class MonthSales(ManagerSaleBaseView):
    def get(self, request, year, month):
        controller = self.controller.manageSalesServiceController
        self.controller.manageSalesServiceController.get_month_sales(year, month)
        return JsonResponse({'monthsales': self.viewModel.get_month_sales()}, safe=False)