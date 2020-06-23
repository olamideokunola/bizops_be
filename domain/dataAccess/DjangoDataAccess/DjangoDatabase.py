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


from sales_api.models import Sale, Price, Product, Authorization, Group, Person, Customer, Unit, User, ProductionBatch
from domain.sales.Sales import Sale as SaleEntity
from domain.customers.Customers import Person as PersonEntity, Customer as CustomerEntity
from domain.users.Users import Authorization as AuthorizationEntity, Group as GroupEntity, User as UserEntity
from domain.products.Products import Unit as UnitEntity, Price as PriceEntity, Product as ProductEntity
from domain.production.ProductionBatch import ProductionBatch as ProductionBatchEntity
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

            item = self.ModelClass.objects.get(pk=authObject.id)

            print('item id is ', item.id)

            itemToDelete = self.materialize(item)

            numberOfItemsDeleted = item.delete()

            print('Items deleted are: ', numberOfItemsDeleted[0])

            if numberOfItemsDeleted[0] > 0:
                # delete success
                return itemToDelete
            else:
                # delete failed
                return None

    def get_all(self):
        print('In getall')
        if len(self.ModelClass.objects.all()) > 0:
            # print('Items more than 0')
            return [self.materialize(item) for item in self.ModelClass.objects.all() ] 

    def get_ids(self):
        print('In getids')
        return [item.id for item in self.ModelClass.objects.all()]

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

                auth.save()

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

class GroupModelManager(ModelManager, Materializer):
    ModelClass = Group

    def create(self, groupObject):
        if groupObject == None:
            group = Group.objects.create()
        else:
            # Save new
            if groupObject.id == 0 or groupObject.id == None:
                
                authorizations = [ Authorization.objects.get(pk=auth.id) for auth in groupObject.authorizations ] 
                
                group = Group.objects.create(
                    description = groupObject.description,
                    details = groupObject.details, 
                )
                group.authorizations.set(authorizations)
            else:
                # update existing
                group = Group.objects.get(pk=groupObject.id)
                group.description = groupObject.description
                group.details = groupObject.details

                authorizations = [ Authorization.objects.get(pk=auth.id) for auth in groupObject.authorizations ] 
                group.authorizations.set(authorizations)

                group.save()

        return self.materialize(group)

    def materialize(self, groupModel):

        groupEntity = GroupEntity(
            description=groupModel.description,
            details=groupModel.details,
        )

        groupEntity.id=groupModel.id
        groupEntity.authorizations=[{
                'id': authorization.id,
                'description': authorization.description,
                'model': authorization.model,
                'create': authorization.can_create,
                'change': authorization.can_change,
                'view': authorization.can_view,
                'delete': authorization.can_delete,
            } for authorization in groupModel.authorizations.all()]

        return groupEntity

class PersonModelManager(ModelManager, Materializer):
    ModelClass = Person

    def create(self, personObject):
        if personObject == None:
            person = Person.objects.create()
        else:
            # Save new
            if personObject.id == 0 or personObject.id == None:
                
                person = Person.objects.create(
                    firstname = personObject.firstname,
                    lastname = personObject.lastname, 
                    middlename = personObject.middlename, 
                )

            else:
                # update existing
                person = Person.objects.get(pk=personObject.id)
                person.firstname = personObject.firstname
                person.lastname = personObject.lastname
                person.middlename = personObject.middlename

                person.save()

        return self.materialize(person)

    def materialize(self, personModel):

        personEntity = PersonEntity(
            firstname=personModel.firstname,
            lastname=personModel.lastname,
            middlename=personModel.middlename,
        )

        personEntity.id=personModel.id
        return personEntity

