from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from coffee_db_alchemy import Base, CoffeeAddict, CoffeeMachine, CoffeeCount
 
engine = create_engine('sqlite:///sqlite:///coffee.db',
        connect_args={'check_same_thread':False},
        poolclass=pool.SingletonThreadPool, pool_size=1)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

# TODO: regenerate and source from file
api_key = '8539e6e2b8f5117f64f7080d5cf91b97'

def check_api_key(key):
    return api_key == key

def is_email_valid(email):
    # TODO: how does a valid email look like?
    # do we want to only accept company addresses?
    return "@" in email
