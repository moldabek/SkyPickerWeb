import logging

from .server import HttpServer

__all__ = ['start_http_server', 'stop_http_server']
logger = logging.getLogger(__name__)


async def start_http_server():
    """
    Запуск Http сервера.
    """
    http_server = HttpServer()
    if not await http_server.start():
        logging.critical('Http Server start error.')
        raise Exception("Http Server start error.")
    logger.info('Starting Http Server')


async def stop_http_server():
    """
    Остановка Http сервера.
    """
    http_server = HttpServer()
    await http_server.stop()
    logger.info('Stopping Http Server')
