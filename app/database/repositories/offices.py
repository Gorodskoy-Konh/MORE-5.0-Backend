from math import radians, cos, asin, sqrt, sin

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.office import OfficeDB
from app.database.models.product import ProductDB
from app.database.models.terminal import TerminalDB
from app.database.models.terminal_product import TerminalProductDB
from app.database.models.working_hours import WorkingHoursDB
from app.database.repositories.base import BaseRepository
from app.schemas.models.common import WorkingHours
from app.schemas.models.offices import OfficeDto
from app.schemas.requests.offices import GetOfficesDto


class OfficesRepository(BaseRepository):
    def __init__(self, conn: AsyncSession) -> None:
        super().__init__(conn)

    async def get_offices(
            self, *, get_offices: GetOfficesDto
    ) -> list[OfficeDto]:
        query = select(OfficeDB, WorkingHoursDB).join(WorkingHoursDB)
        result: Result = await self.connection.execute(
            query
        )
        offices_hours_db = list(result.fetchall())
        query = select(OfficeDB.id, ProductDB)\
            .join(TerminalDB).join(TerminalProductDB).join(ProductDB)
        result: Result = await self.connection.execute(
            query
        )
        offices_products_db = list(result.fetchall())
        if get_offices.radius and get_offices.latitude and get_offices.longitude:
            lat1 = get_offices.latitude
            lon1 = get_offices.longitude
            rad_lat1 = radians(lat1)
            offices_hours_db = list(
                filter(
                    lambda office: 12742 * asin(
                        sqrt(
                            (pow(sin(radians(office[0].latitude - lat1) / 2), 2) +
                             pow(sin(radians(office[0].longitude - lon1) / 2), 2) *
                             cos(rad_lat1) * cos(radians(office[0].latitude))
                             )
                        )
                    ) <= get_offices.radius,
                    offices_hours_db
                )
            )
        id_to_office = dict()
        for office_db, working_hours in offices_hours_db:
            office_db: OfficeDB
            working_hours: WorkingHoursDB
            if office_db.id in id_to_office:
                id_to_office[office_db.id]["hours"].append(working_hours)
            else:
                id_to_office[office_db.id] = {
                    "office": office_db,
                    "hours": [self._get_working_hours_from_db_row(working_hours)],
                    "products": set()
                }
        for order_id, product in offices_products_db:
            if order_id in id_to_office:
                id_to_office[order_id]["products"].add(product.name)
        offices_dto = [
            self._get__full_office_from_db_rows(
                office["office"],
                office["hours"],
                list(office["products"])
            )
            for office in id_to_office.values()
        ]

        return offices_dto

    @staticmethod
    def _get__full_office_from_db_rows(office: OfficeDB, working_hours: list[WorkingHours], products: list[str]) -> OfficeDto:
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
            has_ramp=office.has_ramp,
            working_hours=working_hours,
            products=products
        )

    @staticmethod
    def _get_working_hours_from_db_row(working_hours: WorkingHoursDB) -> WorkingHours:
        return WorkingHours(
            begin=working_hours.begin,
            end=working_hours.end,
            is_individual=working_hours.individual,
            week_day=working_hours.week_day.value
        )
