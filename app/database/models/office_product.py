from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, BOOLEAN

from app.database.base import Base

office_product_table = Table('office_product',
                             Base.metadata,
                             Column('office_id', BIGINT, ForeignKey('office.id'), primary_key=True),
                             Column('name', TEXT, ForeignKey('product.name')))
