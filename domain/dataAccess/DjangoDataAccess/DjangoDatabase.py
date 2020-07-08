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


from sales_api.models import Sale, Price, Product, Authorization, Group, Person, Customer, Unit, User, ProductionBatch, ProductionProduct
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

    def delete_all(self):
        return self.ModelClass.objects.all().delete()[0]

    def get_all(self):
        print('In getall')
        numOfItems = len(self.ModelClass.objects.all())
        if numOfItems > 0:
            print('Items more than 0, number is', numOfItems)
            return [self.materialize(item) for item in self.ModelClass.objects.all() ] 
        else:
            print('No items found!')
            return []

    def get_ids(self):
        print('In getids')
        return [item.id for item in self.ModelClass.objects.all()]


class AuthorizationModelManager(ModelManager, Materializer):
    ModelClass = Authorization

    @staticmethod
    def create_model(authObject):
        if isinstance(authObject, dict):
            print('is dict')
            return Authorization.objects.create(
                        description = authObject['description'],
                        model = authObject['model'],
                        can_create = authObject['create'],
                        can_edit = authObject['edit'],
                        can_view = authObject['view'],
                        can_delete = authObject['delete'],
                    )
        elif isinstance(authObject, AuthorizationEntity):
            return Authorization.objects.create(
                        description = authObject.description,
                        model = authObject.model,
                        can_create = authObject.create,
                        can_edit = authObject.edit,
                        can_view = authObject.view,
                        can_delete = authObject.delete,
                    )
    
    def create(self, authObject):
        if authObject == None:
            auth = Authorization.objects.create()
        else:
            if authObject.id == 0 or authObject.id == None:
                auth = self.create_model(authObject)
            else:
                auth = Authorization.objects.get(pk=authObject.id)
                auth.description = authObject.description
                auth.model = authObject.model
                auth.can_create = authObject.create
                auth.can_edit = authObject.edit
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
            edit=authModel.can_edit,
            view=authModel.can_view,
            delete=authModel.can_delete,
        )

class GroupModelManager(ModelManager, Materializer):
    ModelClass = Group

    @staticmethod
    def create_model(groupObject):
        return Group.objects.create(
                    description = groupObject.description,
                    details = groupObject.details, 
                )

    def create(self, groupObject):
        if groupObject == None:
            group = Group.objects.create()
        else:
            authModelManager = AuthorizationModelManager()
            authorizations = [ authModelManager.create(auth) for auth in groupObject.authorizations ] if groupObject.authorizations != None else None

            print('auths is', len(authorizations))
            # Save new
            if groupObject.id == 0 or groupObject.id == None:
                
                # authorizations = [ Authorization.objects.get(pk=auth.id) for auth in groupObject.authorizations ] 
                
                group = Group.objects.create(
                    description = groupObject.description,
                    details = groupObject.details, 
                )
                group.authorizations.set(authorizations) if authorizations != None else None
            else:
                # update existing
                group = Group.objects.get(pk=groupObject.id)
                group.description = groupObject.description
                group.details = groupObject.details

                # authorizations = [ authModelManager.create(auth) for auth in groupObject.authorizations ] if groupObject.authorizations != None else None
                # authorizations = [ Authorization.objects.get(pk=auth.id) for auth in groupObject.authorizations ] 
                group.authorizations.set(authorizations) if authorizations != None else None

                group.save()

        return self.materialize(group)

    def materialize(self, groupModel):
        # print('materializing group!')
        groupEntity = GroupEntity(
            description=groupModel.description,
            details=groupModel.details,
        )

        # print('Group entity created', groupEntity.description)

        groupEntity.id=groupModel.id
        groupEntity.authorizations=[{
                'id': authorization.id,
                'description': authorization.description,
                'model': authorization.model,
                'create': authorization.can_create,
                'edit': authorization.can_edit,
                'view': authorization.can_view,
                'delete': authorization.can_delete,
            } for authorization in groupModel.authorizations.all()]
        print('group collected')
        return groupEntity

