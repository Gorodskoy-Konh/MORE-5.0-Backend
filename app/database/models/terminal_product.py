from sqlalchemy import Column, ForeignKey, TEXT, BOOLEAN
from sqlalchemy.dialects.postgresql import BIGINT

from app.database.base import Base


class TerminalProductDB(Base):
    __tablename__ = "termnial_product"
    terminal_id = Column(
        'terminal_id',
        BIGINT,
        ForeignKey('terminal.id'),
        primary_key=True
    )
    product_name = Column(
        'product_name',
        TEXT,
        ForeignKey('product.name'),
        primary_key=True,
    )
    individual = Column('individual', BOOLEAN)
    legal = Column('legal', BOOLEAN)
