from math import radians, cos, asin, sqrt, sin

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import eq

from app.database.models.atm import ATMDB
from app.database.repositories.base import BaseRepository
from app.schemas.models.atm import ATMDto, GetATMsDto


class ATMsRepository(BaseRepository):
    def __init__(self, conn: AsyncSession):
        super().__init__(conn)

    async def get_atms(
        self, *, get_atms: GetATMsDto
    ) -> list[GetATMsDto]:
        pass
