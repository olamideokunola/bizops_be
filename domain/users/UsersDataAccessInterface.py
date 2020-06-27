from abc import ABC, abstractmethod

# an interface for manager product data access
class UsersDataAccessInterface(ABC):
    @abstractmethod
    def get_username(self, id):
        pass

    @abstractmethod
    def get_password(self, id):
        pass
    
    @abstractmethod
    def get_by_username(self, username):
        pass

