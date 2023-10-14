from sqlalchemy import Column, ForeignKey, TEXT, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import BIGINT

from app.database.base import Base
from app.database.models.terminal import TerminalDB


class TerminalProductDB(Base):
    __tablename__ = "termnial_product"
    terminal_id = Column(
        'terminal_id',
        BIGINT,
        primary_key=True
    )
    office_id = Column(
        'office_id',
        BIGINT,
        primary_key=True
    )
    product_name = Column(
        'product_name',
        TEXT,
        ForeignKey('product.name'),
        primary_key=True,
    )
    __table_args__ = (ForeignKeyConstraint([terminal_id, office_id],
                                           [TerminalDB.id, TerminalDB.office_id]),
                      {})
