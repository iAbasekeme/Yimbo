from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from . import Base
from models import users

classes = {'users': users}


class DatabaseStorage():
    __engine
    __session

    def __init__(self):
        YIMBO_MYSQL_USER = getenv('YIMBO_MYSQL_USER')
        YIMBO_MYSQL_PWD = getenv('YIMBO_MYSQL_PWD')
        YIMBO_MYSQL_HOST = getenv('YIMBO_MYSQL_HOST')
        YIMBO_MYSQL_DB = getenv('YIMBO_MYSQL_DB')
        YIMBO_ENV = getenv('YIMBO_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(YIMBO_MYSQL_USER,
                                             YIMBO_MYSQL_PWD,
                                             YIMBO_MYSQL_HOST,
                                             YIMBO_MYSQL_DB))
    Base.metadata.drop_all()

    def all(self, cls=None):
        '''A method that queries all objects with the class name'''
        new_dict = {}
        for clss in classes:
            if cls is clss or cls in classes[clss]:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    obj[key] = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        return new_dict

    def new(self, obj):
        '''A method that creates a new obj'''
        self.__session.add(obj)

    def save(self):
        '''A method that commits the current transaction'''
        self.__session.commit()

    def delete(self, obj):
        '''A method that deletes an obj'''
        if obj is not None:
            self.__session.delete(obj)

    def update_db(self):
        '''A method that updates the db with tables'''
    Base.metadata.create_all(self.__engine)
    db_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
    Session = scoped_session(db_session)
    self.__session = Session()

    def close(self):
        '''A method that removes a session'''
        self.__session.remove()

    def get(self, cls, id):
        '''A method that gets an obj by it's class and id'''
        if cls not in classes.values():
            return None
        else:
            class_obj = self.all(cls)
            for obj in class_obj:
                if (obj.id == id):
                    return obj

    def count(self, cls=None):
        '''A method that counts all objects in a class'''
        pass
