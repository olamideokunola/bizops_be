import unittest
import datetime

from domain.users.Users import User, Group, Authorization
from domain.dataAccess.ShelveDatabase import ShelveDataBaseManager
from domain.dataAccess.UsersDataAccess import ShelveUsersDataAccess

from domain.services.AuthenticationServices import UsersDataAccessInterface, AuthenticationInputData, AuthenticationInputInterface, AuthenticationOutputInterface, AuthenticationService
from domain.services.AuthenticationPresenters import AuthenticationViewModel, AuthenticationOutputData, AuthenticationPresenter
from domain.controllers.AuthenticationControllers import AuthenticationController

import db_tests

class UserAuthenticationServiceTest(unittest.TestCase):        
    userDataAccess = None
    newuser = None

    def setup_userdb(self):
        db_manager = ShelveDataBaseManager(db_tests.dblocation)
        self.userDataAccess = ShelveUsersDataAccess(db_manager)

        self.newuser = User('Joy', 'Okunola','joy', 'allow', 'joy@favychos.com')

    def setup_authentication(self):
        self.inputData = AuthenticationInputData()
        userDataInterface = self.userDataAccess
        
        self.outputData = AuthenticationOutputData()
        self.viewModel = AuthenticationViewModel()
        self.presenter = AuthenticationPresenter(self.viewModel)

        self.authenticateService = AuthenticationService(self.inputData, userDataInterface, self.presenter)
        
    def test_user(self):
        self.setup_userdb()

        self.assertEqual(self.newuser.username, 'joy')
        self.assertEqual(self.newuser.id, 'joy')
        self.assertEqual(self.newuser.get_firstname(), 'Joy')
        self.assertEqual(self.newuser.get_lastname(), 'Okunola')
        self.assertEqual(self.newuser.get_password(), 'allow')

    def test_get_username(self):
        self.setup_userdb()
        self.userDataAccess.save(self.newuser)

        saveduser = self.userDataAccess.get(self.newuser.username)

        self.assertEqual(self.newuser.username, saveduser.username)
        self.assertEqual(self.newuser.username, self.userDataAccess.get_username(self.newuser.username))
        self.assertEqual(self.newuser.get_password(), self.userDataAccess.get_password(self.newuser.username))

    def test_authenticate(self):
        self.setup_userdb()
        self.userDataAccess.save(self.newuser)

        self.setup_authentication()

        self.inputData.username = 'joy'
        self.inputData.password = 'allow'

        self.authenticateService.authenticate()
        print(self.viewModel.user)
        self.assertTrue(self.viewModel.user['isAuthenticated'])

class UserAuthenticationControllerTest(unittest.TestCase):        
    userDataAccess = None
    newuser = None

    def setup_userdb(self):
        db_manager = ShelveDataBaseManager(db_tests.dblocation)
        self.userDataAccess = ShelveUsersDataAccess(db_manager)

        self.newuser = User('Joy', 'Okunola','joy', 'allow', 'joy@favychos.com')

    def setup_controller(self):
        self.inputData = AuthenticationInputData()
        userDataInterface = self.userDataAccess
        
        self.outputData = AuthenticationOutputData()
        self.viewModel = AuthenticationViewModel()
        self.presenter = AuthenticationPresenter(self.viewModel)

        self.authenticateService = AuthenticationService(self.inputData, userDataInterface, self.presenter)

        self.authenticateController = AuthenticationController(self.inputData, self.authenticateService)
        
    def test_authenticate(self):
        self.setup_userdb()
        self.userDataAccess.save(self.newuser)

        self.setup_controller()

        self.authenticateController.authenticate('joy', 'allow')

        print(self.viewModel.user)
        self.assertTrue(self.viewModel.user['isAuthenticated'])

    def test_getuser(self):
        self.setup_userdb()
        self.userDataAccess.save(self.newuser)

        self.setup_controller()

        self.authenticateController.getuser('joy')

        print(self.viewModel.user)
        self.assertEqual('joy', self.viewModel.user['username'])

# Tests fot authorizations and groups
class UserAuthorizationsTest(unittest.TestCase):    
    def setup_user(self):
        self.user = User("Olamide", "Okunola")  

        # Add groups
        sellerGroup = Group("Sellers", '')
        sellerGroup.id = 1

        bakerGroup = Group("Bakers", '')
        bakerGroup.id = 2

        self.user.add_group(sellerGroup)
        self.user.add_group(bakerGroup) 

        # Add authorizations
        auth1 = Authorization(description="auth1", model="User", id=1, create=True, delete=True )
        auth2 = Authorization(description="auth2", model="User", id=2)

        self.user.add_authorization(auth1)
        self.user.add_authorization(auth2) 

    def test_add_group(self):
        self.setup_user()

        self.assertGreater(len(self.user.groups), 1)
        self.assertEquals(len(self.user.groups), 2)

    def test_get_group(self):
        self.setup_user()

        grp1 = self.user.get_group(1)
        grp2 = self.user.get_group(2)
    
        self.assertEquals(grp1.description, "Sellers")
        self.assertEquals(grp2.description, "Bakers")

    def test_remove_group(self):
        self.setup_user()
        InitialItems = len(self.user.groups)
        
        self.assertGreater(InitialItems, 1)
        
        self.user.remove_group(2)

        self.assertGreater(InitialItems, 1)

    def test_add_authorization(self):
        self.setup_user()

        self.assertGreater(len(self.user.authorizations), 1)
        self.assertEquals(len(self.user.authorizations), 2)

    def test_get_authorization(self):
        self.setup_user()

        auth1 = self.user.get_authorization(1)
        auth2 = self.user.get_authorization(2)

        # print ("auths: " + str(self.user.authorizations))
        # print ("auth: " + str(self.user.authorizations[1].id) + str(self.user.authorizations[1].name))

        self.assertEquals(auth1.description, "auth1")
        self.assertEquals(auth2.description, "auth2")

    def test_remove_authorization(self):
        self.setup_user()
        InitialItems = len(self.user.authorizations)
        
        self.assertGreater(InitialItems, 1)
        
        self.user.remove_authorization(2)

        self.assertGreater(InitialItems, 1)

    def test_authorization_clear(self):
        self.setup_user()

        auth1 = self.user.get_authorization(1)

        auth1.clear()
        
        self.assertFalse(auth1.delete)
        self.assertFalse(auth1.create)

class UserGroupTest(unittest.TestCase):    
    def setup_group(self):
        self.group = Group("Bakers", "")  

        # Add authorization
        self.group.add_authorization(Authorization("auth1","User", id=1))
        self.group.add_authorization(Authorization("auth2","User",id=2))

    def test_add_authorization(self):
        self.setup_group()

        self.assertGreater(len(self.group.authorizations), 0)

    def test_update_authorization(self):
        self.setup_group()

        auth1 = self.group.get_authorization(1)

        auth1.name = "newauth1"

        self.assertEqual(auth1.name, "newauth1")

    def test_remove_authorization(self):
        self.setup_group()

        initialSize = len(self.group.authorizations)

        self.group.remove_authorization(1)

        self.assertGreater(initialSize, len(self.group.authorizations))

    def test_clear_authorizations(self):
        self.setup_group()

        self.group.clear_authorizations()

        self.assertEqual(len(self.group.authorizations), 0)

