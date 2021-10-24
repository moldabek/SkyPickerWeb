import asyncio
import logging
import sys

import settings
from crontab_tasks import set_data_to_db
from database.client import run_database_client, get_client, close_database_client
from http_server import start_http_server, stop_http_server
from picker_client.client import get_skypicker_client

logger = logging.getLogger()
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter("%(levelname)s %(asctime)s %(message)s"))
logger.addHandler(consoleHandler)

db_client = get_client()
skypicker_client = get_skypicker_client()


async def initialize():
    await run_database_client(settings.DATABASE_URL)
    await skypicker_client.set_data_to_db()
    await start_http_server()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if sys.argv[1:]:
        if sys.argv[1] == 'update_data':
            loop.run_until_complete(set_data_to_db())
    else:
        loop.create_task(initialize())
        loop.run_forever()
        loop.run_until_complete(stop_http_server())
        loop.run_until_complete(close_database_client())
        loop.close()
