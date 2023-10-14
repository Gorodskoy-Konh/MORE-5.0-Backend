from sqlalchemy import Column, BIGINT, ForeignKey

from app.database.base import Base


class TerminalDB(Base):
    __tablename__ = "terminal"
    id = Column("id", BIGINT, primary_key=True, autoincrement=True)
    office_id = Column("office_id", BIGINT, ForeignKey('office.id'), primary_key=True, autoincrement=False)
    # products = relationship('ProductDB', secondary=TerminalProductDB, backref='terminal')
