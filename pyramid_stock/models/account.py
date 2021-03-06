from .meta import Base
from datetime import datetime as dt
from sqlalchemy.exc import DBAPIError
from cryptacular import bcrypt
from .associste import association_table
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
)


manager = bcrypt.BCRYPTPasswordManager()


class Account(Base):
    """class for account instance"""
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    stock = relationship("Stock", secondary=association_table, back_populates='account')

    def __init__(self, username, email, password, admin=False):
        """
        init account inctance
        """
        self.username = username
        self.email = email
        self.password = manager.encode(password, 10)
        self.registered_on = dt.now()
        self.admin = admin

    @classmethod
    def check_credentials(cls, request=None, username=None, password=None):
        """check database"""
        if request.dbsession is None:
            raise DBAPIError
        is_authenticated = False
        query = request.dbsession.query(cls).filter(
            cls.username == username).one_or_none()
        if query is not None:
            if manager.check(query.password, password):
                is_authenticated = True

        return (is_authenticated, username)