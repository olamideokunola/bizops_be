import datetime
from abc import ABC, abstractmethod

from domain.services.ManagerSalesServices import ManagerSaleOutputData, ManagerSaleOutputInterface

import json

class ManagerSaleViewModel:
    products = []
    customers = []
    daysales = []
    sales = []
    sale = None
    indent = 4
    feedback = {}

    def __init__(self):
        pass
    
    def get_sale(self):
        # return JSON
        return self.sale

    def get_sales(self):
        # return JSON
        return self.sales

    def get_day_sales(self):
        # return JSON
        return self.daysales

    def get_month_sales(self):
        # return JSON
        return self.monthsales

    def get_products(self):
        # set to JSON
        print (self.products)
        return self.products

    def get_customers(self):
        # set to JSON
        return self.customers

    def get_product(self):
        # set to JSON
        return self.product
    
    def get_feedback(self):
        # set to JSON
        return self.feedback

class ManagerSalesPresenter(ManagerSaleOutputInterface):
    managerSaleViewModel = None

    def __init__(self, managerSaleViewModel):
        self.managerSaleViewModel = managerSaleViewModel

    @staticmethod
    def _format_sale(daysale):
        return {
                "id": daysale.id,
                "product": {
                    "id": daysale.product.id,
                    "name": daysale.product.name,
                    "title": daysale.product.title,
                    "date": {
                        "year": daysale.product.date.year,
                        "month": daysale.product.date.month,
                        "day": daysale.product.date.day
                    },
                    "price": {
                        'date': '%i-%02i-%02i' % (daysale.product.price.fromDate.year, daysale.product.price.fromDate.month, daysale.product.price.fromDate.day) if daysale.product.price != None else None,
                        'price': daysale.product.price.amount if daysale.product.price != None else None,
                        'active': daysale.product.price.active if daysale.product.price != None else None,
                    },
                    'prices': [
                        {
                            'date': '%i-%02i-%02i' % (price.fromDate.year, price.fromDate.month, price.fromDate.day),
                            'price': price.amount,
                            'active': price.active
                        } for price in daysale.product.prices
                    ]
                },
                "quantity": daysale.quantity,
                "price": {'price': float(daysale.price)},
                "currency": daysale.currency,
                "date": {
                    "year": daysale.date.year,
                    "month": daysale.date.month,
                    "day": daysale.date.day
                },
                "customer": {
                    "id": (daysale.customer.id if daysale.customer != None else None),
                    "name": (daysale.customer.name if daysale.customer != None else None),
                    "title": (daysale.customer.title if daysale.customer != None else None),
                    "date": {
                        "year": daysale.customer.date.year if daysale.customer != None else None,
                        "month": daysale.customer.date.month if daysale.customer != None else None,
                        "day": daysale.customer.date.day if daysale.customer != None else None,
                    }
                },
                "creator": daysale.creator.username,
                "lastSaleTime":  str(daysale.lastSaleTime),
                "currency": daysale.currency,
            }

    def set_sale(self, managerSaleOutputData):
        # get sale from managerSaleOutputData,
        # convert to JSON and put in 
        # managerSaleViewModel
        # self.managerSaleViewModel.sale = self.make_json_complaint(managerSaleOutputData.sale)
        print('In set sales')
        daysale = managerSaleOutputData.sale
        self.managerSaleViewModel.sale = self._format_sale(daysale) if daysale != None else None

    def set_sales(self, managerSaleOutputData):
        # get sale from managerSaleOutputData,
        # convert to JSON and put in 
        # managerSaleViewModel
        print('In set sales')
        self.managerSaleViewModel.sales = [
                self._format_sale(sale) for sale in managerSaleOutputData.sales
            ]
    
    def __get_formatted_sales(self, salesObj):
        # print('prices type', type(salesObj[0].product.prices))
        # print('prices', (salesObj[0].product))
        return [ 
           self._format_sale(saleObj) for saleObj in salesObj
        ]

    def set_day_sales(self, managerSaleOutputData):
        # get daysale from managerSaleOutputData,
        # convert to JSON and put in 
        # managerSaleViewModel
        # self.managerSaleViewModel.daysales = self.make_json_complaint(managerSaleOutputData.daysales)
        print('In  set day dales')
        self.managerSaleViewModel.daysales = self.__get_formatted_sales(managerSaleOutputData.daysales)

    def set_month_sales(self, managerSaleOutputData):
        # get daysale from managerSaleOutputData,
        # convert to JSON and put in 
        # managerSaleViewModel
        # self.managerSaleViewModel.daysales = self.make_json_complaint(managerSaleOutputData.daysales)

        self.managerSaleViewModel.monthsales = [
            self.__get_formatted_sales(monthsale) for monthsale in managerSaleOutputData.monthsales
            if len(self.__get_formatted_sales(monthsale)) > 0
        ]

        

    def set_customers(self, managerSaleOutputData):
        # get customer from managerSaleOutputData,
        # convert to JSON and put in 
        # managerSaleViewModel
        self.managerSaleViewModel.customers = self.make_json_complaint(managerSaleOutputData.customers)

    def set_products(self, managerSaleOutputData):
        # get products from managerSaleOutputData,
        # convert to JSON and put in 
        # managerSaleViewModel
        self.managerSaleViewModel.products = self.make_json_complaint(managerSaleOutputData.products)

    def make_json_complaint(self, item):
        compliant_item = None
        if type(item) == list:
            compliant_item = [self.__make_object_json_complaint(item_element) for item_element in item]                
        else:
            compliant_item = self.__make_object_json_complaint(item)
        return compliant_item

    def __make_object_json_complaint(self, item):
        json_compliant_object = {}
        itemkeys = list(item.__dict__.keys())
        for attr_name in item.__dict__.keys():
            if attr_name.startswith('_') == False:                
                try:
                    # for objects
                    attr_value = item.__dict__[attr_name]
                    if len(attr_value.__dict__.keys()) > 0: 
                        json_compliant_object[attr_name] = self.make_json_complaint(attr_value)
                except AttributeError:       
                    # for other types            
                    print (type(item).__name__ + ' ' + attr_name + ' has no __dict__: ' + str(attr_value) )
                    if type(attr_value) == datetime.date:
                        # for dates
                        json_compliant_object[attr_name] = {
                            'year': attr_value.year,
                            'month': attr_value.month,
                            'day': attr_value.day,
                        }
                    elif type(attr_value) == list:
                        # for lists
                        json_compliant_object[attr_name] = [
                            self.make_json_complaint(itm) for itm in attr_value                                                
                        ]
                    else:
                        # for others
                        json_compliant_object[attr_name] = item.__dict__[attr_name]
        return json_compliant_object

    def set_product(self, managerSaleOutputData):
        # get product from managerSaleOutputData,
        # convert to JSON and put in 
        # managerSaleViewModel
        self.managerSaleViewModel.product = {
            'id': managerSaleOutputData.product.id,
            'name': managerSaleOutputData.product.name,
            'title': managerSaleOutputData.product.name,
            'group': managerSaleOutputData.product.group,
            'units': managerSaleOutputData.product.units,
        }

    def set_feedback(self, managerSaleOutputData):
        self.managerSaleViewModel.feedback = managerSaleOutputData.feedback