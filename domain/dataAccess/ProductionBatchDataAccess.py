from datetime import date
from domain.production.ProductionBatchDataAccessInterface import ProductionBatchDataAccessInterface
from domain.dataAccess.DatabaseInterface import DatabaseManagerInterface, DataAccessInterface

class ShelveProductionBatchDataAccess(ProductionBatchDataAccessInterface, DataAccessInterface): 
    database = None

    def __init__(self, database_manager_interface_object):
        if isinstance(database_manager_interface_object, DatabaseManagerInterface):
            self.database = database_manager_interface_object
    
    def save(self, productionBatch):
        return self.database.save('salesdb', 'ProductionBatch', productionBatch)
    
    def delete(self, productionBatch):
        return self.database.delete('salesdb', 'ProductionBatch', productionBatch)
    
    def get(self, id):
        return self.database.get('salesdb', 'ProductionBatch', id)
    
    def get_day_production_batches(self, date):
        return self.database.get_day_items('salesdb', 'ProductionBatch', date)

    def get_all(self):
        return self.database.get_all('salesdb', 'ProductionBatch')

    def get_production_batch(self, date, id):
        return self.database.get_day_item('salesdb', 'ProductionBatch', date, id)
