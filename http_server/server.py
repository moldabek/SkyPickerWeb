from typing import List

from aiohttp import web
from aiohttp.web_response import json_response
from attr import asdict

import settings
from base.objects import PickerResponse, SkyPickerResponseObject
from picker_client.client import SkyPickerClient


async def get_tickets_by_months(request):  # noqa
    response_list: List[SkyPickerResponseObject] = await SkyPickerClient().get_tickets_cache()
    response = PickerResponse(picker_response=response_list)
    return json_response(response.as_dict())


async def check_ticket(request):
    payload = await request.json()
    if response := await SkyPickerClient().check_ticket(**payload):
        return json_response(asdict(response))
    return json_response({
        "data": "booking_token doesn't exist"
    })


class HttpServer:
    _instance = None
    _app = None
    _site = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HttpServer, cls).__new__(cls)
            cls._instance._initialized = True
        return cls._instance

    async def start(self):
        self._app = web.Application()
        self._app.add_routes([web.get('/get_tickets', get_tickets_by_months),
                              web.get('/check_ticket', check_ticket)])
        runner = web.AppRunner(self._app)
        await runner.setup()
        self._site = web.TCPSite(runner, host=settings.HTTP_HOST, port=settings.HTTP_PORT)
        await self._site.start()

        return True

    async def stop(self):
        await self._site.stop()