class CustomerModelManager(ModelManager, Materializer):
    ModelClass = Customer

    def create(self, customerObject):
        if customerObject == None:
            customer = Customer.objects.create()
        else:
            contact_persons = [ Person.objects.get(pk=person.id) for person in customerObject.contact_persons ] 

            try:
                phonenumbers = ', '.join(customerObject.get_phonenumbers()) if customerObject.get_phonenumbers() != None else None
            except:
                phonenumbers = None

            # Save new
            if customerObject.id == 0 or customerObject.id == None:
                customer = Customer.objects.create(
                    name = customerObject.name,
                    date = customerObject.date, 
                    email = customerObject.get_email(), 
                    address = customerObject.get_address(), 
                    phonenumber = phonenumbers, 
                )

                customer.contact_persons.set(contact_persons) if customer.contact_persons != None else None
            else:
                # update existing
                customer = Customer.objects.get(pk=customerObject.id)
                customer.name = customerObject.name
                customer.date = customerObject.date
                customer.email = customerObject.get_email()
                customer.address = customerObject.get_address()
                customer.phonenumber = phonenumbers

                customer.contact_persons.set(contact_persons) if customer.contact_persons != None else None

                customer.save()

        return self.materialize(customer)

    def materialize(self, customerModel):

        customerEntity = CustomerEntity(
            name = customerModel.name,
            email = customerModel.email, 
            phonenumber = customerModel.phonenumber, 
            address = customerModel.address, 
            date = customerModel.date, 
        )

        customerEntity.id=customerModel.id
        
        customerEntity.contact_persons=[{
                'id': contactperson.id,
                'firstname': contactperson.firstname,
                'middlename': contactperson.middlename,
                'lastname': contactperson.lastname,
            } for contactperson in customerModel.contact_persons.all()] if customerModel.contact_persons != None else None

        return customerEntity

class UnitModelManager(ModelManager, Materializer):
    ModelClass = Unit

    def create(self, unitObject):
        if unitObject == None:
            unit = Unit.objects.create()
        else:
            # Save new
            if unitObject.id == 0 or unitObject.id == None:
                unit = Unit.objects.create(
                    shortDesc = unitObject.shortDesc,
                    longDesc = unitObject.longDesc, 
                    active = unitObject.active, 
                )
            else:
                # update existing
                print('shortDesc: ', unitObject.shortDesc)
                unit = Unit.objects.get(pk=unitObject.id)
                unit.shortDesc = unitObject.shortDesc
                unit.longDesc = unitObject.longDesc
                unit.active = unitObject.active
                unit.save()

        return self.materialize(unit)

    def materialize(self, unitModel):

        unitEntity = UnitEntity(
            shortDesc = unitModel.shortDesc,
            longDesc = unitModel.longDesc, 
            active = unitModel.active, 
        )

        unitEntity.id=unitModel.id
        return unitEntity

class PriceModelManager(ModelManager, Materializer):
    ModelClass = Price

    def create(self, priceObject):
        if priceObject == None:
            price = Price.objects.create()
        else:
            # Save new

            if priceObject.id == 0 or priceObject.id == None:
                price = Price.objects.create(
                    fromDate = priceObject.fromDate,
                    toDate = priceObject.toDate, 
                    amount = priceObject.amount, 
                    currency = priceObject.currency, 
                    active = priceObject.active, 
                    product = Product.objects.get(pk=priceObject.product.id) if priceObject.product != None else None
                )
            else:
                # update existing
                price = Price.objects.get(pk=priceObject.id)
                price.fromDate = priceObject.fromDate
                price.toDate = priceObject.toDate
                price.amount = priceObject.amount
                price.currency = priceObject.currency
                price.active = priceObject.active 

                price.product = Product.objects.get(pk=priceObject.product.id) if priceObject.product != None else None

                price.save()

        return self.materialize(price)

    def materialize(self, priceModel):

        priceEntity = PriceEntity(
            fromDate = priceModel.fromDate,
            toDate = priceModel.toDate, 
            amount = priceModel.amount, 
            currency = priceModel.currency,
            active = priceModel.active, 
        )

        priceEntity.id=priceModel.id

        return priceEntity

