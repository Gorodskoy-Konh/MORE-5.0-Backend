from sqlalchemy import Column, BIGINT, ForeignKey, TEXT

from app.database.base import Base


class QueueDB(Base):
    __tablename__ = "queue"
    office_id = Column("id", BIGINT, ForeignKey('office.id'), primary_key=True)
    product_name = Column('name', TEXT, ForeignKey('product.name'), primary_key=True)
