from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, BOOLEAN, DOUBLE_PRECISION
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.models.atm_service import ATMConditionDB


class ATMDB(Base):
    __tablename__ = "atm"
    id = Column("id", BIGINT, primary_key=True)
    address = Column("address", TEXT)
    latitude = Column("latitude", DOUBLE_PRECISION)
    longitude = Column("longitude", DOUBLE_PRECISION)
    all_day = Column("all_day", BOOLEAN)
    conditions = relationship('ConditionDB', secondary=ATMConditionDB, backref='atms')
