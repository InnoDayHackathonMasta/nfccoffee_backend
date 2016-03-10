import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import coffeeapp
import coffee_db_alchemy
from common import utils
import json
import unittest
import string

# inited at end of script
helper_global_card_id = None

def init():
    global helper_global_card_id
    helper_global_card_id = gen_card_id() 

def gen_card_id():
    """
    generator yielding unique card_ids
    """
    card_ids = []
    while True:
        card_id = ''.join(random.SystemRandom().choice( \
                string.ascii_uppercase + \
                string.digits) for _ in range(8))

        if not card_id in card_ids:
            card_ids.append(card_id)
            yield card_id

def create_coffee_machine(app, name, costs_per_unit, currency):
    """
    creates a CoffeMachine

    return machine_id
    """

    data = { "name" : name,
               "costs_per_unit" : costs_per_unit,
               "currency" : currency, 
               "api_key" :  utils.api_key }

    res = app.post(coffeeapp.coffee_machine_api_path, \
            data=data)

    assert 200 == res.status_code

    return json.loads(res.data)["machine_id"]

def create_aspiring_addict_via_coffee_count(app, card_id, machine_id):
    data = { "card_id" : card_id, 
              "api_key" : utils.api_key,
              "machine_id" : machine_id }

    res = app.put(coffeeapp.coffee_count_api_path, data=data)

    assert 200 == res.status_code
    return res.data

def create_coffee_addict(app, name, email, machine_id):
        """
        creates a 'functional' CoffeeAddict 
        which can be used for further testing

        return card_id (String)
        """

        card_id = gen_card_id()
        res_aspiring_api = create_aspiring_addict_via_coffee_count(app, \
                card_id, machine_id)

        json_aspiring = json.loads(res_aspiring_api)

        post_data = { "short_pin" : json_aspiring["short_pin"],
                       "name" : name,
                       "email" : email,
                       "machine_id" : machine_id }

        res = app.post(coffeeapp.coffee_addict_api_path, data=post_data)
        assert res.status_code == 200

        return card_id

init()
