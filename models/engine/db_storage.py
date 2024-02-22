#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base


class DBStorage:
    """This class manages storage of hbnb models in a database"""
    __engine = None
    __session = None

    def __init__(self):
        '''Initialize the database storage'''
        username = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                username, password, host, database, pool_pre_ping=True)
            )

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def all(self, cls=None):
        '''Returns a dictionary of model currently in storage'''
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        if cls is None:
            cls_list = [User, State, City, Amenity, Place, Review]
        else:
            cls_list = [cls]

        dictionary = {}
        for class_name in cls_list:
            objs = self.__session.query(class_name).all()
            for obj in objs:
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                dictionary[key] = obj
        return dictionary

    def new(self, obj):
        '''Adds new object to the current database session'''
        self.__session.add(obj)

    def save(self):
        '''Commits all changes of the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''Delete an object obj from the current database session'''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''Creates all tables in the database and creates a new session'''
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False))

    def close(self):
        """Closes the session"""
        self.__session.close()