class UserModelManager(ModelManager, Materializer):
    ModelClass = User

    def create(self, userObject):
        if userObject == None:
            user = User.objects.create()
        else:
            authorizations = [ Authorization.objects.get(pk=auth.id) for auth in userObject.authorizations ] if userObject.authorizations != None else None
            groups = [ Group.objects.get(pk=group.id) for group in userObject.groups ] if userObject.groups != None else None
        
            person = Person.objects.create(
                firstname = userObject.person.firstname,
                lastname = userObject.person.lastname, 
                middlename = userObject.person.middlename, 
            )

            # Save new
            if userObject.id == 0 or userObject.id == None:
                
                user = User.objects.create(
                    person = person if person != None else None,
                    username = userObject.username,
                    password = userObject.password, 
                    email = userObject.email, 
                    phonenumber = userObject.phonenumber, 
                    isAuthenticated = userObject.isAuthenticated, 
                )

                user.authorizations.set(authorizations)
                user.groups.set(groups)
                user.active = False
                
            else:
                # update existing
                user = User.objects.get(pk=userObject.id)
                user.person = person if person != None else None
                user.username = userObject.username
                user.password = userObject.password
                user.email = userObject.email
                user.phonenumber = userObject.phonenumber
                user.isAuthenticated = userObject.isAuthenticated

                user.authorizations.set(authorizations)
                user.groups.set(groups)
                user.active = userObject._active

                user.save()

        return self.materialize(user)

    def materialize(self, userModel):

        userEntity = UserEntity(
            firstname = userModel.person.firstname if userModel.person != None else None, 
            lastname = userModel.person.lastname if userModel.person != None else None, 
            username = userModel.username,
            password = userModel.password, 
            email = userModel.email, 
            phonenumber = userModel.phonenumber, 
        )

        userEntity.isAuthenticated = userModel.isAuthenticated

        userEntity.authorizations=[{
                'id': authorization.id,
                'description': authorization.description,
                'model': authorization.model,
                'create': authorization.can_create,
                'change': authorization.can_change,
                'view': authorization.can_view,
                'delete': authorization.can_delete,
            } for authorization in userModel.authorizations.all()] if userModel.authorizations != None else None

        userEntity.groups=[{
                'id': group.id,
                'description': group.description,
                'details': group.details,
                'authorizations': [{
                    'id': authorization.id,
                    'description': authorization.description,
                    'model': authorization.model,
                    'create': authorization.can_create,
                    'change': authorization.can_change,
                    'view': authorization.can_view,
                    'delete': authorization.can_delete,
                } for authorization in group.authorizations.all()] if group.authorizations != None else None
            } for group in userModel.groups.all()] if userModel.groups != None else None
 
        userEntity.id=userModel.id

        return userEntity

class ProductModelManager(ModelManager, Materializer):
    ModelClass = Product

    def create(self, productObject):
        if productObject == None:
            product = Product.objects.create()
        else:

            units = [ Unit.objects.get(pk=unit.id) for unit in productObject.units ] if productObject.units != None else None

            # Save new
            if productObject.id == 0 or productObject.id == None:  
                product = Product.objects.create(
                    name = productObject.name,
                    group = productObject.group,
                    title = productObject.name,
                    price = productObject.price,
                    date = productObject.date,
                )

                product.units.set(units)

                # create prices
                if productObject.prices != None:
                    for price in productObject.prices:
                        Price.objects.create(
                            fromDate = price.fromDate,
                            toDate = price.toDate, 
                            amount = price.amount, 
                            currency = price.currency, 
                            active = price.active, 
                            product = Product.objects.get(pk=product.id) if product != None else None
                        ) 
                
            else:
                # update existing
                product = Product.objects.get(pk=productObject.id)

                product.name = productObject.name
                product.group = productObject.group
                product.title = productObject.name
                product.price = productObject.price
                product.date = productObject.date
            
                product.units.set(units)

                # create prices
                if productObject.prices != None:
                    for price in productObject.prices:
                        Price.objects.create(
                            fromDate = price.fromDate,
                            toDate = price.toDate, 
                            amount = price.amount, 
                            currency = price.currency, 
                            active = price.active, 
                            product = Product.objects.get(pk=product.id) if product != None else None
                        ) 

                product.save()

        return self.materialize(product)

    def materialize(self, productModel):

        productEntity = ProductEntity(
            name = productModel.name,
            price = productModel.price,
            date = productModel.date,
        )

        productEntity.units=[
            {
                'id': unit.id,
                'shortDesc': unit.shortDesc,
                'longDesc': unit.longDesc,
            } for unit in productModel.units.all()] if productModel.units != None else None

        if productModel.product_prices != None:
            for price in productModel.product_prices.all():
                productEntity.add_price(
                    amount = price.amount,
                    fromDate = price.fromDate,
                    toDate = price.toDate,
                    currency = price.currency,
                    active = price.active,
                )

        productEntity.id=productModel.id

        return productEntity