class PersonModelManager(ModelManager, Materializer):
    ModelClass = Person

    @staticmethod
    def create_model(personObject):
        return Person.objects.create(
                    firstname = personObject.firstname,
                    lastname = personObject.lastname, 
                    middlename = personObject.middlename, 
                )

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

        personEntity = self.create_model(personModel)

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

    @staticmethod
    def create_model(priceObject):
        print('In PriceModelManager')
        # print('In PriceModelManager, product id is', priceObject.product.id)
        if isinstance(priceObject, PriceEntity):
            print('is PriceEntity', priceObject.fromDate, priceObject.toDate, priceObject.amount, priceObject.currency, priceObject.active)
            return Price.objects.create(
                        fromDate = priceObject.fromDate if priceObject.fromDate != None else None,
                        toDate = priceObject.toDate if priceObject.toDate != None else None,
                        amount = priceObject.amount if priceObject.amount != None else None,
                        currency = priceObject.currency if priceObject.currency != None else None,
                        active = priceObject.active if priceObject.active != None else None,
                        product = Product.objects.get(pk=priceObject.product.id) if priceObject.product != None else None
                    )
        elif isinstance(priceObject, dict):
            print('is dict', priceObject)
            return Price.objects.create(
                        fromDate = priceObject['date'] if 'date' in  priceObject else None,
                        toDate = priceObject['toDate'] if 'toDate' in  priceObject else None,
                        amount = priceObject['price'] if 'price' in  priceObject else None,
                        currency = priceObject['currency'] if 'currency' in  priceObject else None,
                        active = priceObject['active'] if 'active' in  priceObject else None,
                        product = Product.objects.get(pk=priceObject['product']['id']) if 'product' in  priceObject else None,
                    )

    def create(self, priceObject):
        if priceObject == None:
            price = Price.objects.create()
        else:
            # Save new
            if priceObject.id == 0 or priceObject.id == None:
                price = self.create_model(priceObject)
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
            # create authorizations and group
            print('In UserModelManager create ', userObject.authorizations )
            authorizations = [ AuthorizationModelManager.create_model(auth) for auth in userObject.authorizations ] if userObject.authorizations != None else None
            
            print('In UserModelManager auths prepared ' )
            groups = [ GroupModelManager.create_model(group) for group in userObject.groups ] if userObject.groups != None else None

            print('auths is', len(authorizations))
            print('auth type', type(authorizations[0]))

            # create groups
            # authorizations = [ Authorization.objects.get(pk=auth.id) for auth in userObject.authorizations ] if userObject.authorizations != None else None
            # groups = [ Group.objects.get(pk=group.id) for group in userObject.groups ] if userObject.groups != None else None
        
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

                user.authorizations.set(authorizations) if authorizations != None else None
                user.groups.set(groups) if groups != None else None
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
                'edit': authorization.can_edit,
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
                    'edit': authorization.can_edit,
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
            print('In create 1')
            print('units', type(productObject.units))

            units = None

            if productObject.units != None and len(productObject.units) > 0:
                if isinstance(productObject.units[0], dict):
                    units = [ Unit.objects.get(pk=unit['id']) for unit in productObject.units ] if productObject.units != None else None
                elif isinstance(productObject.units[0], UnitEntity):
                    units = [ Unit.objects.get(pk=unit.id) for unit in productObject.units ] if productObject.units != None else None


            # Save new
            print('In create 2', productObject.group)
            if productObject.id == 0 or productObject.id == None:  
                product = Product.objects.create(
                    name = productObject.name,
                    group = productObject.group,
                    title = productObject.name,
                    date = productObject.date,
                )
                
            else:
                # update existing
                # Get model from db
                print('about to update')
                product = Product.objects.get(pk=productObject.id)
                print('about to update', productObject.date)

                # Update the fields
                product.name = productObject.name if productObject.name != None else None
                product.group = productObject.group if productObject.group != None else None
                product.title = productObject.name if productObject.name != None else None
                product.date = productObject.date if productObject.date != None else None

            
            # Set fields common to new save and update
            # print('In create 2 price amount', productObject.price.fromDate)
            if productObject.price != None:
                price = Price(
                    fromDate = productObject.price.fromDate if productObject.price.fromDate != None else None,
                    toDate = productObject.price.toDate if productObject.price.toDate != None else None,
                    amount = productObject.price.amount if productObject.price.amount != None else None,
                    currency = productObject.price.currency if productObject.price.currency != None else None,
                    active = productObject.price.active if productObject.price.active != None else None,
                )
                print('price created')
                price.save()
                print('price created')
                product.price = price
                product.save()

            product.units.set(units) if units != None else None

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

        return self.materialize(product)

    def materialize(self, productModel):

        # print('price',productModel.price )
        # Set basic fields
        productEntity = ProductEntity(
            name = productModel.name,
            price = productModel.price,
            date = productModel.date,
        )

        # set group
        productEntity.group = productModel.group

        productEntity.units=[]
        productEntity.units=[
            {
                'id': unit.id,
                'shortDesc': unit.shortDesc,
                'longDesc': unit.longDesc,
            } for unit in productModel.units.all()] if productModel.units != None else None

        productEntity.prices=[]
        if productModel.product_prices != None:
            for price in productModel.product_prices.all():
                # print('adding prices')
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
            # print('Sale id', saleObject.id)
            # Save new
            if saleObject.id == 0 or saleObject.id == None:  
                # print('About to save')
                prd = Product.objects.get(pk=saleObject.product.id)
                # print('product is', prd)
                # print('prices is', prd.product_prices.all())
                # print('creator is', saleObject.creator)
                # print('quantity is', saleObject.quantity)
                # print('currency is', saleObject.currency)
                # print('price is', saleObject.price)
                # print('date is', saleObject.date)
                # print('date type is', type(saleObject.date))
                # print('customer is', saleObject.customer)
                # print('lastSaleTime is', saleObject.lastSaleTime)
                # print('1 creator type is', type(saleObject.creator))
                # print('1 creator type is', saleObject.creator)

                if isinstance(saleObject.creator, UserEntity):
                    # print('2 creator type is UserEntity')
                    creator = User.objects.get(pk=saleObject.creator.id) if saleObject.creator != None else None
                elif isinstance(saleObject.creator, dict):
                    # print('2 creator type is dict')
                    creator = User.objects.get(pk=saleObject.creator['id']) if saleObject.creator != None else None

                # print('3 creator type is confirmed as ', type(creator))

                price = None
                # convert price to plain number
                if isinstance(saleObject.price, dict):
                    price = float(saleObject.price['price'])
                if isinstance(saleObject.price, Price):
                    price = saleObject.price.amount

                sale = Sale.objects.create(
                    product = Product.objects.get(pk=saleObject.product.id) if saleObject.product != None else None,
                    quantity = saleObject.quantity,
                    price = price,
                    currency = saleObject.currency,
                    date = saleObject.date,
                    customer = Customer.objects.get(pk=saleObject.customer.id) if saleObject.customer != None else None,
                    creator = creator,
                    lastSaleTime = saleObject.lastSaleTime,
                )

                # print('After sale')

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

        productModelManager = ProductModelManager()
        customerModelManager = CustomerModelManager()
        userModelManager = UserModelManager()

        saleEntity = SaleEntity(
            product = productModelManager.materialize(Product.objects.get(pk=saleModel.product.id)) if saleModel.product != None else None,
            quantity = saleModel.quantity,
            price = saleModel.price,
            currency = saleModel.currency,
            date = saleModel.date,
            customer = customerModelManager.materialize(Customer.objects.get(pk=saleModel.customer.id)) if saleModel.customer != None else None,
            creator = userModelManager.materialize(User.objects.get(pk=saleModel.creator.id)) if saleModel.creator != None else None,     
        )

        # print('In materialize for sale, date is ' + str(saleModel.date))

        saleEntity.lastSaleTime = saleModel.lastSaleTime

        saleEntity.id=saleModel.id

        return saleEntity

