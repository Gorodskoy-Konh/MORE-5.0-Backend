from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT

from app.database.base import Base


class ProductDB(Base):
    __tablename__ = 'product'
    name = Column('name', TEXT, primary_key=True)