class SaleModelManager(ModelManager, Materializer):
    ModelClass = Sale

    def create(self, saleObject):
        if saleObject == None:
            sale = Sale.objects.create()
        else:

            # Save new
            if saleObject.id == 0 or saleObject.id == None:  
                sale = Sale.objects.create(
                    product = Product.objects.get(pk=saleObject.customer.id) if saleObject.customer != None else None,
                    quantity = saleObject.quantity,
                    price = saleObject.price,
                    currency = saleObject.currency,
                    date = saleObject.date,
                    customer = Customer.objects.get(pk=saleObject.customer.id) if saleObject.customer != None else None,
                    creator = User.objects.get(pk=saleObject.creator.id) if saleObject.creator != None else None,
                    lastSaleTime = saleObject.lastSaleTime,
                )

            else:
                # update existing
                sale = Sale.objects.get(pk=saleObject.id)

                sale.product = Product.objects.get(pk=saleObject.customer.id) if saleObject.customer != None else None
                sale.quantity = saleObject.quantity
                sale.price = saleObject.price
                sale.currency = saleObject.currency
                sale.price = saleObject.price
                sale.date = saleObject.date
                sale.customer = Customer.objects.get(pk=saleObject.customer.id) if saleObject.customer != None else None
                sale.creator = User.objects.get(pk=saleObject.creator.id) if saleObject.creator != None else None
                sale.lastSaleTime = saleObject.lastSaleTime

                sale.save()

        return self.materialize(sale)

    def materialize(self, saleModel):

        saleEntity = SaleEntity(
            product = Product.objects.get(pk=saleModel.product.id) if saleModel.product != None else None,
            quantity = saleModel.quantity,
            price = saleModel.price,
            currency = saleModel.currency,
            date = saleModel.date,
            customer = Customer.objects.get(pk=saleModel.customer.id) if saleModel.customer != None else None,
            creator = User.objects.get(pk=saleModel.creator.id) if saleModel.creator != None else None,     
        )

        saleEntity.lastSaleTime = saleModel.lastSaleTime

        saleEntity.id=saleModel.id

        return saleEntity

