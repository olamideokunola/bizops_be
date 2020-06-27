import datetime

from domain.users.Users import User, Group, Authorization
from domain.dataAccess.ShelveDatabase import ShelveDataBaseManager
from domain.dataAccess.UsersDataAccess import ShelveUsersDataAccess
from domain.dataAccess.GroupsDataAccess import ShelveGroupsDataAccess

from domain.dataAccess.DjangoDataAccess.DjangoDatabase import DjangoDataBaseManager

from domain.services.AuthenticationServices import UsersDataAccessInterface, AuthenticationInputData, AuthenticationInputInterface, AuthenticationOutputInterface, AuthenticationService
from domain.services.AuthenticationPresenters import AuthenticationViewModel, AuthenticationOutputData, AuthenticationPresenter
from domain.controllers.AuthenticationControllers import AuthenticationController

from managerdeleteuser import deleteuser
 
from system.settings import defaultUser

# setup db
db_manager = DjangoDataBaseManager()
userDataAccess = ShelveUsersDataAccess(db_manager)
groupDataAccess = ShelveGroupsDataAccess(db_manager)

# setup service
inputData = AuthenticationInputData()

outputData = AuthenticationOutputData()
viewModel = AuthenticationViewModel()
presenter = AuthenticationPresenter(viewModel)

authenticateService = AuthenticationService(inputData, outputData, userDataAccess,groupDataAccess, presenter)


inputData.username = defaultUser['username']
inputData.firstname = defaultUser['firstname']
inputData.lastname = defaultUser['lastname']
inputData.password = defaultUser['password']
inputData.email = defaultUser['email']
inputData.phonenumber = defaultUser['phonenumber']
# inputData.authorizations = defaultUser['authorizations']
inputData.authorizations = [  Authorization(
    model=auth['model'] ,
    description=auth['description'],
    create=auth['create'] ,
    edit=auth['edit'],
    view=auth['view'],
    delete=auth['delete']
) for auth in defaultUser['authorizations']]

inputData.groups = [  Group(
    description=group['description'],
    details=group['details'],
) for group in defaultUser['groups']]

authenticateService.getuser()
userid=outputData.user.id
print('userid', userid)
inputData.id = userid

# deleteuser(inputData.username)
authenticateService.createuser()

if  outputData.user != None:
    print('User', outputData.user.username , 'created!')
    print('User id is ', outputData.user.id)
else:
    print('User creation failed!')