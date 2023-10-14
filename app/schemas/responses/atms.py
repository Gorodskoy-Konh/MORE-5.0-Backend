from pydantic import BaseModel

from app.schemas.models.atm import ATMDto


class GetATMsResponse(BaseModel):
    offices: list[ATMDto]
