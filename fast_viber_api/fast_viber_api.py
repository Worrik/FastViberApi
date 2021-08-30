import logging

from starlette.requests import Request

from fast_viber_api.viber_requests import *
from fast_viber_api.viberbot import ViberBot

logger = logging.getLogger()


def viber_api(bot: ViberBot):
    async def wrapper(viber: viber_request, request: Request):
        text = await request.body()
        sig = request.query_params.get('sig')

        logger.info("ViberRequest: %s", viber)

        if not bot.verify_signature(text, sig):
            logger.warning("Invalid signature")
            print("Invalid signature")
            return

        await bot.call_handlers(viber)

    return wrapper
