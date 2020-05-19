from abc import ABC, abstractmethod

from domain.dataAccess.UsersDataAccess import UsersDataAccessInterface
from domain.dataAccess.GroupsDataAccess import GroupsDataAccessInterface
from domain.users.Users import User, Group
from domain.common.Models import models

class AuthenticationInputInterface(ABC):
    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def getuser(self):
        pass

    @abstractmethod
    def createuser(self):
        pass

    @abstractmethod
    def updateuser(self):
        pass

class AuthenticationInputData:
    id = None
    username = None
    password = None
    firstname = None
    lastname = None
    email = None
    phonenumber = None
    authorizations = None
    groups = None
    models = None
    description = None
    details = None

    

class AuthenticationOutputData:
    user = None
    messages = None
    groups = None

    def clear(self):
        self.user = None
        self.messages = None
        self.groups = None

class AuthenticationOutputInterface(ABC):
    @abstractmethod
    def set_user(self):
        pass

class Message:
    status = ''
    def __init__(self, status):
        self.status = status

class AuthenticationService(AuthenticationInputInterface):
    inputData = None
    userDataAccess = None
    groupDataAccess = None
    presenter = None
    
    def __init__(self, inputData, outputData, userDataAccess, groupDataAccess, presenter):
        if isinstance (inputData, AuthenticationInputData):
            self.inputData = inputData
        if isinstance (outputData, AuthenticationOutputData):
            self.outputData = outputData
        if isinstance(userDataAccess, UsersDataAccessInterface):
            self.userDataAccess = userDataAccess 
        if isinstance(groupDataAccess, GroupsDataAccessInterface):
            self.groupDataAccess = groupDataAccess 
        if isinstance(presenter, AuthenticationOutputInterface):
            self.presenter = presenter 
        
    def authenticate(self):
        user = self.userDataAccess.get(self.inputData.username)
        if  user != None and self.inputData.password == user.password:
            user.isAuthenticated = True
            
            self.outputData.user = user
            self.presenter.set_user(self.outputData)
            
            self.outputData.messages = Message('Success')
            self.presenter.set_messages(self.outputData)

            # self.outputData.status = True
            # self.presenter.set_status(self.outputData)
        else:
            self.outputData.user = User('','')
            self.presenter.set_user(self.outputData)

            self.outputData.messages = Message('Failure')
            self.presenter.set_messages(self.outputData)

    def __present_user(self, user):
        if  user != None:
            print('User is not None')
            self.outputData.user = user
            self.presenter.set_user(self.outputData)
        else:
            print('User is None')
            self.outputData.user = User('','')
            self.presenter.set_user(self.outputData)

    def getuser(self):
        user = self.userDataAccess.get(self.inputData.username)

        self.__present_user(user)

    def getusers(self):
        users = self.userDataAccess.get_all()

        if len(users) > 0:
            self.outputData.users = users
            self.presenter.set_users(self.outputData)

    def createuser(self):
        newuser = User( 
            self.inputData.firstname, 
            self.inputData.lastname, 
            self.inputData.username, 
            self.inputData.password, 
            self.inputData.email,
            self.inputData.phonenumber
        )
        newuser.id = self.inputData.username
        newuser.authorizations = self.inputData.authorizations
        newuser.groups = self.inputData.groups

        print("In create user service, inputData phonenumer " + str(self.inputData.phonenumber))
        print("In create user service, before save, phnenumber is: " + str(newuser.phonenumber))

        print("In create user service, username is: " + str(self.inputData.username))
        user = self.userDataAccess.save(newuser)
        
        print("In create user service, after save, phnenumber is: " + str(user.phonenumber))


        self.__present_user(user)
    
    def deleteuser(self):
        id = self.inputData.id
        usertodelete = self.userDataAccess.get(id)
        user = self.userDataAccess.delete(usertodelete)

        self.__present_user(user)

    def delete_allusers(self):
        users = self.userDataAccess.get_all()

        for user in users:
            self.userDataAccess.delete(user)

        if len(users) > 0:
            self.outputData.users = users
            self.presenter.set_users(self.outputData)

    def updateuser(self):
        user = User( 
            self.inputData.firstname, 
            self.inputData.lastname, 
            self.inputData.username, 
            self.inputData.password, 
            self.inputData.email,
            self.inputData.phonenumber
        )

        user.id = self.inputData.id
        user.authorizations = self.inputData.authorizations
        user.groups = self.inputData.groups
        print("In update user service, username is: " + str(self.inputData.username))
        self.outputData.clear()
        
        user = self.userDataAccess.save(user)
        
        self.__present_user(user)

    def getmodels(self):
        self.outputData.models = models
        self.presenter.set_models(self.outputData)      
    
    def getgroups(self):
        self.outputData.groups = self.groupDataAccess.get_groups()
        self.presenter.set_groups(self.outputData)

    def creategroup(self):
        group = Group(
            self.inputData.description,
            self.inputData.details,
        )
        group.authorizations = self.inputData.authorizations

        group = self.groupDataAccess.save(group)

        self.outputData.group = group
        self.presenter.set_group(self.outputData)

    def deletegroup(self):

        group = self.groupDataAccess.get(self.inputData.groupid)
        self.outputData.group = self.groupDataAccess.delete(group)

        self.presenter.set_group(self.outputData)
        self.getgroups()

    def updategroup(self):

        group = self.groupDataAccess.get(self.inputData.groupid)
        group.description = self.inputData.description
        group.details = self.inputData.details
        group.authorizations = self.inputData.authorizations

        group = self.groupDataAccess.save(group)

        self.outputData.group = group
        self.presenter.set_group(self.outputData)

