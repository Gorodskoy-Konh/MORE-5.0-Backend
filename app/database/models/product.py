from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.models.terminal_product import TerminalProductDB


class ProductDB(Base):
    __tablename__ = 'product'
    name = Column('name', TEXT, primary_key=True)
    terminals = relationship('TerminalDB', secondary=TerminalProductDB.__table__, backref='products')