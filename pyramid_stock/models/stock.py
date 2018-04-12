from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey,
    Boolean
)
from .associste import association_table
from sqlalchemy.orm import relationship
from .meta import Base


class Stock(Base):
    __tablename__ = 'stock'
    account_id = Column(Text, ForeignKey('account.username'), nullable=False)
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False, unique=True)
    companyName = Column(String)
    exchange = Column(String)
    industry = Column(String)
    website = Column(String)
    description = Column(String)
    CEO = Column(String)
    issueType = Column(String)
    sector = Column(String)
    account = relationship("Account", secondary=association_table, back_populates='stock')