import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import coffeeapp
import coffee_db_alchemy
from common import utils
import json
import unittest
import test_helpers as helpers

class CoffeeAddictApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        coffee_db_alchemy.init_db() 

    @classmethod
    def tearDownClass(cls):
        coffee_db_alchemy.delete_db()

    def setUp(self):
        coffeeapp.app.config['TESTING'] = True
        self.app = coffeeapp.app.test_client()
        self.aspiring_data = { "card_id" : "1234567890" , 
                               "api_key" : utils.api_key }

        r = helpers.create_coffee_machine(self.app)

        machine_dict = json.loads(r)
        self.post_data = { "short_pin" : "",
                           "name" : "john",
                           "email" : "john.doe@siemens.com",
                           "machine_id" : machine_dict["machine_id"] }

    def tearDown(self):
        pass

    ### Helper Functions ###

    def create_aspiring_addict(self):
        res = self.app.post(coffeeapp.aspiring_coffee_addict_api_path, data=self.aspiring_data)
        assert 200 == res.status_code
        return res.data

    ### Argument Tests ###

    def test_missing_args(self):
        res = self.app.post(coffeeapp.coffee_addict_api_path)
        assert 400 == res.status_code

    def test_missing_short_pin(self):
        del self.post_data["short_pin"]
        res = self.app.post(coffeeapp.coffee_addict_api_path, data=self.post_data)
        assert 400 == res.status_code
        assert "short_pin" in res.data

    def test_missing_name(self):
        del self.post_data["name"]
        res = self.app.post(coffeeapp.coffee_addict_api_path, data=self.post_data)
        assert 400 == res.status_code
        assert "name" in res.data

    def test_missing_email(self):
        del self.post_data["email"]
        res = self.app.post(coffeeapp.coffee_addict_api_path, data=self.post_data)
        assert 400 == res.status_code
        assert "email" in res.data

    def test_missing_machine_id(self):
        del self.post_data["machine_id"]
        res = self.app.post(coffeeapp.coffee_addict_api_path, data=self.post_data)
        assert 400 == res.status_code
        assert "machine_id" in res.data

    def test_wrong_short_pin(self):
        self.post_data["short_pin"] = "1234"
        res = self.app.post(coffeeapp.coffee_addict_api_path, data=self.post_data)
        assert 404 == res.status_code

    def test_invalid_email(self):
        data = json.loads(self.create_aspiring_addict())
        assert "short_pin" in data
        self.post_data["short_pin"] = data["short_pin"] 
        self.post_data["email"] = "john.doe@flamingo.ru"
        res = self.app.post(coffeeapp.coffee_addict_api_path, data=self.post_data)
        # we excpect this to be an unprocessable entity
        assert 422 == res.status_code

if __name__ == '__main__':
    unittest.main()
