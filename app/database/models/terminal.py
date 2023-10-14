from sqlalchemy import Column, BIGINT, ForeignKey

from app.database.base import Base


class TerminalDB(Base):
    __tablename__ = "atm"
    id = Column("id", BIGINT, primary_key=True)
    office_id = Column("id", BIGINT, ForeignKey('office.id'), primary_key=True)
