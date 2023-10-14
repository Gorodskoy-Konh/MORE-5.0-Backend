from pydantic import BaseModel

from app.schemas.models.common import WorkingHours


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
    working_hours: list[WorkingHours]
    products: list[str]
