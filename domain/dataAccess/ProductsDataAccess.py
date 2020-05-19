from datetime import date
from domain.products.ProductsDataAccessInterface import ProductsDataAccessInterface
from domain.dataAccess.DatabaseInterface import DatabaseManagerInterface, DataAccessInterface

class ShelveProductsDataAccess(ProductsDataAccessInterface, DataAccessInterface): 
    database = None

    def __init__(self, database_manager_interface_object):
        if isinstance(database_manager_interface_object, DatabaseManagerInterface):
            self.database = database_manager_interface_object
    
    def save(self, product):
        return self.database.save('salesdb', 'Product', product)
    
    def delete(self, product):
        return self.database.delete('salesdb', 'Product', product)
         
    def get(self, id):
        return self.database.get('salesdb', 'Product', id)

    def get_product(self, id):
        return self.get(id)

    def get_products(self):
        return self.database.get_all('salesdb', 'Product')
    
    
    

        
