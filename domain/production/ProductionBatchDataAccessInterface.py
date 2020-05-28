from abc import ABC, abstractmethod

# an interface for manager product data access
class ProductionBatchDataAccessInterface(ABC):

    @abstractmethod
    def get_production_batch(self, date, id):
        pass

    @abstractmethod
    def get_day_production_batches(self, date):
        pass

    @abstractmethod
    def get_all(self):
        pass


