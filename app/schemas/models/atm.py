import datetime
from pydantic import BaseModel
from app.schemas.models.common import Hours


class ATM(BaseModel):
    id: int
    address: str
    allDay: bool

    latitude: float
    longitude: float

    services: [Tuple[str, bool]]
