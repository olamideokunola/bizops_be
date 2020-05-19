from abc import ABC, abstractmethod

# an interface for manager product data access
class ProductsDataAccessInterface(ABC):
    @abstractmethod
    def get_product(self, id):
        pass

    @abstractmethod
    def get_products(self):
        pass