class ProductionBatchModelManager(ModelManager, Materializer):
    ModelClass = ProductionBatch

    @staticmethod
    def create(inputParams):
        if inputParams != None:
            id =  inputParams['id'] if 'id' in inputParams else None
            productType =  inputParams['productType'] if 'productType' in inputParams else None
            flourQuantity =  inputParams['flourQuantity'] if 'flourQuantity' in inputParams else None
            date =  inputParams['date'] if 'date' in inputParams else None
            startTime = inputParams['startTime'] if 'startTime' in inputParams else None
            endTime = inputParams['endTime'] if 'endTime' in inputParams else None
            baker =  inputParams['baker'] if 'baker' in inputParams else None
            supervisor =  inputParams['supervisor'] if 'supervisor' in inputParams else None
            assistants = inputParams['assistants'] if 'assistants' in inputParams else None
            problems = inputParams['problems'] if 'problems' in inputParams else None
            products = inputParams['products'] if 'products' in inputParams else []

        # Create an empty object with id
        if inputParams == None or inputParams == {}:
            productionBatch = ProductionBatch.objects.create()
        else:

            # Save new
            if id == 0 or id == None:  

                # create productionBatch
                productionBatch = ProductionBatch(
                    productType=productType,
                    flourQuantity=flourQuantity,
                    date=date,
                    startTime=startTime,
                    endTime=endTime,
                    baker=baker,
                    supervisor=supervisor,
                    assistants=assistants,
                    problems=problems
                )

                productionBatch.save()

                # create production products
                for product in products:
                    product['productionBatchId'] = productionBatch.id
                    ProductionProductModelManager.create(product)

            # update existing
            else:
                # Get productionBatch from DB
                productionBatch = ProductionBatch.objects.get(pk=id)
                
                # update fields
                productionBatch.productType = productType
                productionBatch.flourQuantity = flourQuantity
                productionBatch.date = date
                productionBatch.startTime = startTime
                productionBatch.endTime= endTime
                productionBatch.baker= baker
                productionBatch.supervisor= supervisor
                productionBatch.assistants= assistants
                productionBatch.problems= problems

                productionBatch.save()

                # delete old production products
                productionBatch.productionproduct_set.clear()

                # create new production products
                for product in products:
                    # print('product', product)
                    product['id'] = None
                    product['productionBatchId'] = productionBatch.id
                    ProductionProductModelManager.create(product)

        return ProductionBatchModelManager.materialize(productionBatch)

    @staticmethod
    def materialize(productionBatchModel):
        productionProducts = productionBatchModel.productionproduct_set.all()
        return {
            'id': productionBatchModel.id,
            'productType': productionBatchModel.productType,
            'flourQuantity': productionBatchModel.flourQuantity,
            'date': productionBatchModel.date,
            'startTime': productionBatchModel.startTime,
            'endTime': productionBatchModel.endTime,
            'baker': productionBatchModel.baker,
            'supervisor': productionBatchModel.supervisor,
            'assistants': productionBatchModel.assistants,
            'problems': productionBatchModel.problems,
            'products': [ 
                {
                    "id": productionProduct.id,
                    "name": productionProduct.product.name,
                    "price": productionProduct.product.price.amount,
                    "goodQuantity": productionProduct.goodQuantity,
                    "damagedQuantity": productionProduct.damagedQuantity
                } for productionProduct in productionProducts]
        }