class ProductionBatchModelManager(ModelManager, Materializer):
    ModelClass = ProductionBatch

    def create(self, productionBatchObject):
        if productionBatchObject == None:
            productionBatch = ProductionBatch.objects.create()
        else:

            products = [ Product.objects.get(pk=product.id) for product in productionBatchObject.products ]

            # Save new
            if productionBatchObject.id == 0 or productionBatchObject.id == None:  
                productionBatch = ProductionBatch.objects.create(
                    productType=productionBatchObject.productType, 
                    flourQuantity=productionBatchObject.flourQuantity, 
                    date=productionBatchObject.date, 
                    startTime=productionBatchObject.startTime, 
                    baker=productionBatchObject.baker,
                )

                productionBatch.endTime = productionBatchObject.endTime
                productionBatch.supervisor = productionBatchObject.supervisor
                productionBatch.assistants = ','.join(productionBatchObject.assistants) if productionBatchObject.assistants != None else None
                productionBatch.problems = ','.join(productionBatchObject.problems) if productionBatchObject.problems != None else None

                productionBatch.products.set(products)

            else:
                # update existing
                productionBatch = ProductionBatch.objects.get(pk=productionBatchObject.id)

                productionBatch.productType=productionBatchObject.productType
                productionBatch.flourQuantity=productionBatchObject.flourQuantity
                productionBatch.date=productionBatchObject.date
                productionBatch.startTime=productionBatchObject.startTime
                productionBatch.baker=productionBatchObject.baker

                productionBatch.endTime = productionBatchObject.endTime
                productionBatch.supervisor = productionBatchObject.supervisor
                productionBatch.assistants = ','.join(productionBatchObject.assistants) if productionBatchObject.assistants != None else None
                productionBatch.problems = ','.join(productionBatchObject.problems) if productionBatchObject.problems != None else None

                productionBatch.products.set(products)

                productionBatch.save()

        return self.materialize(productionBatch)

    def materialize(self, productionBatchModel):

        productionBatchEntity = ProductionBatchEntity(
            productType=productionBatchModel.productType, 
            flourQuantity=productionBatchModel.flourQuantity, 
            date=productionBatchModel.date, 
            startTime=productionBatchModel.startTime, 
            baker=productionBatchModel.baker,        
        )

        productionBatchEntity.endTime = productionBatchModel.endTime
        productionBatchEntity.supervisor = productionBatchModel.supervisor
        productionBatchEntity.assistants = productionBatchModel.assistants.split(',') if productionBatchModel.assistants != None else None
        productionBatchEntity.problems = productionBatchModel.problems.split(',') if productionBatchModel.problems != None else None
        
        productModelManager = ProductModelManager()
        productionBatchEntity.products = [
                productModelManager.materialize(product) for product in productionBatchModel.products.all()
            ] if productionBatchModel.products.all() != None else None

        productionBatchEntity.id=productionBatchModel.id

        return productionBatchEntity

class DjangoDataBaseManager(DatabaseManagerInterface):
    saleModelManager = SaleModelManager()
    authorizationModelManager = AuthorizationModelManager()
    groupModelManager = GroupModelManager()
    personModelManager = PersonModelManager()
    customerModelManager = CustomerModelManager()
    unitModelManager = UnitModelManager()
    priceModelManager = PriceModelManager()
    userModelManager = UserModelManager()
    productModelManager = ProductModelManager()
    productionBatchModelManager = ProductionBatchModelManager()
    
    models = {
                'Sale': saleModelManager,
                'Product': productModelManager, 
                'Customer': customerModelManager, 
                'User': userModelManager, 
                'Group': groupModelManager, 
                'Authorization': authorizationModelManager,
                'Person': personModelManager,
                'Price': priceModelManager,
                'Unit': unitModelManager,
                'ProductionBatch': productionBatchModelManager
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
        model = self.models[modelname]
        items = []  

        try:
            for id in ids:
                items.append(self.get(databasename, modelname, id))
        except AttributeError:
            return None
        else:
            return items

    def get_day_items(self, databasename, modelname, date):
        model = self.models[modelname]
        items = []

        ids = model.get_ids()

        for id in ids:
            if model.get(id).date == date:
                items.append(model.get(id))

        return items
    
    def get_day_item(self, databasename, modelname, date, id):
        model = self.models[modelname]

        ids = model.get_ids()

        if id in ids:
            item = model.get(id)
            if item.date == date:
                return item
            else:
                print('Item is not for date!')
                return None
        else:
            print('Item not in database!')
            return None

    def get_all(self, databasename, modelname):
        model = self.models[modelname]
        return model.get_all()



# class Database():
#     name = ''productionBatchModel
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
        
