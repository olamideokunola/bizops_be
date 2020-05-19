from abc import ABC, abstractmethod

# an interface for manager product data access
class CustomersDataAccessInterface(ABC):
    @abstractmethod
    def get_customer(self, id):
        pass

    @abstractmethod
    def get_customers(self):
        pass

