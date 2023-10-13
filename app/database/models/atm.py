from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, BOOLEAN, DOUBLE_PRECISION

from app.database.base import Base

atm_order_table = Table(
    "atm",
    Base.metadata,
    Column("id", BIGINT, primary_key=True),
    Column("address", TEXT),
    Column("latitude", DOUBLE_PRECISION),
    Column("longitude", DOUBLE_PRECISION),
    Column("allDay", BOOLEAN),
)
