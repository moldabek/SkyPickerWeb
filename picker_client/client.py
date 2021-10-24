import asyncio
import datetime
from datetime import date

import aiohttp
from attr import asdict
from sqlalchemy import and_

from base import SkyPickerResponseObject, CheckObject, get_days_for_month
from database.client import get_client
from database.schemas import Ticket
from settings import SKYPICKER_BASE_HOST_NAME, PARTNER_NAME, PRICE_CURRENCY, SKYPICKER_CHECK_HOST

ROUTES = [
    ('ALA', 'TSE'),
    ('TSE', 'ALA'),
    ('ALA', 'MOW'),
    ('MOW', 'ALA'),
    ('ALA', 'CIT'),
    ('CIT', 'ALA'),
    ('TSE', 'MOW'),
    ('MOW', 'TSE'),
    ('TSE', 'LED'),
    ('LED', 'TSE'),
]


class SkyPickerClient:
    _db_client = None

    def __init__(self):
        self._db_client = get_client()

    async def get_tickets_cache(self):
        records = await self._db_client.fetch_all(Ticket.select().where(Ticket.c.date >= date.today()))
        return [SkyPickerResponseObject(**dict(record)) for record in records]

    async def set_data_to_db(self):
        days = get_days_for_month()
        task_list = []
        for day in days:
            for route in ROUTES:
                task_list.append(asyncio.create_task(self._get_data(fly_from=route[0], fly_to=route[1],
                                                                    date_from=day, date_to=day)))
        await asyncio.gather(*task_list)

    async def check_ticket(self, ticket_date: str, fly_from: str, fly_to: str):
        date_ = datetime.datetime.strptime(ticket_date, "%d/%m/%Y")
        if record := await self._get_ticket_cache(date_.date(), fly_from, fly_to):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        SKYPICKER_CHECK_HOST,
                        params=self._get_param_for_check(booking_token=record['booking_token']),
                ) as response:
                    result = await response.json()
            resp_object = CheckObject(
                valid=(not result.get('flights_invalid')) if isinstance(result, dict) else False,
                booking_token=record['booking_token']
            )
            return resp_object
        return None

    @staticmethod
    def _get_param_for_check(booking_token: str) -> dict:
        return dict(v=2,
                    bnum=1,
                    pnum=1,
                    booking_token=booking_token)

    @staticmethod
    def _get_param_for_get(fly_from: str, fly_to: str, date_from: date, date_to: date) -> dict:
        return dict(fly_from=fly_from,
                    fly_to=fly_to,
                    partner=PARTNER_NAME,
                    date_from=date_from.strftime('%d/%m/%Y'),
                    date_to=date_to.strftime('%d/%m/%Y'),
                    sort='price',
                    adults=1,
                    curr=PRICE_CURRENCY)

    async def _get_data(self, fly_from: str, fly_to: str, date_from, date_to):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    SKYPICKER_BASE_HOST_NAME,
                    params=self._get_param_for_get(fly_from, fly_to, date_from, date_to),
            ) as response:
                result = await response.json()
            resp_object = SkyPickerResponseObject(
                price=result.get('data')[0].get('price') if result.get('data') != [] else 0,
                booking_token=result.get('data')[0].get('booking_token') if result.get(
                    'data') != [] else "Doesn't exist",
                date=date_to,
                fly_to=fly_to,
                fly_from=fly_from
            )
            return await self._set_data_to_db(resp_object)

    async def _set_data_to_db(self, resp_object: SkyPickerResponseObject):
        record = await self._get_ticket_cache(ticket_date=resp_object.date, fly_from=resp_object.fly_from,
                                              fly_to=resp_object.fly_to)
        if record:
            record = await self._update_ticket_cache(**asdict(resp_object))
        else:
            record = await self._create_ticket_cache(**asdict(resp_object))
        return record

    async def _create_ticket_cache(self, **kwargs):
        return await self._db_client.fetch_all(Ticket.insert().values(kwargs).returning(Ticket))

    async def _get_ticket_cache(self, ticket_date: date, fly_from: str, fly_to: str):
        return await self._db_client.fetch_one(Ticket.select().where(
            and_(Ticket.c.date == ticket_date,
                 Ticket.c.fly_from == fly_from,
                 Ticket.c.fly_to == fly_to)
        ))

    async def _update_ticket_cache(self, **kwargs):
        return await self._db_client.fetch_one(
            Ticket.update().values(kwargs).where(
                and_(Ticket.c.date == kwargs.get('ticket_date'),
                     Ticket.c.fly_from == kwargs.get('fly_from'),
                     Ticket.c.fly_to == kwargs.get('fly_to'))
            ).returning(Ticket))


def get_skypicker_client():
    return SkyPickerClient()
