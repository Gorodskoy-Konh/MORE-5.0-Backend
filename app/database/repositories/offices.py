from math import radians, cos, asin, sqrt, sin

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import eq

from app.database.models.office import OfficeDB
from app.database.repositories.base import BaseRepository
from app.schemas.models.offices import OfficeDto, GetOfficesDto


class OfficesRepository(BaseRepository):
    def __init__(self, conn: AsyncSession) -> None:
        super().__init__(conn)

    async def get_offices(
            self, *, get_offices: GetOfficesDto
    ) -> list[OfficeDto]:
        from sqlalchemy import select
        query = select(OfficeDB)
        print(get_offices.city)
        if get_offices.city:
            query = query.where(eq(OfficeDB.address, get_offices.city))

        print(get_offices.latitude)
        result: Result = await self.connection.execute(
            query
        )
        offices_dto = [self._get_office_from_db_row(office_db) for office_db in result.scalars().all()]
        if get_offices.radius and get_offices.latitude and get_offices.longitude:
            lat1 = get_offices.latitude
            lon1 = get_offices.longitude
            rad_lat1 = radians(lat1)
            offices_dto = list(
                filter(
                    lambda office: 12742 * asin(
                        sqrt(
                            (pow(sin(radians(office.latitude - lat1) / 2), 2) +
                             pow(sin(radians(office.longitude - lon1) / 2), 2) *
                             cos(rad_lat1) * cos(radians(office.latitude))
                             )
                        )
                    ) <= get_offices.radius,
                    offices_dto
                )
            )
        return offices_dto

    @staticmethod
    def _get_office_from_db_row(office: OfficeDB) -> OfficeDto:
        return OfficeDto(
            id=office.id,
            name=office.name,
            address=office.address,
            latitude=office.latitude,
            longitude=office.longitude,
            sale_point_format=office.sale_point_format,
            rko=office.rko,
            kep=office.kep,
            office_type=office.office_type,
            suo_availability=office.suo_availability,
            has_ramp=office.has_ramp
        )
