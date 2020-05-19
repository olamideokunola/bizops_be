from datetime import date
import shelve
import os

from domain.dataAccess.DatabaseInterface import DatabaseManagerInterface
from domain.common.Models import models

class ShelveDataBaseManager(DatabaseManagerInterface):
    databases = {}
    dblocation = "../../domain/dataAccess/ShelveDatabase/"
    #topfolder = "domain/dataAccess/ShelveDatabase/"
    
    databases_and_models = [
        {
            'databasename': 'salesdb',
            #'models': list(map(lambda model: model'[name']), models),
            #'models': [model['name']] for model in models,
            'models': [
                'Sale', 
                'Product', 
                'Customer', 
                'User', 
                'Group', 
                'Authorization', 
                'Price',
                'Unit'
                ]
        }
    ]

    def __init__(self, dblocation):
        self.dblocation = dblocation
        for database_and_models in self.databases_and_models:
            db = self.create_database(database_and_models['databasename'])
            for modelname in database_and_models['models']:
                db.create_model(modelname)

    def create_database(self, name):
        if name not in self.databases.keys():
            self.database = Database(name, self.dblocation)
            self.databases[name] = self.database
            self.__create_database_folder(name)
            return self.database
        else:
            return self.databases[name]

    def get_database(self, name):
        if name in self.databases.keys():
            return self.databases[name]

    def __create_database_folder(self, name):
        dirName = self.dblocation + name
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ")
        else:    
            print("Directory " , dirName ,  " already exists")
    
    def save(self, databasename, modelname, item):
        db = self.get_database(databasename)
        return db.save(type(item).__name__, item)
    
    def delete(self, databasename, modelname, item):
        db = self.get_database(databasename)
        return db.delete(type(item).__name__, item)

    def create_new_id(self, databasename, modelname):
        db = self.get_database(databasename)
        return db.create_new_id(modelname)
 
    def get(self, databasename, modelname, id):
        db = self.get_database(databasename)
        return db.get(modelname, id)

    def get_many(self, databasename, modelname, ids):
        db = self.get_database(databasename)
        return db.get_many(modelname, ids)

    def get_day_items(self, databasename, modelname, date):
        db = self.get_database(databasename)
        return db.get_day_items(modelname, date)
    
    def get_day_item(self, databasename, modelname, date, id):
        db = self.get_database(databasename)
        return db.get_day_item(modelname, date, id)

    def get_all(self, databasename, modelname):
        db = self.get_database(databasename)
        return db.get_all(modelname)


class Database():
    name = ''
    dblocation = ''
    models = {}
    model = None

    def __init__(self, name, dblocation):
        self.name = name
        self.dblocation = dblocation + name + '/'
   
    def create_model(self, modelname):
        if modelname not in self.models.keys():
            self.models[modelname] = shelve.open(self.dblocation+modelname)

    def get_model(self, modelname):
        if modelname in self.models.keys():
            #return self.models[modelname]
            return shelve.open(self.dblocation+modelname)

    def save(self, modelname, item):
        model = self.get_model(modelname)
        print("id: " + str(item.id))
        if item.id != None:
            #save            
            print ('id: ' + str(item.id))
            model[str(item.id)] = item
        else:
            #create new id
            newid = self.create_new_id(modelname)
            #save with new id
            item.id = newid
            model[str(newid)] = item
            
        return item

    def delete(self, modelname, item):
        model = self.get_model(modelname)
        print("id: " + str(item.id))

        if item.id != None:
            #delete            
            print ('id: ' + str(item.id))
            return model.pop(str(item.id))

    def create_new_id(self, modelname):
        model = self.get_model(modelname)
        if len(model.keys()) > 0:
            ids = [ item.id for item in model.values() if item.id != None]
            newid = max(ids) + 1
        else:
            newid = 1

        return newid
        
    def get(self, modelname, id):
        model = self.get_model(modelname)

        if str(id) in model.keys():
            return model[str(id)]
        else:
            return None

    def get_many(self, modelname, ids):
        model = self.get_model(modelname)
        items = []  

        try:
            for id in ids:
                items.append(self.get(modelname, id))
        except AttributeError:
            model.close()
            return None
        else:
            model.close()
            return items
    
    def get_day_items(self, modelname, date):
        model = self.get_model(modelname)
        items = [] 

        for key in model.keys():
            if model[key].date == date:
                items.append(model[key])
        model.close()
        return items
    
    def get_day_item(self, modelname, date, id):
        model = self.get_model(modelname)

        if str(id) in model.keys():
            if model[str(id)].date == date:
                return model[str(id)]
            else:
                print('Item is not for date!')
                model.close()
                return None
        else:
            print('Item not in database!')
            model.close()
            return None

    def get_all(self, modelname):
        model = self.get_model(modelname)
        items = [] 
        
        for key in model.keys():
            print (key)
            if key in model:
                print (model[key])
            else: print('None')

        for key in model.keys():
            items.append(model[key])

        model.close()
        return items
        
