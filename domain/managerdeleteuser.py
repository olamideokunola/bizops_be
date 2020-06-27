import datetime

from domain.users.Users import User, Group, Authorization
from domain.dataAccess.ShelveDatabase import ShelveDataBaseManager
from domain.dataAccess.UsersDataAccess import ShelveUsersDataAccess
from domain.dataAccess.GroupsDataAccess import ShelveGroupsDataAccess

from domain.dataAccess.DjangoDataAccess.DjangoDatabase import DjangoDataBaseManager

from domain.services.AuthenticationServices import UsersDataAccessInterface, AuthenticationInputData, AuthenticationInputInterface, AuthenticationOutputInterface, AuthenticationService
from domain.services.AuthenticationPresenters import AuthenticationViewModel, AuthenticationOutputData, AuthenticationPresenter
from domain.controllers.AuthenticationControllers import AuthenticationController

from system.settings import defaultUser


def deleteuser(username):
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


    inputData.username = username

    authenticateService.getuser()
    userid=outputData.user.id

    if userid != None:

        print('userid', userid)
        inputData.id = userid
        authenticateService.deleteuser()

        # if  outputData.user != None:
        print('User', outputData.user.username , 'deleted!')
    else:
        print('User deletion failed!, user with username', inputData.username, 'not found!')


deleteuser('olamide')