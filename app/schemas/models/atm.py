from pydantic import BaseModel, confloat


class ATMDto(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float
    all_day: bool

    conditions: [str]
