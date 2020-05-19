from abc import ABC, abstractmethod

# an interface for manager sales data access
class SalesDataAccessInterface(ABC):

    @abstractmethod
    def get_day_sales(self, date):
        pass

    @abstractmethod
    def get_day_sale(self, date, id):
        pass
