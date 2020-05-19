from django.test import TestCase, Client


# Create your tests here.
class UnitsTestCase(TestCase):
    def setup(self):
        pass

    def test_post_units(self):
        c = Client(HTTP_AUTHORIZATION='Bearer ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpveSIsInBhc3N3b3JkIjoiYWxsb3cifQ.UsDBtLZ5t-IdbCrRIPO9M4d8Clh9cmL9W8thipAg3YQ')
        response = c.post('/bizops/units/', 
            {"short":"ns2", "long":"new Short2", "active": "false"},
            content_type="application/json"
            )
        print (response.content)
        for key in response.json():
            print (key +  " " + str(response.json()[key])) 

