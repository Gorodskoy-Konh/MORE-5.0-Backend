from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import TIME

from app.database.base import Base

# TODO: Check TIME type for fitness in our case
working_hours_table = Table(
    "working_hours",
    Base.metadata,
    Column("begin", TIME, primary_key=True),
    Column("end", TIME, primary_key=True)
)
