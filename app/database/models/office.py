from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, BOOLEAN, DOUBLE_PRECISION
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.models.office_product import OfficeProductDB


class OfficeDB(Base):
    __tablename__ = 'office'
    id = Column('id', BIGINT, primary_key=True),
    name = Column('name', TEXT, unique=True),
    address = Column('address', TEXT),
    latitude = Column('latitude', DOUBLE_PRECISION),
    longitude = Column('longitude', DOUBLE_PRECISION),
    sale_point_format = Column('sale_point_format', TEXT),
    rko = Column('rko', BOOLEAN),
    kep = Column('kep', BOOLEAN),
    office_type = Column('office_type', BOOLEAN),
    suo_availability = Column('suo_availability', BOOLEAN),
    has_ramp = Column('has_ramp', BOOLEAN)
    products = relationship('ProductDB', secondary=OfficeProductDB, backref='offices')
