import enum

from sqlalchemy import Column, BIGINT, BOOLEAN, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import TIME
from sqlalchemy.orm import relationship

from app.database.base import Base


class WeekDays(enum.Enum):
    monday = "MON"
    tuesday = "TUE"
    wednesday = "WED"
    thursday = "THU"
    friday = "FRI"
    saturday = "SAT"
    sunday = "SUN"


class WorkingHoursDB(Base):
    __tablename__ = "working_hours"
    begin = Column("begin", TIME)
    end = Column("end", TIME)
    office_id = Column("office_id", BIGINT, ForeignKey('office.id'), primary_key=True)
    individual = Column("is_individual", BOOLEAN, primary_key=True)
    week_day = Column("week_day", Enum(WeekDays), primary_key=True)
    working_hours = relationship('OfficeDB', backref='working_hours')
