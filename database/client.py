import logging

import asyncpgsa
from asyncpg import exceptions

logger = logging.getLogger(__name__)


class DatabaseClient:
    _instance = None
    _initialized = False
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseClient, cls).__new__(cls)
            cls._instance._initialized = True
        return cls._instance

    async def connect(self, dsn, max_size=20, timeout=60, **kwargs):
        try:
            self._pool = await asyncpgsa.create_pool(dsn, max_size=max_size, command_timeout=timeout, **kwargs)
        except (exceptions.InvalidCatalogNameError, exceptions.InvalidPasswordError,
                ConnectionRefusedError, OSError, ValueError) as error:
            raise error
        except Exception as err:
            raise err

    async def close(self):
        await self._pool.close()

    async def execute(self, sql):
        async with self._pool.acquire() as connection:
            return await connection.execute(sql)

    async def fetch_val(self, sql):
        async with self._pool.acquire() as connection:
            return await connection.fetchval(sql)

    async def fetch_one(self, sql):
        async with self._pool.acquire() as connection:
            return await connection.fetchrow(sql)

    async def fetch_all(self, sql):
        async with self._pool.acquire() as connection:
            return await connection.fetch(sql)

    @property
    def pool(self):
        return self._pool


async def run_database_client(dsn):
    logger.info('Starting DB picker_client.')
    client = DatabaseClient()
    await client.connect(dsn)


async def close_database_client():
    logger.info('Stopping DB picker_client.')
    client = DatabaseClient()
    await client.close()


def get_client():
    return DatabaseClient()
