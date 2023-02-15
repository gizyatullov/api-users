from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from loguru import logger

from fastapi_template.services import price_service
from fastapi_template.settings import settings

__all__ = [
    'init_repeaters',
]


def init_repeaters(app: FastAPI) -> None:
    @app.on_event('startup')
    @repeat_every(seconds=60 * settings.FREQUENCY_PRICE_UPDATES_IN_MINUTES,
                  logger=logger)
    async def run_update_price():
        await price_service.set_price()
        logger.info(f'price update, {settings.FREQUENCY_PRICE_UPDATES_IN_MINUTES} '
                    f'minutes have passed or first start')
