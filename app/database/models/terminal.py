from sqlalchemy import Column, BIGINT, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.models.terminal_product import TerminalProductDB


class TerminalDB(Base):
    __tablename__ = "terminal"
    id = Column("id", BIGINT, primary_key=True)
    office_id = Column("id", BIGINT, ForeignKey('office.id'), primary_key=True)
    products = relationship('ProductDB', secondary=TerminalProductDB, backref='terminal')
