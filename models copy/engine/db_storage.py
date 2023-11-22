#!/usr/bin/python3
""" define class DBStorage """
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import base_model
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """ DBStorage class """
    __engine = None
    __session = None

    def __init__(self):
        """ create engine """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(getenv("HBNB_MYSQL_USER"),
                                              getenv("HBNB_MYSQL_PWD"),
                                              getenv("HBNB_MYSQL_HOST"),
                                              getenv("HBNB_MYSQL_DB"),
                                              pool_pre_ping=True))
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query db session """
        cls_dic = {}
        if cls:
            query = self.__session.query(cls).all()
        else:
            cls_all = [User, State, City, Amenity, Place, Review]
            query = []
            for cls_name in cls_all:
                query += self.__session.query(cls_name).all()
        for obj in query:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            cls_dic[key] = obj
        return cls_dic

    def new(self, obj):
        """ add obj to current db session """
        self.__session.add(obj)

    def save(self):
        """ commit all changes of current db session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from current db session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ commit changes of current db session """
        self.__session = Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session()
