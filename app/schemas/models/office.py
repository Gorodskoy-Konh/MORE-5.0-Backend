from enum import Enum
from typing import Optional
import datetime

from pydantic import BaseModel

from app.schemas.models.common import Hours


class WorkingHours(BaseModel):
    begin: datetime.time
    end: datetime.time


class Product(BaseModel):
    name: str


class Office(BaseModel):
    id: int
    name: str
    address: str
    salePointFormat: str

    # services
    kep: bool
    rko: bool
    officeType: bool
    sudoAvailability: bool
    products: [Product]

    hasRamp: bool

    workingHours: [WorkingHours]

    latidude: float
    longtitude: float
