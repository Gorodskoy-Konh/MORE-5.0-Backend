from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, BOOLEAN

from app.database.base import Base

working_hours_table = Table(
    "working_hours",
    Base.metadata,
    Column("order_id", BIGINT, ForeignKey("order.order_id")),
    Column("assignment_id", BIGINT, ForeignKey("assignment.assignment_id")),
)