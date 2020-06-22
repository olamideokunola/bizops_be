from domain.services.AuthenticationServices import AuthenticationInputInterface, AuthenticationService, AuthenticationInputData
import datetime

class AuthenticationController:
    authenticationService = AuthenticationInputInterface
    authenticationInputData = AuthenticationInputData()

    def __init__(self, authenticationInputData, authenticationService):
        self.authenticationInputData = authenticationInputData
        if isinstance(authenticationService, AuthenticationInputInterface):
            self.authenticationService = authenticationService

    def authenticate(self, username, password):
        self.authenticationInputData.username = username
        self.authenticationInputData.password = password

        self.authenticationService.authenticate()

    def getuser(self, username):
        self.authenticationInputData.username = username
        self.authenticationService.getuser()

    def getusers(self):
        self.authenticationService.getusers()

    def __set_authenticationInputData(self, inputData):

        self.authenticationInputData.username = inputData['username'] if inputData['username'] != None else None

        self.authenticationInputData.firstname = inputData['firstname'] if inputData['firstname'] != None else None
        
        self.authenticationInputData.lastname = inputData['lastname'] if inputData['lastname']!= None else None

        self.authenticationInputData.password = inputData['password'] if inputData['password']!= None else None
        
        self.authenticationInputData.email = inputData['email'] if inputData['email'] != None else None
        
        self.authenticationInputData.phonenumber = inputData['phonenumber'] if inputData['phonenumber'] != None else None
        
        self.authenticationInputData.authorizations = inputData['authorizations'] if inputData['authorizations'] != None else None
        
        self.authenticationInputData.groups = inputData['groups'] if inputData['groups'] != None else None


    def createuser(self, inputData):
        print("In createuser of controller, username is: " + inputData["username"] )

        self.__set_authenticationInputData(inputData)
        
        self.authenticationService.createuser()
    
    def activateuser(self, inputData):
        if inputData['id'] != None:
            self.authenticationInputData.id = inputData['id']

            self.authenticationService.activate_user()

    def deactivateuser(self, inputData):
        if inputData['id'] != None:
            self.authenticationInputData.id = inputData['id']

            self.authenticationService.deactivate_user()

    def deleteuser(self, inputData):
        if inputData['id'] != None:
            self.authenticationInputData.id = inputData['id']

            self.authenticationService.deleteuser()
    
    def delete_allusers(self):
        self.authenticationService.delete_allusers()

    def updateuser(self, inputData):
        print("In createuser of controller, username is: " + inputData["username"] )
        
        self.authenticationInputData.id = inputData['id'] if inputData['id'] != None else None

        self.__set_authenticationInputData(inputData)
        
        self.authenticationService.updateuser()

    def getmodels(self):
        self.authenticationService.getmodels()

    def getgroups(self):
        self.authenticationService.getgroups()

    def creategroup(self, inputData):
        if inputData['description'] != None:
            self.authenticationInputData.description = inputData['description']
        if inputData['details'] != None:
            self.authenticationInputData.details = inputData['details']
        if inputData['authorizations'] != None:
            self.authenticationInputData.authorizations = inputData['authorizations']

        self.authenticationService.creategroup()

    def deletegroup(self, inputData):
        if inputData['groupid'] != None:
            self.authenticationInputData.groupid = inputData['groupid']
            
        self.authenticationService.deletegroup()

    def updategroup(self, inputData):
        if inputData['groupid'] != None:
            self.authenticationInputData.groupid = inputData['groupid']
        if inputData['description'] != None:
            self.authenticationInputData.description = inputData['description']
        if inputData['details'] != None:
            self.authenticationInputData.details = inputData['details']
        if inputData['authorizations'] != None:
            self.authenticationInputData.authorizations = inputData['authorizations']

        self.authenticationService.updategroup()
