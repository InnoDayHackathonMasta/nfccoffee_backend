from flask_restful import Resource, reqparse, fields, abort 
from common import utils
from sqlalchemy.exc import IntegrityError
from coffee_db_alchemy import CoffeeAddict, AspiringCoffeeAddict, \
    CoffeeMachine, CoffeeCount

post_parser = reqparse.RequestParser()
post_parser.add_argument(
        'name', dest='name',
        location='form', required=True,
        help='A name for the CoffeeMachine'
)
post_parser.add_argument(
        'costs_per_unit', dest='costs_per_unit',
        location='form', required=True,
        help='The costs per unit of coffee from this CoffeeMachine'
)
post_parser.add_argument(
        'currency', dest='currency',
        location='form', required=True,
        help='The currency in which the costs are charged'
)
post_parser.add_argument(
        'api_key', dest='api_key',
        location='form', required=True,
        help='An api_key is required to create CoffeeMachines'
)

class CoffeeMachineController(Resource):
    def post(self):
        """
        Creates a CoffeeMachine
        """
        args = post_parser.parse_args()

        if(utils.check_api_key(args.api_key)):
            try:
                new_machine = CoffeeMachine(name=args.name, \
                    costs_per_unit=args.costs_per_unit, \
                    currency=args.currency)
                utils.dbsession.add(new_machine)
                utils.dbsession.commit()
            except IntegrityError, e:
                utils.dbsession.rollback()
                abort(409)
            return { "machine_id" : new_machine.id }
        else:
            # wrong api_key, YOU SHALL NOT PASS!
            abort(401)


    def get(self):
        """
        List machines
        """
        machines = utils.dbsession.query(CoffeeMachine).all()
        out_dict = { 'names' : [] }
        for machine in machines:
            out_dict['names'].append(machine.name)

        return out_dict 
