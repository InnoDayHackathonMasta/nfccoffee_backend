import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import coffeeapp
import coffee_db_alchemy
from common import utils
import json
import unittest
import test_helpers as helpers

class CoffeeMachineApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        coffee_db_alchemy.init_db() 

    @classmethod
    def tearDownClass(cls):
        coffee_db_alchemy.delete_db()


    def setUp(self):
        coffeeapp.app.config['TESTING'] = True
        self.app = coffeeapp.app.test_client()
        self.post_data = { "name" : "Senseo with <3",
                           "costs_per_unit" : "0.35",
                           "currency" : "EUR", 
                           "api_key" : utils.api_key }

    def tearDown(self):
        pass

    ### Argument Tests ###

    def test_missing_args(self):
        res = self.app.post(coffeeapp.coffee_machine_api_path)
        assert 400 == res.status_code

    def test_missing_name(self):
        del self.post_data["name"]
        res = self.app.post(coffeeapp.coffee_machine_api_path, data=self.post_data)
        assert 400 == res.status_code
        assert "name" in res.data

    def test_missing_costs_per_unit(self):
        del self.post_data["costs_per_unit"]
        res = self.app.post(coffeeapp.coffee_machine_api_path, data=self.post_data)
        assert 400 == res.status_code
        assert "costs_per_unit" in res.data

    def test_missing_currency(self):
        del self.post_data["currency"]
        res = self.app.post(coffeeapp.coffee_machine_api_path, data=self.post_data)
        assert 400 == res.status_code
        assert "currency" in res.data

    def test_missing_api_key(self):
        del self.post_data["api_key"]
        res = self.app.post(coffeeapp.coffee_machine_api_path, data=self.post_data)
        assert 400 == res.status_code
        assert "api_key" in res.data

    ### Creation Tests ###

    def test_create_machine(self):
        ret_data = helpers.create_coffee_machine(self.app)
        assert "machine_id" in ret_data 

if __name__ == '__main__':
    unittest.main()
