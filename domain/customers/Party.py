# a class for ContactInformation 
class ContactInformation():
    address = None
    website = None
    email = None
    phonenumbers = []

    def __init__(self, address=None, website=None, email=None, phonenumbers=[]):
        self.address=address
        self.website=website
        self.email=email
        self.phonenumbers=phonenumbers

# a super class of parties
class Party:
    id=None
    name=None
    date=None
    _contactinformation = ContactInformation()

    def set_address(self, address):
        self._contactinformation.address = address
    
    def set_email(self, email):
        self._contactinformation.email = email

    def set_website(self, website):
        self._contactinformation.website = website

    def set_phonenumbers(self, phonenumbers):
        self._contactinformation.phonenumbers = phonenumbers

    def add_phonenumber(self, phonenumber):
        self._contactinformation.phonenumbers.append(phonenumber)

    def get_address(self):
        return self._contactinformation.address

    def get_email(self):
        return self._contactinformation.email
    
    def get_website(self):
        return self._contactinformation.website

    def get_phonenumbers(self):
        return self._contactinformation.phonenumbers

    def get_name(self):
        if self.name != None:
            return self.name

    def __repr__(self):
        if self.id != None and self._contactinformation.address != None:
            return str(self.id) + ' from ' + self._contactinformation.address
        else:
            return "Address Empty"

# a class for Persons 
class Person(Party):
    firstname=''
    lastname=''
    middlename=''
    def __init__(self, firstname, lastname, middlename=None, id=None, address=None, phonenumber=None, email=None, website=None):
        if firstname != None and lastname != None:
            self.firstname = firstname
            self.lastname = lastname
            self.middlename = middlename
            self.id=id
            self.set_address(address)
            self.set_email(email)
            self.add_phonenumber(phonenumber)
            # print('firstname is '+ firstname)
            # print('lastname is '+ lastname)
        #Party.__init__(self, name, id, address, phonenumber, email)
    
    # def set_email(self, email):
    #     Party.set_email(email)

    def get_name(self):
        return self.firstname + ' ' + self.lastname

# if __name__ == '__main__':
#     party = Party("Party Name", 1000, "Party Address", "Phone Number", "party@email.com")
#     print(party)