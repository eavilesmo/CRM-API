# Imports
import app
import unittest
import datetime

# Variables
dict_create_correct = {"name": "example", "surname": "testing", 
                       "email":"email@email.com", "birthdate":"1997/11/22"}
dict_create_fail = {"name": "example", "surname": "testing", 
                    "email":"email", "birthdate":"1997/11/22"}

# Classes
class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.app.application.config['WTF_CSRF_ENABLED'] = False

    # Testing if flask is initialized correctly
    def test_01_app(self):
        response = self.app.get("/", content_type="html/text")
        self.assertEqual(response.status_code, 200)
    
    # Index Page
    # Testing if the message from the index page is correctly created
    def test_02_index(self):
        response = self.app.get("/", content_type="html/text")
        self.assertTrue(b"Welcome to the CRM API!" in response.data)
    
    # Home Page
    # Testing if the options from the home page are correctly created
    def test_03_home(self):
        response = self.app.get("/home", content_type="html/text")
        self.assertTrue(b"Get one customer" in response.data)
    
    # Create Page
    # Testing if the options from the create-customer page are correctly created
    def test_04_create_customer_load(self):
        response = self.app.get("/create-customer", content_type="html/text")
        self.assertTrue(b"Customer Creation Form" in response.data)
    
    # Testing create-customer functionality with correct data
    def test_05_create_customer_correctly(self):
        response = self.app.post("/create-customer", 
                                data=dict(custom_name="example", 
                                          custom_surname="testing", 
                                          custom_email="email@email.com", 
                                          custom_birthdate=datetime.date(1997, 11, 22)),
                                          follow_redirects=True)
        self.assertIn(b"The customer was correctly created!", response.data)

    # Testing create-customer functionality with incorrect data
    def test_06_create_customer_incorrectly(self):
        response = self.app.post("/create-customer", 
                                data=dict(custom_name="example", 
                                          custom_surname="testing", 
                                          custom_email="email", 
                                          custom_birthdate=datetime.date(1997, 11, 22)), 
                                          follow_redirects=True)
        self.assertIn(b"Invalid email address.", response.data)

    # Get One Page
    # Testing if the options from the getone-customer page are correctly created
    def test_07_getone_customer(self):
        response = self.app.get("/getone-customer", content_type="html/text")
        self.assertTrue(b"Get One Customer" in response.data)
    
    # Testing getone-customer functionality with correct data
    def test_08_getone_customer_correctly(self):
        response = self.app.post("/getone-customer", data=dict(custom_id=0), 
                                 follow_redirects=True)
        self.assertIn(b"Here are the results for your search!", response.data)

    # Testing getone-customer functionality with incorrect data
    def test_09_getone_customer_incorrectly(self):
        response = self.app.post("/getone-customer", data=dict(custom_id="."), 
                                 follow_redirects=True)
        self.assertIn(b"The ID does not exist in the database.", response.data)

    # Get All Page
    # Testing if the getall-customer page loads correctly with customer data
    def test_10_getall_customer(self):
        response = self.app.get("/getall-customer", content_type="html/text")
        self.assertTrue(b"List of all customers created" in response.data)

    # Update Page
    # Testing if the options from the update-customer page are correctly created
    def test_11_update_customer(self):
        response = self.app.get("/update-customer", content_type="html/text")
        self.assertTrue(b"Customer Update Form" in response.data)
    
    # Testing update-customer functionality with correct data
    def test_12_update_customer_correctly(self):
        response = self.app.post("/update-customer", 
                                 data=dict(custom_id="0", 
                                 custom_name="example_name", 
                                 custom_surname="testing_surname", 
                                 custom_email="email@email.com", 
                                 custom_birthdate=datetime.date(1997, 11, 22)), 
                                 follow_redirects=True)
        self.assertIn(b"The customer was correctly updated!", response.data)
    
    # Testing update-customer functionality with incorrect data
    def test_13_update_customer_incorrectly(self):
        response = self.app.post("/update-customer", 
                                 data=dict(custom_id=".", 
                                 custom_name="example_name", 
                                 custom_surname="testing_surname", 
                                 custom_email="email@email.com", 
                                 custom_birthdate=datetime.date(1997, 11, 22)), 
                                 follow_redirects=True)
        self.assertIn(b"The ID does not exist in the database.", response.data)

    # Delete Page
    # Testing if the options from the delete-customer page are correctly created
    def test_14_delete_customer(self):
        response = self.app.get("/delete-customer", content_type="html/text")
        self.assertTrue(b"Customer Deletion Form" in response.data)
    
    # Testing delete-customer functionality with correct data
    def test_15_delete_customer_correctly(self):
        response = self.app.post("/delete-customer", data=dict(custom_id="0"), 
                                 follow_redirects=True)
        self.assertIn(b"Customer deleted!", response.data)
    
    # Testing delete-customer functionality with incorrect data
    def test_16_delete_customer_incorrectly(self):
        response = self.app.post("/delete-customer", data=dict(custom_id="."), 
                                 follow_redirects=True)
        self.assertIn(b"The ID does not exist in the database.", response.data)


# Main
if __name__ == "__main__":
    unittest.main()
