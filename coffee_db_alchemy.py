import os
import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func

DATABASE_FILE_NAME="coffee.db"

Base = declarative_base()

machine_admin_assoc_table = Table('machine_admin_assoc', Base.metadata,
                Column('coffeeaddict_id', Integer, ForeignKey('coffeeaddict.id')),
                Column('coffeemachine_id', Integer, ForeignKey('coffeemachine.id')))

class CoffeeAddict(Base):
    __tablename__ = 'coffeeaddict'
    id = Column(Integer, primary_key=True)
    card_id = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    administered_machines = relationship(
            "CoffeeMachine",
            secondary=machine_admin_assoc_table,
            back_populates="admins")
    machines = relationship("CoffeeCount", back_populates="addict")
    password_hash = Column(String(250))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
 
class CoffeeMachine(Base):
    __tablename__ = 'coffeemachine'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    costs_per_unit = Column(Numeric(10,2), nullable=False)
    currency = Column(String(10))
    admins = relationship(
            "CoffeeAddict",
            secondary=machine_admin_assoc_table,
            back_populates="administered_machines")
    addicts = relationship("CoffeeCount", back_populates="machine")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class CoffeeCount(Base):
    __tablename__ = 'coffeecount'
    coffeeaddict_id = Column(Integer, ForeignKey('coffeeaddict.id'),
            primary_key=True)
    coffeemachine_id = Column(Integer, ForeignKey('coffeemachine.id'),
            primary_key=True)
    count = Column(Integer)
    addict = relationship("CoffeeAddict", back_populates="machines")
    machine = relationship("CoffeeMachine", back_populates="addicts")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AspiringCoffeeAddict(Base):
    __tablename__ = 'aspiringcoffeeaddict'
    id = Column(Integer, primary_key=True)
    short_pin = Column(String(10), nullable=False)
    card_id = Column(String(250), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in
           self.__table__.columns}

def init_db():
    engine = create_engine('sqlite:///{}'.format(DATABASE_FILE_NAME))
    Base.metadata.create_all(engine)

def delete_db():
    if os.path.isfile(DATABASE_FILE_NAME):
        os.remove(DATABASE_FILE_NAME)
    

if __name__ == "__main__":
    init_db()
    print("db initialized")
