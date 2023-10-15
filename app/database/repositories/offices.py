import datetime
import random
from collections import defaultdict
from math import radians, cos, asin, sqrt, sin
from operator import le, eq, and_

import requests
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from algorithm.bank_algorithms.bank_client import BankClient
from algorithm.bank_algorithms.bank_priority_sort_algorithm import bank_priority_sort_algorithm
from algorithm.bank_algorithms.bank_queue import BankQueue
from algorithm.bank_algorithms.bank_terminal import BankTerminal
from algorithm.bank_algorithms.bank_unit import BankUnit
from app.database.models.office import OfficeDB
from app.database.models.product import ProductDB
from app.database.models.terminal import TerminalDB
from app.database.models.terminal_product import TerminalProductDB
from app.database.models.tickets import TicketDB
from app.database.models.working_hours import WorkingHoursDB
from app.database.repositories.base import BaseRepository
from app.schemas.models.common import WorkingHours
from app.schemas.models.offices import OfficeDto
from app.schemas.requests.offices import GetOfficesDto, GetBestOfficesDto


def get_way_time(lat1, lon1, lat2, lon2):
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    }
    token = '5b3ce3597851110001cf6248dd678c03ecc542f9b2b0164e94aa64e5'
    call = requests.get(
        f'https://api.openrouteservice.org/v2/directions/foot-walking?api_key={token}&start={lon1},'
        f'{lat1}&end={lon2},{lat2}',
        headers=headers)
    dic = dict(call.json())
    try:
        return dic['features'][0]['properties']['summary']['duration']
    except Exception as e:
        return None


def points_distance(lat1, lon1, lat2, lon2):
    return 12742 * asin(
        sqrt(
            (pow(sin(radians(lat2 - lat1) / 2), 2) +
             pow(sin(radians(lon2 - lon1) / 2), 2) *
             cos(radians(lat1)) * cos(radians(lat2))
             )
        )
    )


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
            offices_hours_db = list(
                filter(
                    lambda office: points_distance(
                        get_offices.latitude, get_offices.longitude,
                        office[0], office[1]
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

    async def get_best_offices(self, get_best_offices: GetBestOfficesDto):
        query = select(OfficeDB).join(TerminalDB).join(TerminalProductDB).join(ProductDB).where(
            eq(ProductDB.name, get_best_offices.product)).distinct()
        result: Result = await self.connection.execute(query)
        offices_db = result.scalars().all()

        if get_best_offices.radius and get_best_offices.latitude and get_best_offices.longitude:
            offices_db = list(
                filter(
                    lambda office: points_distance(
                        get_best_offices.latitude, get_best_offices.longitude,
                        office.longitude, office.latitude
                    ) <= get_best_offices.radius,
                    offices_db
                )
            )
        office_dic = {
            office.id: {
                "terminals": [],
                "office": office,
                "queue": [],
                "products": set()
            }
            for office in offices_db
        }
        terminals_query = select(TerminalDB).where(TerminalDB.office_id.in_(office_dic.keys()))
        result: Result = await self.connection.execute(terminals_query)
        terminals_db: list[TerminalDB] = list(result.scalars().all())
        for terminal in terminals_db:
            office_dic[terminal.office_id]["terminals"].append(terminal)
        tickets_query = select(TicketDB).where(
            and_(and_(TicketDB.office_id.in_(office_dic.keys()),
                      eq(TicketDB.service_finish_time, None)),
                 le(TicketDB.issue_time, datetime.datetime.now()))
        ).order_by(TicketDB.issue_time)
        result: Result = await self.connection.execute(tickets_query)
        tickets_db: list[TicketDB] = list(result.scalars().all())
        for ticket in tickets_db:
            office_dic[ticket.office_id]["queue"].append(ticket.product_name)
        products_query = select(ProductDB.name, OfficeDB.id) \
            .join(TerminalProductDB).join(TerminalDB) \
            .join(OfficeDB).where(OfficeDB.id.in_(office_dic.keys())).distinct()
        result: Result = await self.connection.execute(products_query)
        products_db = list(result.fetchall())
        for product_name, office_id in products_db:
            office_dic[office_id]["products"].add(product_name)
        offices = [
            office for office in office_dic.values() if get_best_offices.product in office["products"]
        ]
        user = BankClient(get_best_offices.product)
        banks = []
        for office in offices:
            office_db: OfficeDB = office["office"]
            queue = BankQueue(
                [
                    BankClient(product_name) for
                    product_name in office["queue"]
                ]
            )
            products_query = select(TerminalDB.id, ProductDB.name) \
                .join(TerminalProductDB).join(TerminalDB).where(
                eq(TerminalProductDB.office_id, office_db.id)).distinct()
            result: Result = await self.connection.execute(products_query)
            products_names = list(result.fetchall())
            terminal_product = defaultdict(set)
            for terminal_id, product_name in products_names:
                terminal_product[terminal_id].add(product_name)
            terminals = [
                BankTerminal(terminal_id, {product_name: random.randint(1, 400) for product_name in product_names}) for
                terminal_id, product_names in terminal_product.items()
            ]
            bank_id = office_db.id  # ID банка

            move_time = get_way_time(
                get_best_offices.latitude,
                get_best_offices.longitude,
                office_db.latitude,
                office_db.longitude)  # Время затрачиваемое на дорогу до банка (секунды).
            if not move_time:
                continue
            banks.append(BankUnit(bank_id, queue, terminals, move_time))
        average_waiting_time = 360  # Общее среднее время, которое клиент проводит в банке

        # Получаем список ID банков и оценочное время ожидания
        best_banks_estimated, best_banks_move = bank_priority_sort_algorithm(banks, user, average_waiting_time)
        best_bank_id, estimated_time = best_banks_estimated[0]
        return [best_bank_id, estimated_time]

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
