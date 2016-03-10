from flask import Flask, request, json, Response, render_template
from flask_restful import Resource, Api

from resources.AspiringCoffeeAddict import AspiringCoffeeAddictController
from resources.CoffeeAddict import CoffeeAddictController
from resources.CoffeeMachine import CoffeeMachineController
from resources.CoffeeCount import CoffeeCountController
import coffee_db_alchemy as db
import requests
import json

application = Flask(__name__)
api = Api(application)
db.init_db()

class HelloWorld(Resource):
    def get(self):
        url = "http://nfc-coffee-dev.eu-west-1.elasticbeanstalk.com"
        json_data = json.dumps({ "longUrl" : url })
        headers = { "Content-Type" : "application/json" }
        # TODO: source from file
        g_api_key = ""
        r = requests.post("https://www.googleapis.com/urlshortener/v1/url?key={}"\
                .format(g_api_key), data=json_data, headers = headers)
        if r.status_code == 200:
            res_json = json.loads(r.content)
            return {'greeting': res_json['id']}
        else:
            return {'greeting': 'hello world!'}

aspiring_coffee_addict_api_path = '/aspiringcoffeeaddict'
coffee_addict_api_path = '/coffeeaddict'
coffee_machine_api_path = '/coffeemachine'
coffee_count_api_path = '/coffeecount'

api.add_resource(HelloWorld, '/hello')
api.add_resource(AspiringCoffeeAddictController, aspiring_coffee_addict_api_path)
api.add_resource(CoffeeAddictController, coffee_addict_api_path)
api.add_resource(CoffeeMachineController, coffee_machine_api_path)
api.add_resource(CoffeeCountController, coffee_count_api_path)

@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    application.debug = True
    application.run()
