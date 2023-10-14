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


class ProductsRepository(BaseRepository):
    def __init__(self, conn: AsyncSession) -> None:
        super().__init__(conn)

    async def get_products(
            self
    ) -> list[OfficeDto]:
        query = select(ProductDB)
        result: Result = await self.connection.execute(
            query
        )
        products = list(product.name for product in result.scalars().all())
        return products

    @staticmethod
    def _get__full_office_from_db_rows(office: OfficeDB, working_hours: list[WorkingHours],
                                       products: list[str]) -> OfficeDto:
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
