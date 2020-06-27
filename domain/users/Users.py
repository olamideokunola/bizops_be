from domain.customers.Party import Person

class Parent:

    def __get_members(self, members):
        return list(members.values())

    def add_member(self, member, members):
        if not member.id in members:
            members[member.id] = member

    def get_member(self, id, members):
        if id in members:
            return members[id]

    def update_member(self, member, members):
        if not member.id in self.members:
            members[member.id] = member

    def remove_member(self, id, members):
        if id in members:
            members.pop(id)

    def clear_members(self, members):
        members.clear()

class AuthorizationParent(Parent):
    # __get_authorizations(self):
    #    return list(self.authorizations.values())

   # authorizations = property(fget=__get_authorizations)
    
    def add_authorization(self, authorization):
        self.add_member(authorization, self.authorizations)

    def get_authorization(self, id):
        return self.get_member(id, self.authorizations)

    def update_authorization(self, authorization):
        self.update_member(authorization, self.authorizations)
        
    def remove_authorization(self, id):
        self.remove_member(id, self.authorizations)

    def clear_authorizations(self):
        self.clear_members(self.authorizations)

class GroupParent(Parent):

    # __groups = {}
    
    # def __get_groups(self):
    #     return list(self.__groups.values())

    # groups = property(fget=__get_groups)
    
    def add_group(self, group):
        self.add_member(group, self.groups)

    def get_group(self, id):
        return self.get_member(id, self.groups)

    def update_group(self, group):
        self.update_member(group, self.groups)
        
    def remove_group(self, id):
        self.remove_member(id, self.groups)

    def clear_groups(self):
        self.clear_members(self.groups)

class User(AuthorizationParent, GroupParent):
    username=None
    password=None
    person=None
    email=None
    phonenumber=None
    isAuthenticated = False
    id=None
    authorizations = {}
    groups = {}
    _active = False

    def __init__(self, firstname, lastname, username=None, password=None, email=None, phonenumber=None):
        self.person = Person(firstname=firstname,lastname=lastname)
        # self.firstname = firstname
        # self.lastname = lastname
        self.username = username
        self.password = password
        self.email = email
        self.phonenumber = phonenumber
        self.authorizations = {}
        self.groups = {}

    def get_username(self):
        return self.username

    def set_username(self, value):
        self.username = value

    def get_password(self):
        return self.password

    def get_firstname(self):
        return self.person.firstname

    def get_lastname(self):
        return self.person.lastname

    def get_email(self):
        return self.person.get_email()

    def get_active(self):
        return self._active

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    #id = property(fget=get_username, fset=set_username)

class Group(AuthorizationParent):
    id=None
    description=''
    details=''
    authorizations = []
    
    def __init__(self, description, details):
        self.description = description
        self.details = details
        self.authorizations = []

class Authorization:
    id=None
    description=''
    model=''
    create=False
    edit=False
    view=False
    delete=False

    def __init__(self, model, description, id=None, create=False, edit=False, view=False, delete=False):
        self.id = id
        self.model = model
        self.description = description
        self.create = create
        self.edit = edit
        self.view = view
        self.delete = delete

    def clear(self):
        self.create=False
        self.edit=False
        self.view=False
        self.delete=False

