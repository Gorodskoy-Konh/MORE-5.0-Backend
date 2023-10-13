from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, BOOLEAN

from app.database.base import Base

atm_service_table = Table('atm_service_table',
                          Base.metadata,
                          Column('atm_id', BIGINT, ForeignKey('atm.id'), primary_key=True),
                          Column('service', TEXT, ForeignKey('service.name'), primary_key=True),
                          Column('active', BOOLEAN)
                          )
