from abc import ABC, abstractmethod

# an interface for generic Database Facade
class DatabaseManagerInterface(ABC):
    @abstractmethod
    def save(self, databasename, modelname, item):
        pass

    @abstractmethod
    def delete(self, databasename, modelname, item):
        pass
    
    @abstractmethod
    def create_new_id(self, databasename, modelname):
        pass

    @abstractmethod 
    def get(self, databasename, modelname, id):
        pass

    @abstractmethod 
    def get_many(self, databasename, modelname, ids):
        pass

    @abstractmethod 
    def get_day_items(self, databasename, modelname, date):
        pass

    @abstractmethod 
    def get_day_item(self, databasename, modelname, date, id):
        pass

    @abstractmethod 
    def get_all(self, databasename, modelname):
        pass


# an interface for generic database
class DatabaseInterface(ABC):
    @abstractmethod
    def save(self, modelname, item):
        pass

    @abstractmethod
    def delete(self, modelname, item):
        pass
    
    @abstractmethod
    def create_new_id(self, modelname):
        pass

    @abstractmethod 
    def get(self, modelname, id):
        pass

    @abstractmethod 
    def get_many(self, modelname, ids):
        pass

    @abstractmethod 
    def get_day_items(self, modelname, date):
        pass

    @abstractmethod 
    def get_day_item(self, modelname, date, id):
        pass

    @abstractmethod 
    def get_all(self, modelname):
        pass

class DataAccessInterface(ABC): 

    @abstractmethod 
    def save(self, item):
        pass

    @abstractmethod 
    def delete(self, item):
        pass
    
    @abstractmethod 
    def get(self, id):
        pass

