from datetime import date
from domain.customers.CustomersDataAccessInterface import CustomersDataAccessInterface
from domain.dataAccess.DatabaseInterface import DatabaseManagerInterface, DataAccessInterface

class ShelveCustomersDataAccess(CustomersDataAccessInterface, DataAccessInterface): 
    database = None

    def __init__(self, database_manager_interface_object):
        if isinstance(database_manager_interface_object, DatabaseManagerInterface):
            self.database = database_manager_interface_object
    
    def save(self, customer):
        return self.database.save('salesdb', 'Customer', customer)

    def delete(self, customer):
        return self.database.delete('salesdb', 'Customer', customer)
         
    def get(self, id):
        return self.database.get('salesdb', 'Customer', id)

    def get_customer(self, id):
        print('id is', id)
        print('customer is', self.get(id))
        return self.get(id)

    def get_customers(self):
        return self.database.get_all('salesdb', 'Customer')
    
    
    

        
