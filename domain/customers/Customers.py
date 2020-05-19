from .Party import Party, Person

class Customer(Party):
    contact_persons = []
    def __init__(self, name, id=None, address=None, email=None, phonenumber=None, date=None):
        self.id = id
        self.name = name
        self.title = name
        self.date = date
        self.set_address(address)
        self.set_email(email)
        self.add_phonenumber(phonenumber)

    def add_contact_person(self, firstname, lastname, phonenumber, id=None, email=None, address=None, website=None):
        person = Person(
            firstname,
            lastname,
            phonenumber=phonenumber, 
            id=id,
            email=email, 
            address=address,
            website=website
            )
        self.contact_persons.append(person)
