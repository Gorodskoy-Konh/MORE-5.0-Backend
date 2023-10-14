from sqlalchemy import Column, ForeignKey, CheckConstraint, TIMESTAMP, TEXT, UniqueConstraint
from sqlalchemy.dialects.postgresql import (
    BIGINT,
)
from sqlalchemy.sql.operators import le, and_, eq

from app.database.base import Base


class TicketDB(Base):
    __tablename__ = "ticket"
    product_name = Column(
        "product_name",
        TEXT,
        ForeignKey("product.name"),
        nullable=False
    )
    office_id = Column(
        "office_id",
        BIGINT,
        ForeignKey("office.id"),
        nullable=False
    )
    user_id = Column(
        "user_id",
        BIGINT,
        nullable=False
    )
    id = Column(
        "id",
        BIGINT,
        primary_key=True,
        autoincrement=True
    )

    issue_time = Column(
        "issue_time",
        TIMESTAMP
    )

    service_start_time = Column(
        "service_start_time",
        TIMESTAMP
    )

    service_finish_time = Column(
        "service_finish_time",
        TIMESTAMP
    )
    CheckConstraint(
        and_(le(issue_time, service_start_time),
             le(service_start_time, service_finish_time))
    )

    __table_args__ = (UniqueConstraint("product_name", "office_id", name="office_product"),)
