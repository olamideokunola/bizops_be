from datetime import date
from domain.users.GroupsDataAccessInterface import GroupsDataAccessInterface
from domain.dataAccess.DatabaseInterface import DatabaseManagerInterface, DataAccessInterface

class ShelveGroupsDataAccess(GroupsDataAccessInterface, DataAccessInterface): 
    database = None

    def __init__(self, database_manager_interface_object):
        if isinstance(database_manager_interface_object, DatabaseManagerInterface):
            self.database = database_manager_interface_object
    
    def save(self, group):
        print("In save, group description: " + str(group.description))
        return self.database.save('salesdb', 'Group', group)
    
    def delete(self, group):
        return self.database.delete('salesdb', 'Group', group)

    def get(self, id):
        return self.database.get('salesdb', 'Group', id)

    def get_all(self):
        return self.database.get_all('salesdb', 'Group')

    def get_groups(self):
        return self.get_all()



    

        
