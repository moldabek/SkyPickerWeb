import settings
from database.client import run_database_client
from picker_client.client import get_skypicker_client


async def set_data_to_db():
    skypicker_client = get_skypicker_client()
    await run_database_client(settings.DATABASE_URL)
    await skypicker_client.set_data_to_db()