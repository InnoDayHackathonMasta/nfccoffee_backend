from flask import Flask, request, json, Response
from flask_restful import Resource, Api

from resources.AspiringCoffeeAddict import AspiringCoffeeAddictController
from resources.CoffeeAddict import CoffeeAddictController
from resources.CoffeeMachine import CoffeeMachineController
from resources.CoffeeCount import CoffeeCountController
import coffee_db_alchemy as db

application = Flask(__name__)
api = Api(application)
db.init_db()

class HelloWorld(Resource):
    def get(self):
        return {'greeting': 'hello world!'}

aspiring_coffee_addict_api_path = '/aspiringcoffeeaddict'
coffee_addict_api_path = '/coffeeaddict'
coffee_machine_api_path = '/coffeemachine'
coffee_count_api_path = '/coffeecount'

api.add_resource(HelloWorld, '/')
api.add_resource(AspiringCoffeeAddictController, aspiring_coffee_addict_api_path)
api.add_resource(CoffeeAddictController, coffee_addict_api_path)
api.add_resource(CoffeeMachineController, coffee_machine_api_path)
api.add_resource(CoffeeCountController, coffee_count_api_path)

@application.route('/index', methods=['GET'])
def index():
    addicts = ['a', 'b', 'c'] 
    out = '<h1>Some Chars</h1>\n<ul>\n' 
    for addict in addicts:
        out += '<li>{}</li>\n'.format(addict) 

    out += '</ul>'
    res = Response(out)
    return res

if __name__ == '__main__':
    application.debug = True
    application.run()
