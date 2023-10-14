from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT

from app.database.base import Base


class ConditionDB(Base):
    __tablename__ = 'condition'
    name = Column('name', TEXT, primary_key=True)
