from abc import ABC, abstractmethod

# an interface for manager product data access
class GroupsDataAccessInterface(ABC):
    pass
    @abstractmethod
    def get_groups(self, description):
        pass
    

