from sqlalchemy import Column, Table
from sqlalchemy.dialects.postgresql import TEXT

from app.database.base import Base

service_table = Table('service_database',
                      Base.metadata,
                      Column('name', TEXT, primary_key=True))
