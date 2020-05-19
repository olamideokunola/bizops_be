from datetime import date
from domain.sales.SalesDataAccessInterface import SalesDataAccessInterface
from domain.dataAccess.DatabaseInterface import DatabaseManagerInterface, DataAccessInterface

class ShelveSalesDataAccess(SalesDataAccessInterface, DataAccessInterface): 
    database = None

    def __init__(self, database_manager_interface_object):
        if isinstance(database_manager_interface_object, DatabaseManagerInterface):
            self.database = database_manager_interface_object
    
    def save(self, sale):
        return self.database.save('salesdb', 'Sale', sale)
    
    def delete(self, sale):
        return self.database.delete('salesdb', 'Sale', sale)
    
    def get(self, id):
        return self.database.get('salesdb', 'Sale', id)
    
    def get_day_sales(self, date):
        return self.database.get_day_items('salesdb', 'Sale', date)

    def get_sales(self):
        return self.database.get_all('salesdb', 'Sale')

    def get_day_sale(self, date, id):
        return self.database.get_day_item('salesdb', 'Sale', date, id)
