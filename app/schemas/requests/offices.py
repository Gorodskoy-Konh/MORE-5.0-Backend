from datetime import datetime
from typing import Optional

from pydantic import BaseModel, confloat


class GetOfficesDto(BaseModel):
    latitude: Optional[confloat(strict=False, ge=-90, le=90)]
    longitude: Optional[confloat(strict=False, ge=-180, le=180)]
    radius: Optional[float]


class GetBestOfficesDto(BaseModel):
    latitude: confloat(strict=False, ge=-90, le=90)
    longitude: confloat(strict=False, ge=-180, le=180)
    radius: float
    product: str
    booking_time: Optional[datetime]
