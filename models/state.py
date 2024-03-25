#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage, storage_type


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref='state',
                          cascade='all, delete-orphan')

    if storage_type != 'db':
        @property
        def cities(self):
            """ Getter method for cities related to the current State """
            from models.city import City

            return [city for city in storage.all(City).values()
                    if getattr(city, 'state_id') == self.id]
