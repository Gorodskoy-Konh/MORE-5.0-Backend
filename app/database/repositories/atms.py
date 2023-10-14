from math import radians, cos, asin, sqrt, sin

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import eq

from app.database.models.atm import ATMDB
from app.database.models.atm_condition import ATMConditionDB
from app.database.models.condition import ConditionDB

from app.database.repositories.base import BaseRepository
from app.schemas.models.atm import ATMDto, GetATMsDto


class ATMsRepository(BaseRepository):
    def __init__(self, conn: AsyncSession):
        super().__init__(conn)

    async def get_atms(
        self, *, get_atms: GetATMsDto
    ) -> list[GetATMsDto]:
        query = select(ATMDB, ATMConditionDB).join(ATMConditionDB)
        result: Result = await self.connection.execute(query)
        atms_db = list(result.fetchall())

        if get_atms.radius and get_atms.latitude and get_atms.longitude:
            lat1 = get_atms.latitude
            lon1 = get_atms.longitude
            rad_lat1 = radians(lat1)

            atms_db = list(
                filter(
                    lambda atm: 12742 * asin(
                        sqrt(
                            (pow(sin(radians(atm[0].latitude - lat1) / 2), 2) +
                            pow(sin(radians(atm[0].longitude - lon1) / 2), 2) * 
                            cos(rad_lat1) * cos(radians(atm[0].latitude)))
                        )
                    ) <= get_atms.radius,
                    atms_db
                )
            )

        id_to_atm = dict()

        for atm_db, atm_condition_db in atms_db:
            if atm_db.id in id_to_atm and atm_condition_db.active:
                id_to_atm[atm_db.id]["atm_conditions"].append(atm_condition_db.condition)
            else:
                id_to_atm[atm_db.id] = {
                    "atm": atm_db,
                    "atm_conditions": [atm_condition_db.condition]
                }

        atms_dto = [
            self._get_full_atm_from_db_rows(
                atm=atm['atm'],
                atm_conditions=atm['atm_conditions']
            )
            for atm in id_to_atm.values()
        ]
        return atms_dto

    @staticmethod
    def _get_full_atm_from_db_rows(self, atm, atm_conditions):
        return ATMDto(
            id=atm.id,
            address=atm.address,
            latitude=atm.latitude,
            longitude=atm.longitude,
            all_day=atm.all_day,
            conditions=atm_conditions
        )
