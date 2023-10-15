from datetime import time

from pydantic import BaseModel
from pydantic.types import confloat, constr


class Position(BaseModel):
    latitude: confloat(strict=False, ge=-90, le=90)
    longitude: confloat(strict=False, ge=-180, le=180)


class WorkingHours(BaseModel):
    begin: time
    end: time
    is_individual: bool
    week_day: constr(min_length=3, max_length=3, strict=False)
