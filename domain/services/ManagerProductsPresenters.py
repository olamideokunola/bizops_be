import datetime
from abc import ABC, abstractmethod

from domain.services.ManagerProductsServices import ManagerProductOutputData, ManagerProductOutputInterface
from domain.services.BasePresenters import BasePresenter

import json

class ManagerProductViewModel:
    products = []
    product = None
    units = []
    unit = None
    indent = 4
    feedback = {}

    def __init__(self):
        pass
    
    def get_unit(self):
        # return JSON
        return self.unit

    def get_units(self):
        # return JSON
        return self.units

    def get_products(self):
        # set to JSON
        print (self.products)
        return self.products

    def get_product(self):
        # set to JSON
        return self.product

    def get_feedback(self):
        # set to JSON
        return self.feedback

class ManagerProductsPresenter(BasePresenter, ManagerProductOutputInterface):
    managerProductViewModel = None

    def __init__(self, managerProductViewModel):
        self.managerProductViewModel = managerProductViewModel

    def set_unit(self, managerProductOutputData):
        # get unit from managerProductOutputData,
        # convert to JSON and put in 
        # managerProductViewModel
        self.managerProductViewModel.unit = {
            'id': managerProductOutputData.unit.id,
            'short': managerProductOutputData.unit.shortDesc,
            'long': managerProductOutputData.unit.longDesc,
            'active': managerProductOutputData.unit.active
        }
    
    def set_units(self, managerProductOutputData):
        # get unit from managerProductOutputData,
        # convert to JSON and put in 
        # managerProductViewModel
        self.managerProductViewModel.units = [
            {
                'id': unit.id,
                'short': unit.shortDesc,
                'long': unit.longDesc,
                'active': unit.active
            } for unit in managerProductOutputData.units
        ]

    def set_products(self, managerProductOutputData):
        # get products from managerProductOutputData,
        # convert to JSON and put in 
        # managerProductViewModel
        # self.managerProductViewModel.products = self.make_json_complaint(managerProductOutputData.products)
        self.managerProductViewModel.products = [ 
            {
               'id': product.id,
                'name': product.name,
                'title': product.name,
                'group': product.group,
                'units': product.units, 
                'price': {
                    'date': '%i-%02i-%02i' % (product.price.fromDate.year, product.price.fromDate.month, product.price.fromDate.day) if product.price != None else None,
                    'price': product.price.amount if product.price != None else None,
                    'active': product.price.active if product.price != None else None,
                },
                'prices': [
                {
                    'date': ('%i-%02i-%02i' % (price.fromDate.year, price.fromDate.month, price.fromDate.day)) if price != None else None,
                    'price': price.amount,
                    'active': price.active
                } for price in product.prices
            ]
            } for product in managerProductOutputData.products
        ]
        # print("In presenter: number of prices in product 1: " + managerProductOutputData.products[0].name + " " + str(len(managerProductOutputData.products[0].prices)))

    def set_product(self, managerProductOutputData):
        # get product from managerProductOutputData,
        # convert to JSON and put in 
        # managerProductViewModel
        self.managerProductViewModel.product = {
            'id': managerProductOutputData.product.id,
            'name': managerProductOutputData.product.name,
            'title': managerProductOutputData.product.name,
            'group': managerProductOutputData.product.group,
            'units': managerProductOutputData.product.units,
            'price': {
                    'date': '%i-%02i-%02i' % (managerProductOutputData.product.price.fromDate.year, managerProductOutputData.product.price.fromDate.month, managerProductOutputData.product.price.fromDate.day) if managerProductOutputData.product.price != None else None,
                    'price': managerProductOutputData.product.price.amount if managerProductOutputData.product.price != None else None,
                    'active': managerProductOutputData.product.price.active if managerProductOutputData.product.price != None else None
                },
            'prices': [
                {
                    'date': ('%i-%02i-%02i' % (price.fromDate.year, price.fromDate.month, price.fromDate.day)) if price != None else None,
                    'price': price.amount if price != None else None,
                    'active': price.active if price != None else None,
                } for price in managerProductOutputData.product.prices
            ]
        }
    
    def set_feedback(self, managerProductOutputData):
        self.managerProductViewModel.feedback = managerProductOutputData.feedback
