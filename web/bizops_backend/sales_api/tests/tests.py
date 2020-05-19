from django.test import TestCase, Client


# Create your tests here.
class JwtAuthenticationTestCase(TestCase):
    def setup(self):
        pass

    # def test_create_token(self):
    #     """Valid tokens will not  be None """
    #     c = Client()
    #     response = c.get('/bizops/auth/', {'username':'joy', 'password':'allow'})
    #     print ('in tests token: ' + str(response.content))
    #     self.assertFalse(response.content == None)

    def test_get_user(self):
        c = Client(HTTP_AUTHORIZATION='Bearer ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpveSIsInBhc3N3b3JkIjoiYWxsb3cifQ.UsDBtLZ5t-IdbCrRIPO9M4d8Clh9cmL9W8thipAg3YQ')
        response = c.get('/bizops/users/', {'username':'joy'})
        print (response.content)
    
    def test_login(self):
        c = Client()
        response = c.get('/bizops/login/', {'username':'joy', 'password':'allow'})
        print ('in tests login: ' + str(response.content))

