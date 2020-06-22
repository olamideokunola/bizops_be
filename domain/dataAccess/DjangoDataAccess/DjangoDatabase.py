from datetime import date
import shelve
import os

from domain.dataAccess.DatabaseInterface import DatabaseManagerInterface

import django
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.bizops_backend.bizops_backend.settings'
print('Settings module: ' + os.environ['DJANGO_SETTINGS_MODULE'])

import sys

print('Settings module: ' + os.environ['DJANGO_SETTINGS_MODULE'])

sales_api_module_path = settings.BASE_DIR 

print('settings.BASE_DIR is ' + settings.BASE_DIR )

if settings.BASE_DIR not in sys.path:
    sys.path.append(settings.BASE_DIR)

# for path in sys.path:
#     print(path)

try:
    django.setup()
except Exception as ex:
    print(ex)


from sales_api.models import Sale, Price, Product, Authorization
from domain.sales.Sales import Sale as SaleEntity
from domain.users.Users import Authorization as AuthorizationEntity
from abc import ABC

class AbstractModelManager(ABC):
    def create(self, entityObject):
        pass

    def get(self, id):
        pass

    def delete(self, entityObject):
        pass

    def get_all(self):
        pass

class Materializer(ABC):
    def create(self, entityObject):
        pass
    
    def materialize(self, entityObject):
        pass

class ModelManager(AbstractModelManager):
    ModelClass = None

    def create(self, entityObject):
        pass

    def get(self, id):
        return self.materialize(self.ModelClass.objects.get(pk=id))

    def delete(self, authObject):
        if authObject.id != None:

            auth = self.ModelClass.objects.get(pk=authObject.id)

            auth.delete()

            return self.materialize(auth)

    def get_all(self):
        print('In getall')
        if len(self.ModelClass.objects.all()) > 0:
            print('Items more than 0')
            return [self.materialize(auth) for auth in self.ModelClass.objects.all() ] 


class AuthorizationModelManager(ModelManager, Materializer):
    ModelClass = Authorization

    def create(self, authObject):
        if authObject == None:
            auth = Authorization.objects.create()
        else:
            if authObject.id == 0 or authObject.id == None:
                auth = Authorization.objects.create(
                    description = authObject.description,
                    model = authObject.model,
                    can_create = authObject.create,
                    can_change = authObject.change,
                    can_view = authObject.view,
                    can_delete = authObject.delete,
                )
            else:
                auth = Authorization.objects.get(pk=authObject.id)
                auth.description = authObject.description
                auth.model = authObject.model
                auth.can_create = authObject.create
                auth.can_change = authObject.change
                auth.can_view = authObject.view
                auth.can_delete = authObject.delete

        return self.materialize(auth)

    def materialize(self, authModel):
        return AuthorizationEntity(
            id=authModel.id,
            model=authModel.model,
            description=authModel.description,
            create=authModel.can_create,
            change=authModel.can_change,
            view=authModel.can_view,
            delete=authModel.can_delete,
        )

class SaleModelManager:
    def create(self, outerSale):
        print('In create')

        if outerSale == None:
            sale = Sale.objects.create()
        else:
            try:
                product = Product.objects.get(name=outerSale.product.name)
                print('Product is: ', str(product.id))
                sale = Sale.objects.create(
                    product = product,
                    quantity = outerSale.quantity,
                    price = outerSale.price.amount,
                    date = outerSale.date
                )

                sale.save()
                return sale

            except Product.DoesNotExist:
                print('Product does not Exist!')
                return None
    
    def materialize(self, sale):
        pass

    
    def get(self, id):
        print('In get')

        return Sale.objects.get(pk=id)

    def get_all(self):
        print('In get_all')
        pass

    def update(self, outerSale):
        print('In update')
        pass

    def delete(self, outerSale):
        print('In delete')
        pass



class DjangoDataBaseManager(DatabaseManagerInterface):
    saleModelManager = SaleModelManager()
    authorizationModelManager = AuthorizationModelManager()
    
    models = {
                'Sale': saleModelManager,
                # 'Product': Product, 
                # 'Customer': Customer, 
                # 'User': User, 
                # 'Group': Group, 
                'Authorization': authorizationModelManager, 
                # 'Price': Price,
                # 'Unit': Unit,
                # 'ProductionBatch': ProductionBatch
            }      

    def __init__(self, dblocation=None):
        pass
    
    def save(self, databasename, modelname, item):
        print('In Save')

        model = self.models[modelname]
        return model.create(item)
    
    def delete(self, databasename, modelname, item):
        model = self.models[modelname]
        return model.delete(item)

    def create_new_id(self, databasename, modelname):
        print('In create_new_id')

        item = self.save(databasename, modelname, None)
        return item.id
 
    def get(self, databasename, modelname, id):
        print('In get')

        model = self.models[modelname]
        return model.get(id)

    def get_many(self, databasename, modelname, ids):
        return None

    def get_day_items(self, databasename, modelname, date):
        return None
    
    def get_day_item(self, databasename, modelname, date, id):
        return None

    def get_all(self, databasename, modelname):
        model = self.models[modelname]
        return model.get_all()


        

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
        
