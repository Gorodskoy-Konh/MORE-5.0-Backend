from sqlalchemy import Column, ForeignKey, TEXT
from sqlalchemy.dialects.postgresql import BIGINT

from app.database.base import Base


class OfficeProductTable(Base):
    __tablename__ = "assignment"
    office_id = Column(
        'office_id',
        BIGINT,
        ForeignKey('office.id'),
        primary_key=True
    )
    name = Column(
        'name',
        TEXT,
        ForeignKey('product.name')
    )
    # assignment_id = Column(
    #     "assignment_id",
    #     BIGINT,
    #     primary_key=True,
    #     nullable=False,
    #     autoincrement=True,
    #     index=True,
    # )
