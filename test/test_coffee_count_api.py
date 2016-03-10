import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import coffeeapp
import coffee_db_alchemy
from common import utils
import unittest
import json
import test_helpers as helpers

class CoffeeCountApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        coffee_db_alchemy.init_db() 

    @classmethod
    def tearDownClass(cls):
        coffee_db_alchemy.delete_db()

    def setUp(self):
        coffeeapp.application.config['TESTING'] = True
        self.app = coffeeapp.application.test_client()
        self.put_data = { "card_id" : "1234567890", 
                          "api_key" : utils.api_key,
                          "machine_id" : "1337", 
                          "new_count" : "42"}

    def tearDown(self):
        pass

    ### Argument Tests ###

    def test_missing_args(self):
        res = self.app.put(coffeeapp.coffee_count_api_path)
        assert 400 == res.status_code

    def test_missing_card_id(self):
        del self.put_data["card_id"]
        res = self.app.put(coffeeapp.coffee_count_api_path, data=self.put_data)
        assert 400 == res.status_code
        assert "card_id" in res.data

    def test_missing_api_key(self):
        del self.put_data["api_key"]
        res = self.app.put(coffeeapp.coffee_count_api_path, data=self.put_data)
        assert 400 == res.status_code
        assert "api_key" in res.data

    def test_missing_machine_id(self):
        del self.put_data["machine_id"]
        res = self.app.put(coffeeapp.coffee_count_api_path, data=self.put_data)
        assert 400 == res.status_code
        assert "machine_id" in res.data

    def test_wrong_api_key(self):
        self.put_data["api_key"] = "THIS_IS_NOT_THE_KEY"
        res = self.app.put(coffeeapp.coffee_count_api_path, data=self.put_data)
        assert 401 == res.status_code

    def test_new_card_id(self):
        """
        an unknown card_id was part of the request, we should create an
        AspiringAddict
        """
        self.put_data["card_id"] = "DEADBEEF"
        res = self.app.put(coffeeapp.coffee_count_api_path, data=self.put_data)
        assert 200 == res.status_code
        res_json = json.loads(res.data)
        assert res_json.has_key("known")
        assert res_json["known"] == False
        assert res_json.has_key("short_pin")
        assert res_json.has_key("url")

    def test_card_id_present_but_no_signup_yet(self):
        """
        we have seen this card_id before
        send the same response again
        """
        machine_id = helpers.create_coffee_machine(self.app, \
                        "Senseo Floor 5", 0.35, "EUR" )

        card_id = helpers.gen_card_id() 

        data = { "card_id" : card_id, 
                  "api_key" : utils.api_key,
                  "machine_id" : machine_id }

        # make backend aware of card_id
        res = self.app.put(coffeeapp.coffee_count_api_path, data=data)
        assert 200 == res.status_code
        res_json = json.loads(res.data)
        assert res_json.has_key("known")
        assert res_json["known"] == False
        assert res_json.has_key("short_pin")
        assert res_json.has_key("url")

        res = self.app.put(coffeeapp.coffee_count_api_path, data=data)
        # now it should respond with the same data
        assert 200 == res.status_code
        res_json = json.loads(res.data)
        assert res_json.has_key("known")
        assert res_json["known"] == False
        assert res_json.has_key("short_pin")
        assert res_json.has_key("url")
        
    def test_card_id_present_and_signup_complete(self):
        """
        card_id is known, take a COFFEE!!!
        """
        machine_id = helpers.create_coffee_machine(self.app, \
                        "Senseo Floor 5", 0.35, "EUR" )
        card_id = helpers.create_coffee_addict(self.app, \
                        "john", "john@doe.com", machine_id)

        res = self.app.put(coffeeapp.coffee_count_api_path, data={
            "machine_id" : machine_id,
            "card_id" : card_id,
            "api_key" : utils.api_key})

        assert res.status_code == 200
        res_json = json.loads(res.data)
        assert res_json.has_key("known")
        assert res_json["known"] == True
        assert res_json.has_key("name")
        assert res_json.has_key("count")

    def test_two_addicts_signup_and_count(self):
        """
        """
        machine_id = helpers.create_coffee_machine(self.app, \
                        "Senseo Floor 5", 0.35, "EUR" )
        card_id_one = helpers.create_coffee_addict(self.app, \
                        "john", "john@doe.com", machine_id)

        card_id_two = helpers.create_coffee_addict(self.app, \
                        "alice", "alice@doe.com", machine_id)

        res = self.app.put(coffeeapp.coffee_count_api_path, data={
            "machine_id" : machine_id,
            "card_id" : card_id_one,
            "api_key" : utils.api_key})

        assert res.status_code == 200
        res_json = json.loads(res.data)
        assert res_json.has_key("known")
        assert res_json["known"] == True
        assert res_json.has_key("name")
        assert res_json.has_key("count")

        res = self.app.put(coffeeapp.coffee_count_api_path, data={
            "machine_id" : machine_id,
            "card_id" : card_id_two,
            "api_key" : utils.api_key})

        assert res.status_code == 200
        res_json = json.loads(res.data)
        assert res_json.has_key("known")
        assert res_json["known"] == True
        assert res_json.has_key("name")
        assert res_json.has_key("count")

if __name__ == '__main__':
    unittest.main()
