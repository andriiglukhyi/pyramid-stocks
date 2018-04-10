from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from .meta import Base


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    password = Column(String, nullable=False, unique=True)
    email = Column(String)
    username = Column(String)