from typing import Optional

from pydantic import BaseModel, confloat


class GetOfficesDto(BaseModel):
    latitude: Optional[confloat(strict=False, ge=-90, le=90)]
    longitude: Optional[confloat(strict=False, ge=-180, le=180)]
    radius: Optional[float]


class OfficeDto(BaseModel):
    id: int
    name: str
    address: str
    latitude: float
    longitude: float
    sale_point_format: str
    rko: bool
    kep: bool
    office_type: bool
    suo_availability: bool
    has_ramp: bool
