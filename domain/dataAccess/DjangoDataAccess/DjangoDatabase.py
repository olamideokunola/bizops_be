from datetime import date
import shelve
import os

from domain.dataAccess.DatabaseInterface import DatabaseManagerInterface
from web.bizops_backend.sales_api.models import Sale

class SaleModelManager:
    def create(self, outerSale):
        sale = Sale.objects.create(
            quantity = outerSale.quantity
        )
        sale.save()

        print (sale.quantity)

class DjangoDataBaseManager(DatabaseManagerInterface):
    saleModelManager = SaleModelManager()
    models = {
                'Sale': saleModelManager,
                # 'Product': Product, 
                # 'Customer': Customer, 
                # 'User': User, 
                # 'Group': Group, 
                # 'Authorization': Authorization, 
                # 'Price': Price,
                # 'Unit': Unit,
                # 'ProductionBatch': ProductionBatch
            }      

    def __init__(self, dblocation=None):
        pass
    
    def save(self, databasename, modelname, item):
        model = self.models[modelname]
        model.create(item)
        return None
    
    def delete(self, databasename, modelname, item):
        return None

    def create_new_id(self, databasename, modelname):
        return None
 
    def get(self, databasename, modelname, id):
        return None

    def get_many(self, databasename, modelname, ids):
        return None

    def get_day_items(self, databasename, modelname, date):
        return None
    
    def get_day_item(self, databasename, modelname, date, id):
        return None

    def get_all(self, databasename, modelname):
        return None


        

# class Database():
#     name = ''
#     dblocation = ''
#     models = {}
#     model = None

#     def __init__(self, name, dblocation):
#         pass
#     #     self.name = name
#     #     self.dblocation = dblocation + name + '/'
   
#     # def create_model(self, modelname):
#     #     if modelname not in self.models.keys():
#     #         self.models[modelname] = shelve.open(self.dblocation+modelname)

#     def get_model(self, modelname):
#         if modelname in self.models.keys():
#             #return self.models[modelname]
#             return shelve.open(self.dblocation+modelname)

#     def save(self, modelname, item):
#         model = self.get_model(modelname)
#         print("id: " + str(item.id))
#         if item.id != None:
#             #save            
#             print ('id: ' + str(item.id))
#             model[str(item.id)] = item
#         else:
#             #create new id
#             newid = self.create_new_id(modelname)
#             #save with new id
#             item.id = newid
#             model[str(newid)] = item
            
#         return item

#     def delete(self, modelname, item):
#         model = self.get_model(modelname)
#         print("id: " + str(item.id))

#         if item.id != None:
#             #delete            
#             print ('id: ' + str(item.id))
#             return model.pop(str(item.id))

#     def create_new_id(self, modelname):
#         model = self.get_model(modelname)
#         if len(model.keys()) > 0:
#             ids = [ item.id for item in model.values() if item.id != None]
#             newid = max(ids) + 1
#         else:
#             newid = 1

#         return newid
        
#     def get(self, modelname, id):
#         model = self.get_model(modelname)

#         if str(id) in model.keys():
#             return model[str(id)]
#         else:
#             return None

#     def get_many(self, modelname, ids):
#         model = self.get_model(modelname)
#         items = []  

#         try:
#             for id in ids:
#                 items.append(self.get(modelname, id))
#         except AttributeError:
#             model.close()
#             return None
#         else:
#             model.close()
#             return items
    
#     def get_day_items(self, modelname, date):
#         model = self.get_model(modelname)
#         items = [] 

#         for key in model.keys():
#             if model[key].date == date:
#                 items.append(model[key])
#         model.close()
#         return items
    
#     def get_day_item(self, modelname, date, id):
#         model = self.get_model(modelname)

#         if str(id) in model.keys():
#             if model[str(id)].date == date:
#                 return model[str(id)]
#             else:
#                 print('Item is not for date!')
#                 model.close()
#                 return None
#         else:
#             print('Item not in database!')
#             model.close()
#             return None

#     def get_all(self, modelname):
#         model = self.get_model(modelname)
#         items = [] 
        
#         for key in model.keys():
#             print (key)
#             if key in model:
#                 print (model[key])
#             else: print('None')

#         for key in model.keys():
#             items.append(model[key])

#         model.close()
#         return items
        
