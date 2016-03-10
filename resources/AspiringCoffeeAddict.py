from flask_restful import Resource, reqparse, fields, abort
from common import utils
from coffee_db_alchemy import AspiringCoffeeAddict
from sqlalchemy.exc import IntegrityError
import random

post_parser = reqparse.RequestParser()
post_parser.add_argument(
        'card_id', dest='card_id',
        required=True,
        help='A card_id is required to create AspiringCoffeAddict'
)
post_parser.add_argument(
        'api_key', dest='api_key',
        required=True,
        help='An api_key is required to create AspiringCoffeeAddicts'
)

class AspiringCoffeeAddictController(Resource):
    def post(self):
        """
        Inserts an AspiringCoffeeAddict into the DB, given a
        card_id and the correct api_key is supplied.
        """
        args = post_parser.parse_args()
        if(utils.check_api_key(args.api_key)):
            try:
                short_pin=str(random.randint(1000, 9999))
                utils.dbsession.add(AspiringCoffeeAddict(card_id=args.card_id,\
                    short_pin=short_pin))
                utils.dbsession.commit()
                return { 'short_pin' : short_pin }
            except IntegrityError, e:
                # unique constraint of card_id failed
                utils.dbsession.rollback()
                abort(409)
        else:
            # wrong api_key, YOU SHALL NOT PASS!
            abort(401)

    def get(self):
        """
        Lists all card_ids of AspiringCoffeeAddicts
        """
        addicts = utils.dbsession.query(AspiringCoffeeAddict).all()
        out_dict = { 'card_ids' : [] }
        for addict in addicts:
            out_dict['card_ids'].append(addict.card_id)
        return out_dict 
