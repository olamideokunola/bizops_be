from datetime import date
from domain.products.UnitsDataAccessInterface import UnitsDataAccessInterface
from domain.dataAccess.DatabaseInterface import DatabaseManagerInterface, DataAccessInterface

class ShelveUnitsDataAccess(UnitsDataAccessInterface, DataAccessInterface): 
    database = None

    def __init__(self, database_manager_interface_object):
        if isinstance(database_manager_interface_object, DatabaseManagerInterface):
            self.database = database_manager_interface_object
    
    def save(self, unit):
        return self.database.save('salesdb', 'Unit', unit)
    
    def delete(self, unit):
        return self.database.delete('salesdb', 'Unit', unit)
         
    def get(self, id):
        return self.database.get('salesdb', 'Unit', id)

    def get_unit(self, id):
        return self.get(id)

    def get_units(self):
        return self.database.get_all('salesdb', 'Unit')
    
    
    

        
