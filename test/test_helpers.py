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

def create_coffee_machine(app):
    data = { "name" : "Senseo with <3",
               "costs_per_unit" : "0.35",
               "currency" : "EUR", 
               "api_key" :  utils.api_key }

    res = app.post(coffeeapp.coffee_machine_api_path, \
            data=data)

    assert 200 == res.status_code
    return res.data

def create_aspiring_addict_via_coffee_count(app):
    global helper_global_card_id
    data = { "card_id" : helper_global_card_id, 
              "api_key" : utils.api_key,
              "machine_id" : 1 }

    res = app.put(coffeeapp.coffee_count_api_path, data=data)

    assert 200 == res.status_code
    return res.data

def create_coffee_addict(app):
        """
        creates a 'functional' CoffeeAddict 
        which can be used for further testing

        return dict of 'card_id' and 'machine_id' 
        """
        global helper_global_card_id

        res_aspiring_api = create_aspiring_addict_via_coffee_count(app)
        json_aspiring = json.loads(res_aspiring_api)
        res_machine_api = create_coffee_machine(app)
        json_machine = json.loads(res_machine_api)

        post_data = { "short_pin" : json_aspiring["short_pin"],
                       "name" : "john",
                       "email" : "john.doe@siemens.com",
                       "machine_id" : json_machine["machine_id"] }

        res = app.post(coffeeapp.coffee_addict_api_path, data=post_data)

        return { "machine_id" : json_machine["machine_id"], 
                 "card_id" : helper_global_card_id,
                 "api_key" : utils.api_key }

init()
