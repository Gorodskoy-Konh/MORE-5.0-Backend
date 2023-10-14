from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, BOOLEAN

from app.database.base import Base


class ATMConditionDB(Base):
    __tablename__ = "atm_condition"
    atm_id = Column(
        'atm_id',
        BIGINT,
        ForeignKey('atm.id'),
        primary_key=True
    )
    condition = Column(
        'condition',
        TEXT,
        ForeignKey('condition.name'),
        primary_key=True
    )
    active = Column(
        'active',
        BOOLEAN
    )
