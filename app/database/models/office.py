from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, BOOLEAN, DOUBLE_PRECISION

from app.database.base import Base

office_Table = Table('office',
                     Base.metadata,
                     Column('id', BIGINT, primary_key=True),
                     Column('name', TEXT),
                     Column('address', TEXT),
                     Column('latitude', DOUBLE_PRECISION),
                     Column('longitude', DOUBLE_PRECISION),

                     Column('salePointFormat', TEXT),

                     Column('rko', BOOLEAN),
                     Column('kep', BOOLEAN),
                     Column('officeType', BOOLEAN),
                     Column('suoAvailability', BOOLEAN),

                     Column('hasRamp', BOOLEAN))
