from datetime import date
from domain.users.UsersDataAccessInterface import UsersDataAccessInterface
from domain.dataAccess.DatabaseInterface import DatabaseManagerInterface, DataAccessInterface

class ShelveUsersDataAccess(UsersDataAccessInterface, DataAccessInterface): 
    database = None

    def __init__(self, database_manager_interface_object):
        if isinstance(database_manager_interface_object, DatabaseManagerInterface):
            self.database = database_manager_interface_object
    
    def save(self, user):
        print("In save, user id: " + str(user.username))
        return self.database.save('salesdb', 'User', user)

    def delete(self, user):
        return self.database.delete('salesdb', 'User', user)

    def get(self, id):
        return self.database.get('salesdb', 'User', id)

    def get_all(self):
        return self.database.get_all('salesdb', 'User')

    def get_username(self, username):
        return self.get(username).username

    def get_password(self, username):
        if self.get(username) != None:
            return self.get(username).get_password()
        else:
            return None
    
    
    

        
