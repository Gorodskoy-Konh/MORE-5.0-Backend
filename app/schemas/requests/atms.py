from typing import Optional

from pydantic import BaseModel, confloat


class GetATMsDto(BaseModel):
    latitude: Optional[confloat(strict=False, ge=-90, le=90)]
    longitude: Optional[confloat(strict=False, ge=-180, le=180)]
    radius: Optional[float]
