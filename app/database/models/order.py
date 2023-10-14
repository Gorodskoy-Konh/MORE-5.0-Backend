from sqlalchemy import FLOAT, CheckConstraint, Column, ForeignKey
from sqlalchemy.dialects.postgresql import (
    ARRAY,
    BIGINT,
    CHAR,
    INTEGER,
    TIMESTAMP,
    TEXT
)
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.models.assignment_order import assignment_order_table


class OrderDB(Base):
    __tablename__ = "order"
    product_name = Column(
        "product_name",
        BIGINT,
        primary_key=True,
        ForeignKey("product_name")
    )
    office_id = Column(
        "office_id",
        BIGINT,
        primary_key=True,
        ForeignKey("office.id")
    )
    user_id = Column(
        "user_id",
        BIGINT,
        primary_key=True,
        autoincrement=True
    )

