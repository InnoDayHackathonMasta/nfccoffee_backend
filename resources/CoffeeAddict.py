from flask_restful import Resource, reqparse, fields, abort 
from common import utils
from coffee_db_alchemy import CoffeeAddict, AspiringCoffeeAddict, \
    CoffeeMachine, CoffeeCount

get_parser = reqparse.RequestParser()
get_parser.add_argument(
        'short_pin', dest='short_pin',
        location='args', required=True,
        help='A short_pin is required to register as CoffeeAddict'
)

post_parser = reqparse.RequestParser()
post_parser.add_argument(
        'short_pin', dest='short_pin',
        location='form', required=True,
        help='A short_pin is required to register as CoffeeAddict'
)
post_parser.add_argument(
        'name', dest='name',
        location='form', required=True,
        help='A name which is going to be attached to the freshly created CoffeeAddict'
)
post_parser.add_argument(
        'email', dest='email',
        location='form', required=True,
        help='An email address which is going to be attached to the freshly ' +
        'created CoffeeAddict'
)
post_parser.add_argument(
        'machine_id', dest='machine_id', type=int,
        location='form', required=True, action='append',
        help='Ids of the CoffeeMachines the freshly created CoffeeAddict can '
        + 'get his java from.'
)

class CoffeeAddictController(Resource):
    def post(self):
        """
        Create/Register CoffeeAddict
        """
        args = post_parser.parse_args()
        aspiring_addict = utils.dbsession.query(AspiringCoffeeAddict) \
            .filter(AspiringCoffeeAddict.short_pin == args.short_pin).first()

        if aspiring_addict:
            # is valid email?
            if not utils.is_email_valid(args.email):
                # unprocessable entity
                abort(422)
            # get coffee machine and set up assoc
            machines = []
            for machine_id in args.machine_id:
                machine = utils.dbsession \
                    .query(CoffeeMachine).filter(CoffeeMachine.id == machine_id).one_or_none()

                if not machine:
                    return { 'error' : 'don\'t know CoffeeMachine with id {}' \
                                .format(machine_id) }
                machines.append(machine)
            
            # todo: need to check if card_id already taken + make card_id unique
            new_addict = CoffeeAddict(card_id=aspiring_addict.card_id, \
                email=args.email, name=args.name)
            utils.dbsession.add(new_addict)

            for machine in machines:
                count_addict = CoffeeCount(count=0, addict=new_addict, \
                        machine=machine)
                utils.dbsession.add(count_addict)
                machine.addicts.append(count_addict)

            # delete AspiringAddict
            utils.dbsession.delete(aspiring_addict)
            utils.dbsession.commit()

            return { 'user' : args.email }
        else:
            # there is no aspiring addict with this short_pin, not found!
            abort(404)

    def get(self):
        """
        """
        args = get_parser.parse_args()

        # this should be handled better if the application should scale
        aspiring_addict = utils.dbsession.query(AspiringCoffeeAddict) \
            .filter(AspiringCoffeeAddict.short_pin == args.short_pin).first()

        if aspiring_addict:
            # should redirect to signup view
            return { 'card_id' : aspiring_addict.card_id }
        else:
            # no aspiring addict with supplied short_pin found
            return { 'error' : 'we do not know this short_pin' }
