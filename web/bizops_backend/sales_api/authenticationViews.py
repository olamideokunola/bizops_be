from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse

from domain.controllers.MainController import MainController
from domain.services.AuthenticationPresenters import AuthenticationViewModel, AuthenticationPresenter

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt, csrf_protect 

import datetime
import json

from bizops_backend.JwtBackend.JwtTokenManager import JwtTokenManager

# Create your views here.
class AuthenticationBaseView(View):
    viewModel = AuthenticationViewModel()
    presenter = AuthenticationPresenter(viewModel)
    controller = MainController(presenter)

    def get_params_from_request(self, request):
        # Get param from request body as python object
        print("In get_params_from_request!")
        print(json.loads(request.body))     
        params = json.loads(request.body)
        self.paramsforcheck = params
        print("Params loaded")

        # Get individual params
        self.username = params['username'] if 'username' in params.keys() else None
        self.password = params['password'] if 'password' in params.keys()  else None

        self.firstname = params['firstname'] if 'firstname' in params.keys()  else None
        self.lastname = params['lastname'] if 'lastname' in params.keys()  else None
        self.id = params['id'] if 'id' in params.keys()  else None
        self.email = params['email'] if 'email' in params.keys()  else None
        self.phonenumber = params['phonenumber'] if 'phonenumber' in params.keys()  else None

        self.authorizations = params['authorizations'] if 'authorizations' in params.keys()  else None
        self.groups = params['groups'] if 'groups' in params.keys()  else None

        self.newgroupdescription = params['description'] if 'description' in params.keys()  else None
        self.newgroupdetails = params['details'] if 'details' in params.keys()  else None
        self.newgroupauthorizations = params['authorizations'] if 'authorizations' in params.keys()  else None


    def get_params_from_GET(self, request):
        # Get param from request body as python object
        params = request.GET
        
        # Get individual params
        self.username = params['username'] if 'username' in params.keys() else None
        self.password = params['password'] if 'password' in params.keys()  else None

        print ('Username: ' + str(self.username))
    


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Login(AuthenticationBaseView):
    
    def get(self, request):
        # Get param from request body as python object
        self.get_params_from_GET(request)
        
        # Get controller & authenticate with credentials
        controller = self.controller.authenticationController
        controller.authenticate(self.username, self.password)
        

        print('back from service')

        # if user is authenticated
        if self.viewModel.messages["status"] == "Success":
            # Get tokenManager
            tokenManager = JwtTokenManager()

            payload = self.viewModel.user

            print("payload:------ " + str(payload['username']))
            # Create token
            token = tokenManager.create_token(payload)

            response = HttpResponse(token)
            # Get response from model
            return response

        # if user is not authenticated:
        elif self.viewModel.messages["status"] == "Failure":
            return JsonResponse({'messages':{'status':'Failure', 'message':'User not authenticated!'}})

    def post(self, request):
        # Get param from request body as python object
        self.get_params_from_request(request)

        if self.username != None: # and self.firstname != None and self.lastname != None:
            print("In post, self.username not none! " + str(self.username))
            
            # Get controller & authenticate with credentials
            controller = self.controller.authenticationController
            controller.authenticate(self.username, self.password)
            
            # if user is authenticated
            if self.viewModel.messages["status"] == "Success":
                # Get tokenManager
                tokenManager = JwtTokenManager()

                payload = {'user': self.viewModel.user}

                user = payload['user']

                print("payload:------ " + str(user['username']))
                # Create token
                token = tokenManager.create_token(payload)

                response = JsonResponse({
                    'username': self.username,
                    'email': self.viewModel.user['email'],
                    'name': self.viewModel.user['firstname'] + ' ' + self.viewModel.user['lastname'],
                    'token': token.decode('utf-8')
                    })
                # Get response from model
                return response

            # if user is not authenticated:
            elif self.viewModel.messages["status"] == "Failure":
                response = JsonResponse({ 'error': 'User not authenticated!'}, status=401)
                # response['error'] = 'User not authenticated!'
                return response


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Users(AuthenticationBaseView):
    
    # Old version
    # def get(self, request):
    #     # Get param from request body as python object
    #     self.get_params_from_GET(request)
        
    #     # Get controller & authenticate with credentials
    #     controller = self.controller.authenticationController
    #     controller.getuser(self.username)

    #     # Get response from model
    #     return JsonResponse({'user': self.viewModel.user, 'messages':self.viewModel.messages}, safe=False)

    def get(self, request):
        # token protected
        # Get param from request body as python object
        self.get_params_from_GET(request)

        # validate token
        # tokenManager = JwtTokenManager()
        
        # username = tokenManager.authenticate(request)

        # print('logged username: '+ str(username))
        # print('requested username: '+ str(self.username))
        
        #if username != None:
        # Get controller & authenticate with credentials
        
        print('In Users.get')
        print('user is', request.user)
        controller = self.controller.authenticationController
        controller.getuser(request.user['username'])
        print('In Users.get, request.user is: ', request.user)
        controller.getusers()

        # Get response from model
        return JsonResponse({'users': self.viewModel.users, 'user': self.viewModel.user, 'messages':self.viewModel.messages}, safe=False)

    def post(self, request):
        # Get param from request body as python object
        self.get_params_from_request(request)

        print("In create user!")
        print(str(self.paramsforcheck))

        if self.username != None: # and self.firstname != None and self.lastname != None:
            print("In post, self.username not none! " + str(self.username))
            inputData = {
                'username' :  self.username if self.username != None else None,
                'firstname' : self.firstname if self.firstname != None else None,
                'lastname' : self.lastname if self.lastname != None else None,
                'password' : self.password if self.password != None else None,
                'email' : self.email if self.email != None else None,
                'phonenumber' : self.phonenumber if self.phonenumber != None else None,
                'authorizations' : self.authorizations if self.authorizations != None else None,
                'groups' : self.groups if self.groups != None else None,
            }

            print("In post, self.username not none! " + str(inputData["username"]))
            print("In post, inputData is: " + str(inputData))
            # Get controller & create new user
            controller = self.controller.authenticationController
            controller.createuser(inputData)

            # Get response from model
            print('result: ' + str(self.viewModel.user))

            return JsonResponse({'user': self.viewModel.user, 'messages':{'status': 'Failure', 'message': self.viewModel.messages['message']}}, safe=False)
        else:
            return JsonResponse({'messages': {'status':'Failure'}}, safe=False)

    def delete(self, request):
        self.controller.authenticationController.delete_allusers()

        return JsonResponse({'messages': 'All users deleted!'}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class User(AuthenticationBaseView):
    
    # Old version
    # def get(self, request):
    #     # Get param from request body as python object
    #     self.get_params_from_GET(request)
        
    #     # Get controller & authenticate with credentials
    #     controller = self.controller.authenticationController
    #     controller.getuser(self.username)

    #     # Get response from model
    #     return JsonResponse({'user': self.viewModel.user, 'messages':self.viewModel.messages}, safe=False)

    def get(self, request, username):
        # token protected
        # Get param from request body as python object
        # self.get_params_from_GET(request)

        # validate token
        #tokenManager = JwtTokenManager()
        #username = tokenManager.authenticate(request)

        print('In User, logged username: '+ str(username))
        
        if username != None:
            # Get controller & authenticate with credentials
            controller = self.controller.authenticationController
            controller.getuser(username)

            # Get response from model
            return JsonResponse({'user': self.viewModel.user, 'messages':self.viewModel.messages}, safe=False)

    def delete(self, request, username):
        if username != None:
            controller = self.controller.authenticationController
            inputData = {'id': username}
            controller.deleteuser(inputData)
            controller.getusers()

            return JsonResponse({
                'user': self.viewModel.user,
                'users': self.viewModel.users
                })
        else:
            return JsonResponse({
                'messages': {
                    'status': 'Failure',
                    'message': 'User Id not valid!'
                }
            })

    def put(self, request, username):
        self.get_params_from_request(request)

        print("In update user!")

        if self.username != None: # and self.firstname != None and self.lastname != None:
            print("In post, self.username not none! " + str(self.username))
            inputData = {
                'id': self.id if self.id != None else None,
                'username' :  self.username if self.username != None else None,
                'firstname' : self.firstname if self.firstname != None else None,
                'lastname' : self.lastname if self.lastname != None else None,
                'password' : self.password if self.password != None else None,
                'email' : self.email if self.email != None else None,
                'phonenumber' : self.phonenumber if self.phonenumber != None else None,
                'authorizations' : self.authorizations if self.authorizations != None else None,
                'groups' : self.groups if self.groups != None else None,
            }

            print("In put, self.username not none! " + str(inputData["username"]))
            print("In put, self.id not none! " + str(inputData["id"]))

            # Get controller & update user
            controller = self.controller.authenticationController
            controller.updateuser(inputData)

            # Get response from model
            return JsonResponse({'user': self.viewModel.user}, safe=False)
        else:
            return JsonResponse({'messages': self.viewModel.messages}, safe=False)



@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class JwtAuthenticator(AuthenticationBaseView):
    
    def get(self, request):
        # Get param from request body as python object
        self.get_params_from_GET(request)
        
        # Get authenticator
        tokenManager = JwtTokenManager()

        token = ''

        token = tokenManager.create_token(request)
        response = HttpResponse(token)

        # Get response from model
        return response


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Models(AuthenticationBaseView):

    def get(self, request):
        controller = self.controller.authenticationController
        controller.getmodels()

        return JsonResponse({'models': self.viewModel.models})


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Groups(AuthenticationBaseView):

    def get(self, request):
        controller = self.controller.authenticationController
        controller.getgroups()

        return JsonResponse({'groups': self.viewModel.groups})

    def post(self, request):
        self.get_params_from_request(request)

        if self.username != None: # and self.firstname != None and self.lastname != None:
            print("In post, self.username not none! " + str(self.username))
            inputData = {
                #'username' :  self.username,
                'description' : self.newgroupdescription,
                'details' : self.newgroupdetails,
                'authorizations' : self.newgroupauthorizations,
            }

        controller = self.controller.authenticationController
        controller.creategroup(inputData)

        return JsonResponse({'group': self.viewModel.group})

    def delete(self, request, id):
        self.get_params_from_request(request)

        if self.username != None: # and self.firstname != None and self.lastname != None:
            print("In post, self.username not none! " + str(self.username))
            inputData = {
                #'username' :  self.username,
                'groupid' : id,
            }

        controller = self.controller.authenticationController
        controller.deletegroup(inputData)

        return JsonResponse({
                'deletedgroup': self.viewModel.group, 
                'groups': self.viewModel.groups
            })

    def put(self, request, id):
        self.get_params_from_request(request)

        if self.username != None: # and self.firstname != None and self.lastname != None:
            print("In post, self.username not none! " + str(self.username))
            inputData = {
                #'username' :  self.username,
                'groupid' : id,
                'description': self.newgroupdescription,
                'details': self.newgroupdetails,
                'authorizations': self.newgroupauthorizations
            }

        controller = self.controller.authenticationController
        controller.updategroup(inputData)

        return JsonResponse({
                'group': self.viewModel.group, 
            })
    