### Class representing production output, associated with production batch and product, takes in a dictionary and returns a dictionary
class ProductionProductModelManager(ModelManager, Materializer):
    ModelClass = ProductionProduct
    
    @staticmethod
    def create(inputParams):
        if inputParams != None:
            id =  inputParams['id'] if 'id' in inputParams else None
            productionBatchId =  inputParams['productionBatchId'] if 'productionBatchId' in inputParams else None
            name =  inputParams['name'] if 'name' in inputParams else None
            price =  inputParams['price'] if 'price' in inputParams else None
            goodQuantity = inputParams['goodQuantity'] if 'goodQuantity' in inputParams else None
            damagedQuantity = inputParams['damagedQuantity'] if 'damagedQuantity' in inputParams else None

            # Get product if available
            product = Product.objects.get(name=name) if name != None else None 

            # Get production batch if available
            productionBatch = ProductionBatch.objects.get(id=productionBatchId) if productionBatchId != None else None  


        # Create an empty object with id if there are no inputParams
        if inputParams == None or inputParams == {}:
            print('No input params')
            productionProduct = ProductionProduct.objects.create()
            print('No input params', productionProduct.id)
        else:

            # Save new
            if id == 0 or id == None:  

                # create productionproduct
                productionProduct = ProductionProduct(
                    productionBatch=productionBatch,
                    product=product,
                    goodQuantity=goodQuantity,
                    damagedQuantity=damagedQuantity
                )

                productionProduct.save()

            # update existing
            else:
                # Get productionBatch from DB
                productionProduct = ProductionProduct.objects.get(pk=id)
                
                # update fields
                productionProduct.goodQuantity = goodQuantity
                productionProduct.damagedQuantity = damagedQuantity

                # update associations
                productionProduct.productionBatch =  productionBatch
                productionProduct.product =  product

                productionProduct.save()

        return ProductionProductModelManager.materialize(productionProduct)
    
    @staticmethod
    def materialize(productionProductModel):
        return {
            'id': productionProductModel.id, 
            'productionBatchId': productionProductModel.productionBatch.id, 
            'name': productionProductModel.product.name, 
            'price': productionProductModel.product.price.amount, 
            'goodQuantity': productionProductModel.goodQuantity,  
            'damagedQuantity': productionProductModel.damagedQuantity
        }

    

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
    productionProductModelManager = ProductionProductModelManager()
    
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
                'ProductionBatch': productionBatchModelManager,
                'ProductionProduct': productionProductModelManager
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

    def delete_all(self, databasename, modelname):
        model = self.models[modelname]
        return model.delete_all()

    def create_new_id(self, databasename, modelname):
        print('In create_new_id')

        item = self.save(databasename, modelname, None)
        if  isinstance(item, dict):
            return item['id']
        else:
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
            return []
        except TypeError:
            return []
        else:
            return items

    def get_day_items(self, databasename, modelname, date):
        model = self.models[modelname]
        items = []

        ids = model.get_ids()

        print('about to get day items')
        # print('about to get day items, date is', date)
        # print('about to get day items, ids are', ids)

        for id in ids:
            # print('date', model.get(id)['date'])
            if isinstance(model.get(id), dict):

                if str(model.get(id)['date']) == str(date):
                    items.append(model.get(id))
            else:
                if str(model.get(id).date) == str(date):
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
