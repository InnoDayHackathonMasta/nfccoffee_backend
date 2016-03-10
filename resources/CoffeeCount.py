from flask_restful import Resource, reqparse, fields, abort 
from common import utils
import random
from coffee_db_alchemy import AspiringCoffeeAddict, CoffeeAddict, \
        CoffeeMachine, CoffeeCount
from sqlalchemy.sql import and_, or_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

put_parser = reqparse.RequestParser()
put_parser.add_argument(
        'card_id', dest='card_id',
        required=True,
        help='The SmartCardId of the CoffeeAddict'
)
put_parser.add_argument(
        'machine_id', dest='machine_id', type=int,
        required=True,
        help='The CoffeeMachineId a coffee is taken from'
)
put_parser.add_argument(
        'api_key', dest='api_key',
        required=True,
        help='An api_key is required to create AspiringCoffeeAddicts'
)

class CoffeeCountController(Resource):

    def put(self):
        """
        updates a certain coffee count belonging to an addict and a machine
        """
        args = put_parser.parse_args()
        if utils.check_api_key(args.api_key):
            addict = utils.dbsession.query(CoffeeAddict) \
                    .filter(CoffeeAddict.card_id == \
                            args.card_id).one_or_none()
            if not addict:
                aspiring_addict = utils.dbsession.query(AspiringCoffeeAddict) \
                        .filter(AspiringCoffeeAddict.card_id == \
                                args.card_id).one_or_none()

                if not aspiring_addict:
                    # we have never seen this card_id
                    # create an aspiring addict for it
                    short_pin=str(random.randint(1000, 9999))
                    aspiring_addict = AspiringCoffeeAddict(card_id=args.card_id,\
                                        short_pin=short_pin)
                    utils.dbsession.add(aspiring_addict)
                    try:
                        utils.dbsession.commit()
                    except IntegrityError, e:
                        # unique constraint of card_id failed
                        utils.dbsession.rollback()
                        abort(409)

                return { "known" : False, 
                         "short_pin" : aspiring_addict.short_pin,
                         "url" : "http://example.com" }
            else:
                try:
                    machine = utils.dbsession.query(CoffeeMachine) \
                            .filter(CoffeeMachine.id == args.machine_id).one()
                except NoResultFound, e:
                    # no machine known with this machine_id
                    # todo: default msg of 404 is misleading
                    abort(404)

                # craft condition
                conditions = []
                conditions.append(CoffeeCount.addict == addict)
                conditions.append(CoffeeCount.machine == machine)
                condition = and_(*conditions)
                count = utils.dbsession.query(CoffeeCount) \
                    .filter(condition).one()

                count.count = count.count + 1 
                utils.dbsession.commit()
                return { "known" : True, 
                         "name" : addict.name,
                         "count" : count.count }
        else:
            # wrong api_key, YOU SHALL NOT PASS!
            abort(401)
