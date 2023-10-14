from pydantic import BaseModel
from pydantic.types import confloat


class Position(BaseModel):
    latitude: confloat(strict=False, ge=-90, le=90)
    longitude: confloat(strict=False, ge=-180, le=180)
