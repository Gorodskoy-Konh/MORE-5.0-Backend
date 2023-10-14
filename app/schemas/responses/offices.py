from pydantic import BaseModel

from app.schemas.models.offices import OfficeDto


class GetOfficesResponse(BaseModel):
    offices: list[OfficeDto]
