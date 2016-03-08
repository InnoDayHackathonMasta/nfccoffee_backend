import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import coffeeapp
import coffee_db_alchemy
from common import utils
import unittest

class AspiringcCoffeeAddictApiTestCase(unittest.TestCase):

    def setUp(self):
        coffee_db_alchemy.init_db() 
        coffeeapp.application.config['TESTING'] = True
        self.app = coffeeapp.application.test_client()

    def tearDown(self):
        coffee_db_alchemy.delete_db()

    def test_missing_args(self):
        res = self.app.post(coffeeapp.aspiring_coffee_addict_api_path)
        assert 400 == res.status_code

    def test_missing_card_id(self):
        data = { "api_key" : "DEADBEEFABC123" }
        res = self.app.post(coffeeapp.aspiring_coffee_addict_api_path, data=data)
        assert 400 == res.status_code
        assert "card_id" in res.data

    def test_missing_api_key(self):
        data = { "card_id" : "1234567890" }
        res = self.app.post(coffeeapp.aspiring_coffee_addict_api_path, data=data)
        assert 400 == res.status_code
        assert "api_key" in res.data

    def test_wrong_api_key(self):
        """
        we should get a 401 if a wrong api_key is supplied 
        """
        data = { "card_id" : "1234567890" , "api_key" : "DEADBEEFABC123" }
        res = self.app.post(coffeeapp.aspiring_coffee_addict_api_path, data=data)
        assert 401 == res.status_code

    def test_successful_creation(self):
        data = { "card_id" : "1234567890" , "api_key" : utils.api_key }
        res = self.app.post(coffeeapp.aspiring_coffee_addict_api_path, data=data)
        assert 200 == res.status_code
        assert "short_pin" in res.data

    def test_conflicting_card_ids(self):
        data = { "card_id" : "1234567890" , "api_key" : utils.api_key }
        res = self.app.post(coffeeapp.aspiring_coffee_addict_api_path, data=data)
        assert 200 == res.status_code
        data = { "card_id" : "1234567890" , "api_key" : utils.api_key }
        res = self.app.post(coffeeapp.aspiring_coffee_addict_api_path, data=data)
        assert 409 == res.status_code

if __name__ == '__main__':
    unittest.main()
