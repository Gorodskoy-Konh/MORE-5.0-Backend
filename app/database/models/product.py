from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, BOOLEAN

from app.database.base import Base

product_table = Table('product',
                      Base.metadata,
                      Column('name', TEXT, primary_key=True))