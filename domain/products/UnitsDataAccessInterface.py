from abc import ABC, abstractmethod

# an interface for manager unit data access
class UnitsDataAccessInterface(ABC):
    @abstractmethod
    def get_unit(self, id):
        pass

    @abstractmethod
    def get_units(self):
        pass


