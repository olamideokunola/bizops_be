import datetime
from abc import ABC, abstractmethod

from domain.services.AuthenticationServices import AuthenticationOutputData, AuthenticationOutputInterface

import json

class BasePresenter():

    def make_json_complaint(self, item):
        compliant_item = None
        if type(item) == list:
            compliant_item = [self.__make_object_json_complaint(item_element) for item_element in item]      
        else:
            compliant_item = self.__make_object_json_complaint(item)
        return compliant_item

    def __make_object_json_complaint(self, item):
        json_compliant_object = {}
        #itemkeys = list(item.__dict__.keys())
        for attr_name in item.__dict__.keys():
            print("--attr: " + attr_name)
            if attr_name.startswith('_') == False:                
                try:
                    # for objects
                    attr_value = item.__dict__[attr_name]   
                    if len(attr_value.__dict__.keys()) > 0: 
                        json_compliant_object[attr_name] = self.make_json_complaint(attr_value)
                        print (type(item).__name__ + ' ' + attr_name + ' has __dict__: ' + str(attr_value) )
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

