import datetime
from abc import ABC, abstractmethod

from domain.services.AuthenticationServices import AuthenticationOutputData, AuthenticationOutputInterface
from .BasePresenters import BasePresenter

import json

class AuthenticationViewModel:
    user = None
    groups = None
    messages = None

class AuthenticationPresenter(BasePresenter, AuthenticationOutputInterface):
    viewModel = None

    def __init__(self, viewModel):
        self.viewModel = viewModel

    def set_user(self, outputData):
        # get user from outputData,
        # convert to JSON compliant object and put in 
        # viewModel
        #self.viewModel.user = self.make_json_complaint(outputData.user)
        print('In set user')
        self.viewModel.user = {
            'id': outputData.user.id,
            'username': outputData.user.username,
            'password': outputData.user.password,
            'firstname': outputData.user.person.firstname,
            'lastname': outputData.user.person.lastname,
            'email': outputData.user.email,
            'phonenumber': outputData.user.phonenumber if outputData.user.phonenumber != None else '',
            'authorizations': list(outputData.user.authorizations) if outputData.user.authorizations != None else None,
            'groups': list(outputData.user.groups) if outputData.user.groups != None else None
        }
        print('user set', self.viewModel.user)
    
    def set_users(self, outputData):
        # Get users from outputData
        # convert to JSON compliant objects
        self.viewModel.users = [
            {
                'id': user.id,
                'username':user.username,
                'password': user.password,
                'firstname': user.person.firstname,
                'lastname': user.person.lastname,
                'email': user.email,
                'phonenumber': user.phonenumber,
                'authorizations': list(user.authorizations) if user.authorizations != None else [],
                'groups': list(user.groups) if user.groups != None else []
            } for user in outputData.users
        ]

    def set_messages(self, outputData):
        # get messages from outputData,
        # convert to JSON compliant object and put in 
        # viewModel
        self.viewModel.messages = self.make_json_complaint(outputData.messages)

    def set_models(self, outputData):
        self.viewModel.models = [
            {
                
                'title': model['name']
            } for model in outputData.models]

    def set_groups(self, outputData):
        self.viewModel.groups = [
            {
                'id': group.id,
                'description': group.description,
                'details': group.details,
                'authorizations': list(group.authorizations) if group.authorizations != None else [],
            } for group in outputData.groups
        ]
        
    def set_group(self, outputData):
        self.viewModel.group = {
            'id': outputData.group.id,
            'description': outputData.group.description,
            'details': outputData.group.details,
            'authorizations': list(outputData.group.authorizations) if outputData.group.authorizations != None else []
        }
