from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Table,
    Boolean
)
from .meta import Base

association_table = Table(
    'association', Base.metadata,
    Column('account_id', Integer, ForeignKey('account.id')),
    Column('stock_id', Integer, ForeignKey('stock.id'))
)