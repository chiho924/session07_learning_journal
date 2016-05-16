import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    )

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    """
    This MyModel class is the database that has three columns: id, name, and value.
    """

    __tablename__ = 'models'  # table name
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class Entry(Base):
    """
    This Entry class is the database that has five columns: id, title, body, created, and edited.
    """

    __tablename__ = 'entries'  # table name
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def all(cls, session=None):
        """
        Returns a query with all entries, ordered by creation date reversed.

        :param: session: the database session
        :return: all entries ordered by the creation date reversed
        """
        if session is None:
            session = DBSession
        return session.query(cls).order_by(sa.desc(cls.created)).all()

    @classmethod
    def by_id(cls, id, session=None):
        """
        Returns a single entry identified by id.  If no entry exists with the provided id, this
        class method will return None.

        :param id: the id of an entry to be retrieved
         :return a single entry identified by id
        """
        if session is None:
            session = DBSession
        return session.query(cls).get(id)


class User(Base):
    """
    This User class is the database that has three columns: id, name, and password.  The purpose of this
    User database is for authentication and authorization.
    """

    __tablename__ = 'users'  # table name
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), nullable=False, unique=True, index=True)
    password = Column(Unicode, nullable=False)

    @classmethod
    def by_name(cls, name, session=None):
        """
        Returns a first user given the username.

        :param username: the username
        :param session: the database session
        :return: a single user entry that corresponds to a given username
        """
        if session is None:
            session = DBSession
        return session.query(cls).filter(cls.name == name).first()